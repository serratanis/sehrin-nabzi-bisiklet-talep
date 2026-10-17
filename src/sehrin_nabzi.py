"""Şehrin Nabzı projesinin veri, model ve tahmin işlevleri."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


TARGET = "kiralama_sayisi"
CATEGORICAL_FEATURES = [
    "mevsim",
    "ay",
    "saat",
    "tatil",
    "hafta_gunu",
    "is_gunu",
    "hava_durumu",
]
NUMERIC_FEATURES = ["sicaklik_c", "nem_yuzde", "ruzgar_kmh", "yagis_mm"]
FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES


@dataclass(frozen=True)
class TrainingResult:
    model: Pipeline
    x_train: pd.DataFrame
    x_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series
    predictions: np.ndarray
    metrics: dict[str, float | int | str]


def load_dataset(path: str | Path) -> pd.DataFrame:
    """İşlenmiş CSV'yi temel kalite kontrolleriyle okur."""

    data = pd.read_csv(path, parse_dates=["tarih_saat"])
    required = set(FEATURES + [TARGET, "tarih", "yil"])
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Veri setinde eksik sütunlar var: {sorted(missing)}")
    if data.empty:
        raise ValueError("Veri seti boş.")
    if data[FEATURES + [TARGET]].isna().any().any():
        raise ValueError("Model sütunlarında eksik değer var.")
    if not data["tarih_saat"].is_monotonic_increasing:
        raise ValueError("Veri zaman sırasına göre artan olmalı.")
    return data


def build_model() -> Pipeline:
    """Kategorileri kodlayan ve sayıları ölçekleyen doğrusal modeli kurar."""

    preprocessing = ColumnTransformer(
        transformers=[
            (
                "kategorik",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES,
            ),
            ("sayisal", StandardScaler(), NUMERIC_FEATURES),
        ]
    )
    return Pipeline(
        steps=[
            ("on_isleme", preprocessing),
            ("model", LinearRegression()),
        ]
    )


def train_and_evaluate(
    data: pd.DataFrame, test_size: float = 0.20
) -> TrainingResult:
    """Veriyi zaman sırasını koruyarak böler, modeli eğitir ve ölçer."""

    x = data[FEATURES]
    y = data[TARGET]
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=test_size,
        shuffle=False,
    )

    model = build_model()
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    baseline = np.full(len(y_test), float(y_train.mean()))
    metrics: dict[str, float | int | str] = {
        "satir_sayisi": int(len(data)),
        "kaynak_yolculuk_sayisi": int(data[TARGET].sum()),
        "egitim_satiri": int(len(x_train)),
        "test_satiri": int(len(x_test)),
        "egitim_donemi": (
            f"{data['tarih_saat'].iloc[0]:%Y-%m-%d} / "
            f"{data['tarih_saat'].iloc[len(x_train)-1]:%Y-%m-%d}"
        ),
        "test_donemi": (
            f"{data['tarih_saat'].iloc[len(x_train)]:%Y-%m-%d} / "
            f"{data['tarih_saat'].iloc[-1]:%Y-%m-%d}"
        ),
        "r2": float(r2_score(y_test, predictions)),
        "mae": float(mean_absolute_error(y_test, predictions)),
        "rmse": float(mean_squared_error(y_test, predictions) ** 0.5),
        "baseline_mae": float(mean_absolute_error(y_test, baseline)),
    }
    return TrainingResult(
        model=model,
        x_train=x_train,
        x_test=x_test,
        y_train=y_train,
        y_test=y_test,
        predictions=predictions,
        metrics=metrics,
    )


def tahmin_et(
    model: Pipeline,
    *,
    mevsim: int,
    ay: int,
    saat: int,
    tatil: int,
    hafta_gunu: int,
    is_gunu: int,
    hava_durumu: int,
    sicaklik_c: float,
    nem_yuzde: float,
    ruzgar_kmh: float,
    yagis_mm: float,
) -> int:
    """Tek bir saat için talebi negatif olmayacak biçimde tahmin eder."""

    values: dict[str, Any] = {
        "mevsim": mevsim,
        "ay": ay,
        "saat": saat,
        "tatil": tatil,
        "hafta_gunu": hafta_gunu,
        "is_gunu": is_gunu,
        "hava_durumu": hava_durumu,
        "sicaklik_c": sicaklik_c,
        "nem_yuzde": nem_yuzde,
        "ruzgar_kmh": ruzgar_kmh,
        "yagis_mm": yagis_mm,
    }
    frame = pd.DataFrame([values], columns=FEATURES)
    prediction = float(model.predict(frame)[0])
    return int(round(max(0.0, prediction)))


def tahmini_yorumla(kiralama_sayisi: int) -> str:
    """Sayısal tahmini kullanıcı için anlaşılır bir cümleye dönüştürür."""

    if kiralama_sayisi < 250:
        level = "düşük"
    elif kiralama_sayisi < 700:
        level = "orta"
    else:
        level = "yüksek"
    return (
        f"Bu koşullar için yaklaşık {kiralama_sayisi} yolculuk başlangıcı bekleniyor. "
        f"Tahmini talep düzeyi {level}."
    )

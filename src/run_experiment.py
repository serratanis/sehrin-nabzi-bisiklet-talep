"""EDA grafiklerini, modeli, metrikleri ve örnek tahminleri üretir."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from sehrin_nabzi import load_dataset, tahmin_et, tahmini_yorumla, train_and_evaluate


COLORS = {
    "navy": "#17324D",
    "blue": "#2A6F97",
    "cyan": "#61A5C2",
    "yellow": "#F2C14E",
    "red": "#D95D39",
    "gray": "#E9EEF2",
}


def save_figures(data: pd.DataFrame, result, assets_dir: Path) -> None:
    plt.rcParams.update({"font.size": 11, "axes.titlesize": 14, "axes.labelsize": 11})

    hourly = data.groupby("saat", as_index=False)["kiralama_sayisi"].mean()
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.plot(hourly["saat"], hourly["kiralama_sayisi"], color=COLORS["blue"], linewidth=2.8)
    ax.fill_between(hourly["saat"], hourly["kiralama_sayisi"], color=COLORS["cyan"], alpha=0.18)
    ax.set(title="Saatlere Göre Ortalama Bisiklet Talebi", xlabel="Saat", ylabel="Ortalama kiralama sayısı")
    ax.set_xticks(range(0, 24, 2))
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(assets_dir / "01_saatlik_talep.png", dpi=180)
    plt.close(fig)

    weather_labels = {1: "Açık", 2: "Puslu", 3: "Yağışlı", 4: "Şiddetli"}
    weather = data.groupby("hava_durumu")["kiralama_sayisi"].mean().reindex([1, 2, 3, 4])
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    bars = ax.bar([weather_labels[i] for i in weather.index], weather.values, color=[COLORS["blue"], COLORS["cyan"], COLORS["yellow"], COLORS["red"]])
    ax.bar_label(bars, fmt="%.0f", padding=4)
    ax.set(title="Hava Durumuna Göre Ortalama Talep", xlabel="Hava durumu", ylabel="Ortalama kiralama sayısı")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(assets_dir / "02_hava_durumu_talebi.png", dpi=180)
    plt.close(fig)

    sample = data.sample(n=min(3500, len(data)), random_state=42)
    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    scatter = ax.scatter(sample["sicaklik_c"], sample["kiralama_sayisi"], c=sample["saat"], cmap="viridis", alpha=0.4, s=18)
    colorbar = fig.colorbar(scatter, ax=ax)
    colorbar.set_label("Saat")
    ax.set(title="Sıcaklık ve Bisiklet Talebi", xlabel="Sıcaklık (°C)", ylabel="Saatlik yolculuk başlangıcı")
    ax.grid(alpha=0.18)
    fig.tight_layout()
    fig.savefig(assets_dir / "03_sicaklik_talep.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.8, 6.0))
    ax.scatter(result.y_test, result.predictions, alpha=0.25, s=18, color=COLORS["blue"])
    maximum = max(float(result.y_test.max()), float(result.predictions.max()))
    ax.plot([0, maximum], [0, maximum], linestyle="--", color=COLORS["red"], linewidth=2, label="Kusursuz tahmin")
    ax.set(title="Gerçek ve Tahmin Edilen Kiralama Sayıları", xlabel="Gerçek değer", ylabel="Model tahmini")
    ax.legend(frameon=False)
    ax.grid(alpha=0.18)
    fig.tight_layout()
    fig.savefig(assets_dir / "04_gercek_tahmin.png", dpi=180)
    plt.close(fig)


def main() -> None:
    project_dir = Path(__file__).resolve().parents[1]
    data_path = project_dir / "data" / "processed" / "sehrin_nabzi_bisiklet_talebi.csv"
    assets_dir = project_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    data = load_dataset(data_path)
    result = train_and_evaluate(data)
    save_figures(data, result, assets_dir)

    joblib.dump(result.model, assets_dir / "sehrin_nabzi_model.joblib")
    (assets_dir / "model_metrikleri.json").write_text(
        json.dumps(result.metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    examples = [
        {
            "senaryo": "Serin iş günü sabahı",
            "mevsim": 1,
            "ay": 4,
            "saat": 8,
            "tatil": 0,
            "hafta_gunu": 1,
            "is_gunu": 1,
            "hava_durumu": 1,
            "sicaklik_c": 14.0,
            "nem_yuzde": 58.0,
            "ruzgar_kmh": 11.0,
            "yagis_mm": 0.0,
        },
        {
            "senaryo": "Sıcak hafta sonu öğleden sonrası",
            "mevsim": 2,
            "ay": 7,
            "saat": 16,
            "tatil": 0,
            "hafta_gunu": 5,
            "is_gunu": 0,
            "hava_durumu": 1,
            "sicaklik_c": 31.0,
            "nem_yuzde": 48.0,
            "ruzgar_kmh": 9.0,
            "yagis_mm": 0.0,
        },
        {
            "senaryo": "Yağışlı kış gecesi",
            "mevsim": 4,
            "ay": 12,
            "saat": 23,
            "tatil": 0,
            "hafta_gunu": 2,
            "is_gunu": 1,
            "hava_durumu": 3,
            "sicaklik_c": 5.0,
            "nem_yuzde": 86.0,
            "ruzgar_kmh": 20.0,
            "yagis_mm": 2.0,
        },
    ]
    rows = []
    for example in examples:
        inputs = {key: value for key, value in example.items() if key != "senaryo"}
        prediction = tahmin_et(result.model, **inputs)
        rows.append({**example, "tahmin": prediction, "yorum": tahmini_yorumla(prediction)})
    pd.DataFrame(rows).to_csv(assets_dir / "yeni_ornek_tahminleri.csv", index=False)

    summary = {
        "shape": list(data.shape),
        "missing_values": int(data.isna().sum().sum()),
        "target_mean": float(data["kiralama_sayisi"].mean()),
        "target_median": float(data["kiralama_sayisi"].median()),
        "hourly_peak": int(data.groupby("saat")["kiralama_sayisi"].mean().idxmax()),
        "weather_means": {
            str(int(key)): float(value)
            for key, value in data.groupby("hava_durumu")["kiralama_sayisi"].mean().items()
        },
        "source_trip_count": int(data["kiralama_sayisi"].sum()),
        "date_range": [
            data["tarih_saat"].min().strftime("%Y-%m-%d"),
            data["tarih_saat"].max().strftime("%Y-%m-%d"),
        ],
        "excluded_out_of_scope_rows": 36,
        "correlations": {
            column: float(data[[column, "kiralama_sayisi"]].corr().iloc[0, 1])
            for column in ["sicaklik_c", "nem_yuzde", "ruzgar_kmh", "yagis_mm"]
        },
    }
    (assets_dir / "veri_ozeti.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(json.dumps(result.metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

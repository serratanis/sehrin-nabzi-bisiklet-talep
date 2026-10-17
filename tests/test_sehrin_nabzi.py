from pathlib import Path
import sys

import pandas as pd


PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR / "src"))

from sehrin_nabzi import FEATURES, load_dataset, tahmin_et, train_and_evaluate
from interface_helpers import (
    demand_level,
)


DATA_PATH = PROJECT_DIR / "data" / "processed" / "sehrin_nabzi_bisiklet_talebi.csv"


def test_dataset_has_required_columns_and_no_missing_values():
    data = load_dataset(DATA_PATH)
    assert len(data) == 8760
    assert data["yil"].unique().tolist() == [2025]
    assert int(data["kiralama_sayisi"].sum()) == 6_662_611
    assert set(FEATURES).issubset(data.columns)
    assert not data[FEATURES].isna().any().any()


def test_temporal_split_and_model_quality():
    data = load_dataset(DATA_PATH)
    result = train_and_evaluate(data)
    assert len(result.x_train) == 7008
    assert len(result.x_test) == 1752
    assert result.metrics["r2"] > 0.50
    assert result.metrics["mae"] < result.metrics["baseline_mae"]


def test_single_prediction_is_non_negative_integer():
    data = load_dataset(DATA_PATH)
    result = train_and_evaluate(data)
    prediction = tahmin_et(
        result.model,
        mevsim=2,
        ay=7,
        saat=17,
        tatil=0,
        hafta_gunu=1,
        is_gunu=1,
        hava_durumu=1,
        sicaklik_c=28.0,
        nem_yuzde=45.0,
        ruzgar_kmh=12.0,
        yagis_mm=0.0,
    )
    assert isinstance(prediction, int)
    assert prediction >= 0


def test_interface_demand_levels():
    assert demand_level(200)[0] == "Düşük talep"
    assert demand_level(700)[0] == "Orta talep"
    assert demand_level(1_300)[0] == "Yüksek talep"

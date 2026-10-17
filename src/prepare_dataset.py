"""2025 Capital Bikeshare yolculuklarını saatlik hava verisiyle birleştirir."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile

import pandas as pd


BIKESHARE_URL = (
    "https://s3.amazonaws.com/capitalbikeshare-data/"
    "{year}{month:02d}-capitalbikeshare-tripdata.zip"
)
WEATHER_URL = (
    "https://archive-api.open-meteo.com/v1/archive?latitude=38.9072&longitude=-77.0369"
    "&start_date=2024-12-31&end_date=2026-01-01"
    "&hourly=temperature_2m%2Crelative_humidity_2m%2Cprecipitation%2Cweather_code%2Cwind_speed_10m"
    "&timezone=GMT&timeformat=unixtime&wind_speed_unit=kmh"
)
YEAR = 2025

FEDERAL_HOLIDAYS_2025 = {
    "2025-01-01",
    "2025-01-20",
    "2025-02-17",
    "2025-05-26",
    "2025-06-19",
    "2025-07-04",
    "2025-09-01",
    "2025-10-13",
    "2025-11-11",
    "2025-11-27",
    "2025-12-25",
}

OUTPUT_COLUMNS = [
    "tarih_saat",
    "tarih",
    "yil",
    "mevsim",
    "ay",
    "saat",
    "tatil",
    "hafta_gunu",
    "is_gunu",
    "hava_durumu",
    "sicaklik_c",
    "nem_yuzde",
    "ruzgar_kmh",
    "yagis_mm",
    "kiralama_sayisi",
]


def download_sources(raw_dir: Path, weather_path: Path) -> None:
    """Eksik aylık arşivleri ve hava verisini resmî kaynaklardan indirir."""

    raw_dir.mkdir(parents=True, exist_ok=True)
    weather_path.parent.mkdir(parents=True, exist_ok=True)
    for month in range(1, 13):
        target = raw_dir / f"{YEAR}{month:02d}-capitalbikeshare-tripdata.zip"
        if not target.exists():
            print(f"İndiriliyor: {target.name}")
            urlretrieve(BIKESHARE_URL.format(year=YEAR, month=month), target)
    if not weather_path.exists():
        print("İndiriliyor: Washington D.C. saatlik hava verisi")
        urlretrieve(WEATHER_URL, weather_path)


def _read_trip_start_times(zip_path: Path) -> pd.Series:
    with ZipFile(zip_path) as archive:
        csv_names = [
            name
            for name in archive.namelist()
            if name.endswith(".csv") and not name.startswith("__MACOSX/")
        ]
        if len(csv_names) != 1:
            raise ValueError(f"{zip_path.name} içinde tek bir CSV bekleniyordu.")
        with archive.open(csv_names[0]) as source:
            frame = pd.read_csv(source, usecols=["started_at"])
    return pd.to_datetime(frame["started_at"], errors="raise").dt.floor("h")


def _load_hourly_demand(raw_dir: Path) -> tuple[pd.Series, int]:
    archives = sorted(raw_dir.glob(f"{YEAR}??-capitalbikeshare-tripdata.zip"))
    if len(archives) != 12:
        raise FileNotFoundError(
            f"12 aylık arşiv bekleniyordu; {len(archives)} dosya bulundu. "
            "Eksikleri indirmek için --download kullanın."
        )

    monthly_counts: list[pd.Series] = []
    for archive in archives:
        starts = _read_trip_start_times(archive)
        monthly_counts.append(starts.value_counts())

    counts = pd.concat(monthly_counts, axis=1).fillna(0).sum(axis=1)
    counts.index = pd.DatetimeIndex(counts.index)
    counts = counts.groupby(level=0).sum().sort_index().astype("int64")
    counts = counts.loc[(counts.index >= f"{YEAR}-01-01") & (counts.index < f"{YEAR + 1}-01-01")]
    trip_count = int(counts.sum())
    return counts, trip_count


def _weather_category(code: int) -> int:
    if code <= 2:
        return 1
    if code in {3, 45, 48}:
        return 2
    if code < 95:
        return 3
    return 4


def _load_weather(weather_path: Path) -> pd.DataFrame:
    payload = json.loads(weather_path.read_text(encoding="utf-8"))
    hourly = pd.DataFrame(payload["hourly"])
    local_time = (
        pd.to_datetime(hourly.pop("time"), unit="s", utc=True)
        .dt.tz_convert("America/New_York")
        .dt.tz_localize(None)
        .dt.floor("h")
    )
    hourly.insert(0, "tarih_saat", local_time)
    hourly = hourly.groupby("tarih_saat", as_index=False).mean(numeric_only=True)
    return hourly.rename(
        columns={
            "temperature_2m": "sicaklik_c",
            "relative_humidity_2m": "nem_yuzde",
            "precipitation": "yagis_mm",
            "weather_code": "wmo_kodu",
            "wind_speed_10m": "ruzgar_kmh",
        }
    )


def _season(month: int) -> int:
    if month in {3, 4, 5}:
        return 1
    if month in {6, 7, 8}:
        return 2
    if month in {9, 10, 11}:
        return 3
    return 4


def prepare_dataset(raw_dir: Path, weather_path: Path, output_path: Path) -> pd.DataFrame:
    """Yolculuk başlangıçlarını sayar, hava verisini birleştirir ve CSV üretir."""

    demand, source_trip_count = _load_hourly_demand(raw_dir)
    calendar = pd.DataFrame(
        {
            "tarih_saat": pd.date_range(
                f"{YEAR}-01-01", f"{YEAR}-12-31 23:00:00", freq="h"
            )
        }
    )
    calendar["kiralama_sayisi"] = (
        calendar["tarih_saat"].map(demand).fillna(0).astype("int64")
    )

    weather = _load_weather(weather_path)
    prepared = calendar.merge(
        weather, on="tarih_saat", how="left", validate="one_to_one"
    )
    weather_columns = [
        "sicaklik_c",
        "nem_yuzde",
        "yagis_mm",
        "wmo_kodu",
        "ruzgar_kmh",
    ]
    prepared[weather_columns] = prepared[weather_columns].interpolate(
        limit_direction="both"
    )

    prepared["tarih"] = prepared["tarih_saat"].dt.strftime("%Y-%m-%d")
    prepared["yil"] = YEAR
    prepared["ay"] = prepared["tarih_saat"].dt.month
    prepared["saat"] = prepared["tarih_saat"].dt.hour
    prepared["hafta_gunu"] = prepared["tarih_saat"].dt.weekday
    prepared["mevsim"] = prepared["ay"].map(_season)
    prepared["tatil"] = prepared["tarih"].isin(FEDERAL_HOLIDAYS_2025).astype(int)
    prepared["is_gunu"] = (
        (prepared["hafta_gunu"] < 5) & (prepared["tatil"] == 0)
    ).astype(int)
    prepared["hava_durumu"] = (
        prepared["wmo_kodu"].round().astype(int).map(_weather_category)
    )
    prepared["tarih_saat"] = prepared["tarih_saat"].dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    prepared = prepared[OUTPUT_COLUMNS]

    if prepared.isna().any().any():
        raise ValueError("Hazırlanan veri setinde beklenmeyen eksik değer bulundu.")
    if len(prepared) != 8760:
        raise ValueError(f"2025 için 8.760 saat bekleniyordu; {len(prepared)} bulundu.")
    if int(prepared["kiralama_sayisi"].sum()) != source_trip_count:
        raise ValueError("Saatlik toplam, kaynak yolculuk sayısıyla eşleşmiyor.")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    prepared.to_csv(output_path, index=False)
    return prepared


def main() -> None:
    project_dir = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=project_dir / "data" / "source" / "raw",
    )
    parser.add_argument(
        "--weather-path",
        type=Path,
        default=project_dir
        / "data"
        / "source"
        / "washington_dc_hourly_2025.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=project_dir
        / "data"
        / "processed"
        / "sehrin_nabzi_bisiklet_talebi.csv",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Eksik kaynak dosyalarını indirir.",
    )
    args = parser.parse_args()

    if args.download:
        download_sources(args.raw_dir, args.weather_path)
    dataset = prepare_dataset(args.raw_dir, args.weather_path, args.output)
    print(f"CSV hazırlandı: {args.output}")
    print(f"Boyut: {dataset.shape[0]} satır x {dataset.shape[1]} sütun")
    print(f"Kaynak yolculuk: {int(dataset['kiralama_sayisi'].sum()):,}")
    print(f"Eksik değer: {int(dataset.isna().sum().sum())}")


if __name__ == "__main__":
    main()

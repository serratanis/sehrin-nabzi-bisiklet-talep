"""Komut satırında çalışan Şehrin Nabzı mini tahmin uygulaması."""

from __future__ import annotations

from pathlib import Path

import joblib

from sehrin_nabzi import tahmin_et, tahmini_yorumla


def read_int(prompt: str, minimum: int, maximum: int) -> int:
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Lütfen tam sayı girin.")
            continue
        if minimum <= value <= maximum:
            return value
        print(f"Değer {minimum} ile {maximum} arasında olmalı.")


def read_float(prompt: str, minimum: float = 0.0, maximum: float = 1.0) -> float:
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Lütfen sayısal bir değer girin.")
            continue
        if minimum <= value <= maximum:
            return value
        print(f"Değer {minimum} ile {maximum} arasında olmalı.")


def main() -> None:
    project_dir = Path(__file__).resolve().parents[1]
    model_path = project_dir / "assets" / "sehrin_nabzi_model.joblib"
    if not model_path.exists():
        raise FileNotFoundError(
            "Eğitilmiş model bulunamadı. Önce run_experiment.py dosyasını çalıştırın."
        )

    model = joblib.load(model_path)
    print("\nŞehrin Nabzı - Saatlik Bisiklet Talep Tahmini\n")
    prediction = tahmin_et(
        model,
        mevsim=read_int("Mevsim (1=ilkbahar, 2=yaz, 3=sonbahar, 4=kış): ", 1, 4),
        ay=read_int("Ay (1-12): ", 1, 12),
        saat=read_int("Saat (0-23): ", 0, 23),
        tatil=read_int("Tatil mi? (0=hayır, 1=evet): ", 0, 1),
        hafta_gunu=read_int("Haftanın günü (0=Pazartesi, 6=Pazar): ", 0, 6),
        is_gunu=read_int("İş günü mü? (0=hayır, 1=evet): ", 0, 1),
        hava_durumu=read_int("Hava durumu (1=iyi, 2=puslu, 3=yağışlı, 4=şiddetli): ", 1, 4),
        sicaklik_c=read_float("Sıcaklık (°C): ", -20.0, 50.0),
        nem_yuzde=read_float("Nem (%): ", 0.0, 100.0),
        ruzgar_kmh=read_float("Rüzgâr (km/sa): ", 0.0, 100.0),
        yagis_mm=read_float("Saatlik yağış (mm): ", 0.0, 100.0),
    )
    print("\n" + tahmini_yorumla(prediction))


if __name__ == "__main__":
    main()

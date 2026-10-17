"""Şehrin Nabzı — tarayıcı tabanlı bisiklet talep tahmin paneli."""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

from src.interface_helpers import demand_level
from src.sehrin_nabzi import tahmin_et


PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "assets" / "sehrin_nabzi_model.joblib"
DATA_PATH = PROJECT_DIR / "data" / "processed" / "sehrin_nabzi_bisiklet_talebi.csv"
METRICS_PATH = PROJECT_DIR / "assets" / "model_metrikleri.json"

MONTHS = {
    "Ocak": 1,
    "Şubat": 2,
    "Mart": 3,
    "Nisan": 4,
    "Mayıs": 5,
    "Haziran": 6,
    "Temmuz": 7,
    "Ağustos": 8,
    "Eylül": 9,
    "Ekim": 10,
    "Kasım": 11,
    "Aralık": 12,
}
WEEKDAYS = {
    "Pazartesi": 0,
    "Salı": 1,
    "Çarşamba": 2,
    "Perşembe": 3,
    "Cuma": 4,
    "Cumartesi": 5,
    "Pazar": 6,
}
WEATHER = {
    "Açık / parçalı bulutlu": 1,
    "Kapalı / sisli": 2,
    "Yağmur / kar": 3,
    "Gök gürültülü": 4,
}


def season_for_month(month: int) -> int:
    if month in {3, 4, 5}:
        return 1
    if month in {6, 7, 8}:
        return 2
    if month in {9, 10, 11}:
        return 3
    return 4


@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Eğitilmiş model bulunamadı. Önce src/run_experiment.py çalıştırılmalı."
        )
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


@st.cache_data
def load_metrics() -> dict[str, float | int | str]:
    return json.loads(METRICS_PATH.read_text(encoding="utf-8"))


def format_number(value: float, digits: int = 0) -> str:
    return f"{value:,.{digits}f}".replace(",", "X").replace(".", ",").replace("X", ".")


st.set_page_config(
    page_title="Şehrin Nabzı | Bisiklet Talep Tahmini",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 80% 0%, rgba(47,210,176,.15), transparent 30%),
            linear-gradient(145deg, #071725 0%, #0B2030 55%, #071725 100%);
    }
    [data-testid="stHeader"] { background: rgba(7,23,37,.72); }
    .block-container { max-width: 1180px; padding-top: 2.6rem; padding-bottom: 4rem; }
    .hero {
        padding: 2.2rem 2.4rem;
        border: 1px solid rgba(126, 231, 210, .22);
        border-radius: 28px;
        background: linear-gradient(135deg, rgba(16,41,59,.96), rgba(10,34,49,.78));
        box-shadow: 0 24px 70px rgba(0,0,0,.25);
        margin-bottom: 1.4rem;
    }
    .eyebrow {
        color: #72E2CC; font-weight: 750; letter-spacing: .16em;
        font-size: .72rem; margin-bottom: .7rem;
    }
    .hero h1 { font-size: clamp(2.1rem, 5vw, 4.2rem); line-height: .98; margin: 0; }
    .hero p { color: #B7C9D6; max-width: 720px; font-size: 1.02rem; margin: 1rem 0 0; }
    .result-card {
        padding: 1.65rem 1.8rem; border-radius: 24px;
        background: linear-gradient(135deg, rgba(47,210,176,.18), rgba(16,41,59,.98));
        border: 1px solid rgba(47,210,176,.48); min-height: 245px;
        display: flex; flex-direction: column; justify-content: center;
    }
    .result-label { color: #AFC4D1; font-size: .82rem; letter-spacing: .1em; font-weight: 700; }
    .result-number { color: #F8FCFE; font-size: 4.5rem; line-height: 1; font-weight: 800; margin: .55rem 0; }
    .result-unit { color: #AFC4D1; font-size: 1rem; }
    .status-pill {
        display: inline-block; padding: .4rem .8rem; border-radius: 999px;
        font-weight: 750; margin: .85rem 0 .55rem; width: fit-content;
    }
    .insight-card {
        background: rgba(16,41,59,.72); border: 1px solid rgba(255,255,255,.08);
        border-radius: 20px; padding: 1.25rem 1.4rem; min-height: 132px;
    }
    .insight-card strong { color: #F7FBFD; font-size: 1.05rem; }
    .insight-card p { color: #AFC4D1; margin: .45rem 0 0; font-size: .92rem; }
    div[data-testid="stMetric"] {
        background: rgba(16,41,59,.68); border: 1px solid rgba(255,255,255,.08);
        padding: 1rem 1.1rem; border-radius: 18px;
    }
    div[data-testid="stForm"] {
        background: rgba(11,32,48,.68); border: 1px solid rgba(255,255,255,.08);
        padding: 1.2rem 1.3rem; border-radius: 22px;
    }
    .method-note { color: #AFC4D1; font-size: .86rem; }
    .footer { color: #7892A3; font-size: .78rem; text-align: center; padding-top: 2.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
      <div class="eyebrow">AI-DESTEKLİ KENTSEL HAREKETLİLİK</div>
      <h1>Şehrin Nabzı</h1>
      <p>Saat, takvim ve hava koşullarını seçin; açıklanabilir makine öğrenmesi modeli
      Washington D.C. bisiklet paylaşım sisteminin saatlik talebini anında tahmin etsin.
      Model, 2025'in 6,6 milyon yolculuğundan öğrenmiştir.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

model = load_model()
data = load_data()
metrics = load_metrics()

tab_prediction, tab_analysis, tab_model = st.tabs(
    ["⚡ Talep tahmini", "📊 Veri hikâyesi", "🧠 Model kartı"]
)

with tab_prediction:
    input_col, result_col = st.columns([1.38, 1], gap="large")

    with input_col:
        st.subheader("Koşulları belirleyin")
        with st.form("prediction_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                month_name = st.selectbox("Ay", list(MONTHS), index=6)
                hour = st.slider("Saat", 0, 23, 17)
                weekday_name = st.selectbox("Gün", list(WEEKDAYS), index=1)
                weather_name = st.selectbox("Hava durumu", list(WEATHER), index=0)
            with col_b:
                temperature = st.slider("Sıcaklık (°C)", -10, 42, 28)
                humidity = st.slider("Nem (%)", 0, 100, 45)
                wind = st.slider("Rüzgâr (km/sa)", 0, 70, 12)
                precipitation = st.slider("Saatlik yağış (mm)", 0.0, 20.0, 0.0, 0.1)
                holiday = st.toggle("Resmî tatil", value=False)
            submitted = st.form_submit_button(
                "Talebi tahmin et",
                type="primary",
                width="stretch",
            )

    month = MONTHS[month_name]
    season = season_for_month(month)
    weekday = WEEKDAYS[weekday_name]
    weather = WEATHER[weather_name]
    is_workday = int(not holiday and weekday < 5)
    prediction = tahmin_et(
        model,
        mevsim=season,
        ay=month,
        saat=hour,
        tatil=int(holiday),
        hafta_gunu=weekday,
        is_gunu=is_workday,
        hava_durumu=weather,
        sicaklik_c=float(temperature),
        nem_yuzde=float(humidity),
        ruzgar_kmh=float(wind),
        yagis_mm=float(precipitation),
    )
    level, level_color, recommendation = demand_level(prediction)
    typical_hour = float(data.groupby("saat")["kiralama_sayisi"].mean().loc[hour])
    difference = prediction - typical_hour

    with result_col:
        st.subheader("Tahmin sonucu")
        st.markdown(
            f"""
            <section class="result-card">
              <div class="result-label">BEKLENEN SAATLİK TALEP</div>
              <div class="result-number">{format_number(prediction)}</div>
              <div class="result-unit">yolculuk başlangıcı</div>
              <div class="status-pill" style="background:{level_color}22;color:{level_color};border:1px solid {level_color}66;">
                {level}
              </div>
              <div class="method-note">{recommendation}</div>
            </section>
            """,
            unsafe_allow_html=True,
        )
        st.progress(min(prediction / 2_500, 1.0), text="2.500 yolculukluk yoğun saat referansına göre")
        if submitted:
            st.toast("Tahmin güncellendi", icon="🚲")

    st.write("")
    metric_a, metric_b, metric_c = st.columns(3)
    metric_a.metric("Seçilen saat", f"{hour:02d}:00")
    metric_b.metric("Bu saatin veri ortalaması", format_number(typical_hour))
    metric_c.metric(
        "Ortalamadan fark",
        format_number(abs(difference)),
        delta=f"{'+' if difference >= 0 else '-'}%{abs(difference / typical_hour * 100):.0f}",
    )

with tab_analysis:
    st.subheader("Veri, şehrin hareket ritmini gösteriyor")
    st.caption("8.760 saatlik gözlem · 6.662.611 yolculuk · Washington D.C. · 2025")
    image_a, image_b = st.columns(2, gap="large")
    with image_a:
        st.image(PROJECT_DIR / "assets" / "01_saatlik_talep.png", width="stretch")
    with image_b:
        st.image(PROJECT_DIR / "assets" / "02_hava_durumu_talebi.png", width="stretch")

    insight_a, insight_b, insight_c = st.columns(3)
    with insight_a:
        st.markdown(
            "<div class='insight-card'><strong>17.00 zirvesi</strong><p>İş çıkışı saati ortalama 1.810 yolculukla günün en yüksek talebini oluşturuyor.</p></div>",
            unsafe_allow_html=True,
        )
    with insight_b:
        st.markdown(
            "<div class='insight-card'><strong>Yaz talebi</strong><p>Haziran ayı ortalaması 960 yolculukla yılın en yüksek aylık düzeyine ulaşıyor.</p></div>",
            unsafe_allow_html=True,
        )
    with insight_c:
        st.markdown(
            "<div class='insight-card'><strong>Güncel veri</strong><p>Model, 2025'in tamamını kapsayan resmî yolculuk ve saatlik hava kayıtlarını kullanıyor.</p></div>",
            unsafe_allow_html=True,
        )

    with st.expander("İşlenmiş veriden örnek satırları incele"):
        st.dataframe(data.head(50), width="stretch", hide_index=True)

with tab_model:
    st.subheader("Açıklanabilir ve dürüst bir başlangıç modeli")
    metric_1, metric_2, metric_3, metric_4 = st.columns(4)
    metric_1.metric("R²", format_number(float(metrics["r2"]), 3))
    metric_2.metric("MAE", format_number(float(metrics["mae"]), 1))
    metric_3.metric("RMSE", format_number(float(metrics["rmse"]), 1))
    improvement = 1 - float(metrics["mae"]) / float(metrics["baseline_mae"])
    metric_4.metric(
        "Temel yaklaşım MAE",
        format_number(float(metrics["baseline_mae"]), 1),
        delta=f"%{improvement * 100:.1f} daha düşük hata",
    )

    left, right = st.columns(2, gap="large")
    with left:
        st.markdown("#### Model yaklaşımı")
        st.markdown(
            """
            - Kategorik değişkenler **one-hot encoding** ile dönüştürülür.
            - Açıklanabilir bir **Linear Regression** modeli kullanılır.
            - Eğitim ve test ayrımında zaman sırası korunur.
            - İlk %80 eğitim, son %20 test verisidir.
            """
        )
    with right:
        st.markdown("#### Güvenilirlik sınırı")
        st.markdown(
            """
            - Model tek bir şehrin 2025 davranışlarını temsil eder.
            - İstasyon kapasitesi ve özel etkinlik bilgisi bulunmaz.
            - Sonuç operasyonel bir **karar desteğidir**, kesin talep değildir.
            - Üye türü ve istasyon kimliği tahmin anında bilinmediği için modele alınmaz.
            """
        )
    st.image(PROJECT_DIR / "assets" / "04_gercek_tahmin.png", width="stretch")

st.markdown(
    """
    <div class='footer'>Şehrin Nabzı · Capital Bikeshare 2025 Sistem Verisi ·
    Open-Meteo ERA5 Hava Verisi · Eğitim ve portföy projesi</div>
    """,
    unsafe_allow_html=True,
)

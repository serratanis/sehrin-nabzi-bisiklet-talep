# Şehrin Nabzı

Şehrin Nabzı, Washington D.C. bisiklet paylaşım sisteminin saatlik talebini takvim ve hava koşullarından tahmin eden uçtan uca bir Python projesidir. Model, Capital Bikeshare'ın 2025 yılında yayımladığı 6.662.611 yolculuk kaydının saatlik toplamları ile Open-Meteo hava verisini kullanır.

## Sonuç

Zaman sırası korunarak ayrılan test döneminde model R² 0,578 ve MAE 234,3 üretti. Yalnızca eğitim ortalamasını kullanan temel yaklaşımın MAE değeri 476,8 oldu. Doğrusal model, temel yaklaşıma göre hatayı yüzde 50,9 azalttı.

## Tarayıcıda açma

macOS'ta terminal komutu yazmadan çalıştırmak için `SEHRIN_NABZI_BASLAT.command` dosyasına çift tıklayın. Uygulama tarayıcıda açılır. Kapatmak için `SEHRIN_NABZI_DURDUR.command` dosyasına çift tıklayın.

Terminalden başlatmak isterseniz:

```bash
python -m streamlit run app.py
```

## Kurulum ve doğrulama

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/run_experiment.py
python -m pytest -q
```

İşlenmiş CSV teslim paketinde hazırdır. Ham veriden yeniden üretmek için internet bağlantısıyla:

```bash
python src/prepare_dataset.py --download
```

## Proje yapısı

- `app.py`: görsel tahmin paneli
- `data/processed`: 2025'e ait 8.760 saatlik model verisi
- `src`: veri hazırlama, model eğitimi ve mini uygulama
- `notebooks`: çalıştırılmış Colab uyumlu not defteri
- `assets`: grafikler, metrikler, örnek tahminler ve eğitilmiş model
- `reports`: bir sayfalık proje raporu
- `presentation`: beş slaytlık sunum
- `tests`: veri, model ve arayüz yardımcıları için otomatik testler

## Veri kaynakları

- Capital Bikeshare System Data: https://capitalbikeshare.com/system-data
- Capital Bikeshare Data License Agreement: https://capitalbikeshare.com/data-license-agreement
- Open-Meteo Historical Weather API: https://open-meteo.com/en/docs/historical-weather-api

Ham yolculuk dosyaları lisans koşulları nedeniyle teslim paketinde yeniden dağıtılmaz. Proje, analiz için üretilmiş saatlik toplamları içerir.

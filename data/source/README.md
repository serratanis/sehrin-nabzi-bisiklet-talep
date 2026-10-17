# Ham veri kaynakları

Bu klasör ham yolculuk arşivlerini içermez. Capital Bikeshare lisansı, ham verinin bağımsız bir veri seti olarak yeniden dağıtımını sınırlar. İşlenmiş saatlik toplamlar `data/processed` klasöründedir.

Veriyi yeniden üretmek için internet bağlantısıyla proje kökünde şu komutu çalıştırın:

```bash
python src/prepare_dataset.py --download
```

Kaynaklar:

- Capital Bikeshare System Data: https://capitalbikeshare.com/system-data
- Capital Bikeshare Data License Agreement: https://capitalbikeshare.com/data-license-agreement
- Open-Meteo Historical Weather API: https://open-meteo.com/en/docs/historical-weather-api

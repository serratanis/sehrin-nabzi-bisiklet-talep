# Kalite Denetimi

## Yönerge uyumu

Basitleştirilmiş Python proje yönergesindeki yedi aşama `DELIVERY_CHECKLIST.md` içinde tek tek eşleştirildi.

## Teknik doğrulama

- Veri dönemi: 1 Ocak-31 Aralık 2025
- Saatlik satır: 8.760
- Kaynak yolculuk: 6.662.611
- İşlenmiş sütun: 15
- Eksik değer: 0
- Otomatik test: 4 başarılı
- Eğitim satırı: 7.008
- Test satırı: 1.752
- R²: 0,578
- MAE: 234,3
- RMSE: 315,2
- Temel yaklaşım MAE: 476,8

## Risk denetimi

- Yolculuk kimliği, kullanıcı türü ve istasyon alanları modele alınmadı.
- Test verisi zaman sırasının son yüzde 20'sinden seçildi.
- Negatif ham tahmin sıfıra kırpılır ve model kartında açıklanır.
- Arayüz kullanıcıdan doğrudan anlaşılır birimlerle °C, yüzde, km/sa ve mm girdisi alır.
- Sonuçlar farklı bir şehir veya yıl için genellenebilir kabul edilmedi.
- Ham Capital Bikeshare arşivleri veri lisansı nedeniyle teslim paketinde dağıtılmadı.

## Teslim öncesi kalan dış işlemler

- Colab not defteri Google Drive hesabına yüklenebilir.
- GitHub deposu public yapılabilir.
- Yayın bağlantıları teslim formuna eklenebilir.

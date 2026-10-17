# Veri Kaynakları ve Kullanım Koşulları

## Capital Bikeshare

- Sistem verisi: https://capitalbikeshare.com/system-data
- Lisans: https://capitalbikeshare.com/data-license-agreement
- Kullanılan dönem: Ocak-Aralık 2025
- Analize giren yolculuk: 6.662.611

Capital Bikeshare lisansı veriyi erişme, çoğaltma, analiz etme, değiştirme ve bir ürün ya da hizmet içinde kullanma izni verir. Ham verinin bağımsız bir veri seti olarak yeniden dağıtılması kısıtlıdır. Bu nedenle teslim paketi aylık ham arşivleri içermez; yalnızca proje analizi için üretilen saatlik toplamları içerir. Proje Capital Bikeshare ile bağlantı veya onay iddiasında bulunmaz.

## Open-Meteo

- Historical Weather API: https://open-meteo.com/en/docs/historical-weather-api
- Konum: Washington D.C., 38.9072, -77.0369
- Kullanılan alanlar: sıcaklık, bağıl nem, yağış, WMO hava kodu ve rüzgâr hızı
- Lisans: Creative Commons Attribution 4.0

## Dönüşüm

Yolculuk başlangıç zamanları saate yuvarlandı ve sayıldı. Ocak arşivindeki 31 Aralık 2024 zaman damgalı 36 kayıt, proje kapsamı 2025 olduğu için çıkarıldı. Hava verisi aynı saat anahtarında birleştirildi. Takvim alanları üretildi; ham yolculuk kimliği, kullanıcı türü, koordinatlar ve istasyon kimlikleri işlenmiş CSV'ye alınmadı.

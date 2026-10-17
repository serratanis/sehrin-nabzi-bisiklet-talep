# Veri Sözlüğü

Kaynaklar: Capital Bikeshare 2025 aylık yolculuk geçmişi ve Open-Meteo Historical Weather API.

| Sütun | Tip | Anlam | Modelde kullanım |
| --- | --- | --- | --- |
| tarih_saat | tarih saat | Saatlik gözlemin başlangıcı | Hayır, zaman ayrımı ve izlenebilirlik için |
| tarih | tarih | Gözlemin takvim tarihi | Hayır |
| yil | sayısal | Gözlem yılı, tüm satırlarda 2025 | Hayır |
| mevsim | kategorik | 1 ilkbahar, 2 yaz, 3 sonbahar, 4 kış | Evet |
| ay | kategorik | 1 ile 12 arasında ay | Evet |
| saat | kategorik | 0 ile 23 arasında saat | Evet |
| tatil | ikili | ABD federal tatiliyse 1 | Evet |
| hafta_gunu | kategorik | 0 Pazartesi ile 6 Pazar arasında | Evet |
| is_gunu | ikili | Hafta içi ve federal tatil değilse 1 | Evet |
| hava_durumu | kategorik | 1 açık, 2 kapalı veya sisli, 3 yağışlı, 4 gök gürültülü | Evet |
| sicaklik_c | sayısal | İki metre sıcaklığı, Celsius | Evet |
| nem_yuzde | sayısal | Bağıl nem, yüzde | Evet |
| ruzgar_kmh | sayısal | On metre rüzgâr hızı, km/sa | Evet |
| yagis_mm | sayısal | Saatlik yağış, milimetre | Evet |
| kiralama_sayisi | sayısal | O saatte başlayan yolculuk sayısı | Hedef |

## Veri hazırlama kontrolü

On iki aylık yolculuk arşivindeki `started_at` zamanları saat düzeyine indirgenip sayıldı. Ocak arşivinde yer aldığı hâlde zaman damgası 31 Aralık 2024 olan 36 kayıt, 2025 kapsamı dışında bırakıldı. 2025'in 8.760 saati eksiksiz bir takvimle eşleştirildi. Hava verisi Washington D.C. koordinatları için saatlik olarak birleştirildi. 2025 yolculuk toplamı 6.662.611'dir ve işlenmiş hedef toplamı kaynakla eşleşir. Yolculuk kimliği, kullanıcı türü ve istasyon bilgileri tahmin anında bilinmeyeceği için modele alınmadı.

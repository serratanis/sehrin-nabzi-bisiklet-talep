# Şehrin Nabzı Saatlik Bisiklet Paylaşım Talebi Tahmini

## Problem ve amaç

Bu proje, ay, saat, haftanın günü ve hava koşullarından Washington D.C. Capital Bikeshare sistemindeki saatlik yolculuk başlangıcı sayısını tahmin eder. Sonuç, bisikletlerin istasyonlar arasında taşınması ve yoğun saatler için ekip planı gibi operasyon kararlarını destekleyebilir. Tahmin tek başına karar değildir; 2025 kullanım verisinden üretilen bir planlama sinyalidir.

## Veri ve hazırlık

Capital Bikeshare'ın 2025 boyunca yayımladığı 6.662.611 yolculuk kaydı saatlik toplamlar hâline getirildi. Bu toplamlar, Open-Meteo Historical Weather API'den alınan Washington D.C. sıcaklık, nem, rüzgâr, yağış ve hava kodlarıyla birleştirildi. İşlenmiş veri 8.760 saat ve 15 sütun içerir; eksik değer yoktur. Yolculuk kimliği, kullanıcı türü ve istasyon alanları tahmin anında bilinmediği için modele alınmadı.

## Keşif bulguları

Ortalama talep saat 17.00'de 1.810 yolculukla zirveye çıktı. Haziran ayı saatlik ortalaması 960 ile yılın en yüksek aylık düzeyine ulaştı. Sıcaklık ile talep arasında 0,478 düzeyinde pozitif, nem ile talep arasında -0,426 düzeyinde negatif ilişki görüldü. Bu ilişkiler tek başına neden sonuç göstermez; saat ve mevsim etkileriyle birlikte yorumlanmalıdır.

## Model ve değerlendirme

Yönergeye uygun olarak Linear Regression kullanıldı. Kategorik değişkenler one-hot encoding ile dönüştürüldü, sayısal değişkenler ölçeklendi. Verinin ilk yüzde 80'i eğitim, son yüzde 20'si test için ayrıldı ve zaman sırası karıştırılmadı. Model test döneminde R² 0,578, MAE 234,3 ve RMSE 315,2 üretti. Yalnızca eğitim ortalamasını tahmin eden temel yaklaşımın MAE değeri 476,8 oldu. Model, temel yaklaşıma göre mutlak hatayı yüzde 50,9 azalttı.

## Sonuç ve geliştirme alanları

Model, güncel ve tam yıllık bir veri seti üzerinde açıklanabilir bir başlangıç çözümü sunuyor. Bununla birlikte istasyon kapasitesi, özel etkinlik, toplu taşıma kesintisi ve mekânsal dağılım bilgilerini kullanmıyor. Gelecek sürümde bu alanlar eklenebilir; doğrusal model bir ağaç tabanlı yöntemle aynı ileri tarihli test döneminde karşılaştırılabilir.

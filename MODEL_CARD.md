# Model Kartı

## Amaç

Washington D.C. Capital Bikeshare sistemindeki saatlik yolculuk başlangıcı sayısını takvim ve hava koşullarından tahmin etmek.

## Model

`LinearRegression`. Kategorik değişkenler `OneHotEncoder` ile kodlandı, sayısal değişkenler `StandardScaler` ile ölçeklendi. Doğrusal modelin açıklanabilir olması ve eğitim yönergesindeki regresyon yaklaşımını göstermesi seçimde belirleyici oldu.

## Eğitim ve test düzeni

- Toplam gözlem: 8.760 saat
- Kaynak yolculuk: 6.662.611
- Eğitim: ilk 7.008 saat, 1 Ocak-19 Ekim 2025
- Test: son 1.752 saat, 20 Ekim-31 Aralık 2025
- Bölme: yüzde 80 eğitim, yüzde 20 test
- Zaman sırası korundu, karıştırma yapılmadı

## Sonuçlar

- R²: 0,578
- MAE: 234,3 yolculuk
- RMSE: 315,2 yolculuk
- Eğitim ortalaması temel yaklaşımı MAE: 476,8 yolculuk
- Temel yaklaşıma göre MAE azalması: yüzde 50,9

## Güçlü yönler

- Güncel ve tam yıllık 2025 verisini kullanır.
- Rastgele bölmeye göre daha zor olan ileri tarihli test dönemini kullanır.
- Saat ve ay gibi kategorileri doğrusal sıra olarak yorumlamaz.
- Yalnızca tahmin anında bilinebilecek takvim ve hava değişkenlerini kullanır.

## Sınırlılıklar

- İstasyon konumu, kapasite, özel etkinlik ve toplu taşıma kesintisi bilgisi yoktur.
- Doğrusal model, hava ve saat arasındaki karmaşık etkileşimleri sınırlı öğrenir.
- Veri yalnızca Washington D.C. ve 2025 dönemini temsil eder.
- Negatif ham tahminler kullanıcı çıktısında sıfıra kırpılır.

## Uygun kullanım

Operasyon planlaması için ön tahmin, senaryo karşılaştırması ve eğitim amaçlı analiz.

## Uygun olmayan kullanım

Tek başına personel, filo veya yatırım kararı vermek. Başka şehirlerde yeniden doğrulama yapmadan kullanmak.

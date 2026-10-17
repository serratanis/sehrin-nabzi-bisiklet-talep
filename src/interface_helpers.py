"""Şehrin Nabzı web arayüzünde kullanılan saf yardımcı işlevler."""

from __future__ import annotations


def demand_level(prediction: int) -> tuple[str, str, str]:
    """Tahmini talebi sunum etiketi, renk ve operasyon önerisine dönüştürür."""

    if prediction < 350:
        return (
            "Düşük talep",
            "#68D5C8",
            "Standart kapasite yeterli; bisikletleri yoğun saatler için koruyun.",
        )
    if prediction < 1_000:
        return (
            "Orta talep",
            "#F2C14E",
            "İstasyon doluluklarını izleyin ve dengeleme ekibini hazır tutun.",
        )
    return (
        "Yüksek talep",
        "#FF7A59",
        "Yoğunluk öncesi bisiklet ve boş park noktası kapasitesini artırın.",
    )

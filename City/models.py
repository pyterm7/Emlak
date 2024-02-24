from django.db import models



class City(models.Model): 
    cities = [ "Bakı", "Gence", "Sumqayıt",
        "Lənkəran", "Mingəçevir", "Naxçıvan", "Şəki", "Şirvan", "Yevlax", "Xankəndi",
        "Naftalan", "Xocalı", "Şuşa", "Quba", "Qusar", "Qəbələ", "Ağdam", "Fizuli", "Zaqatala", "Balakən",
        "İmişli", "Göygöl", "Salyan", "Qazax", "Ağdaş", "İsmayıllı", "Bərdə", "Saatlı", "Ağstafa", "Ağsu",
        "Xaçmaz", "Tovuz", "Ucar", "Daskəsən", "Gədəbəy", "Göyçay", "Astara", "Şəmkir", "Ağcabədi", "Qax",
        "Zərdab", "Qobustan", "Şamaxı", "Siyəzən", "Sabirabad", "Kürdəmir", "Beyləqan", "Cəlilabad", "Xızı",
        "Yardımlı", "Lerik", "Masallı", "Neftçala", "Oğuz", "Samux", "Tərtər", "Goranboy",
        "Biləsuvar", "Hacıqabul", "Abşeron", "Xaçmaz", "Laçın", "Kəlbəcər", "Qazax", "Quba", "Qusar", ]
    name = models.CharField(max_length = 50) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str: return self.name 
    class Meta: verbose_name_plural = "Şəhərlər"



class Region(models.Model): 
    # Bakı rayonları
    regions = [
        "Binəqədi Rayonu", "Qaradağ Rayonu", "Xətai Rayonu",
        "Xəzər Rayonu", "Nərimanov Rayonu", "Nəsimi Rayonu",
        "Nizami Rayonu", "Pirallahı Rayonu", "Səbail Rayonu",
        "Sabunçu Rayonu", "Suraxanı Rayonu", "Yasamal Rayonu", 
        ]
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Şəhər", blank=True, null=True)
    name = models.CharField(max_length = 50) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str: return self.name 
    class Meta: verbose_name_plural = "Rayonlar"

class Village(models.Model):
    # Bakı kəndləri
    villages = [
        "Buzovna", "Mərdəkan", "Maştağa", "Bilgəh", "Nardaran",
        "Pirşağı", "Qala", "Zabrat", "Ramana",
        "Balaxanı", "Şüvəlan", "Türkan", "Əmircan", "Keşlə", "Fatmai",
        ]
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Şəhər / Rayon", blank=True, null=True)
    name = models.CharField(max_length = 50) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str: return self.name 
    class Meta: verbose_name_plural = "Kəndlər"
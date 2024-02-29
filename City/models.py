from django.db import models



class City(models.Model): 
    """
        1.First Step
        for c in City.cities:
            City.objects.create(name=c)
    """
    cities = [ "Bakı", "Gəncə", "Sumqayıt",
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
    name = models.CharField(max_length = 50, verbose_name="Rayon adı") 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str: return self.name 
    class Meta: verbose_name_plural = "Rayonlar"


class ZoneForBaku(models.Model):
    # For Baku
    zone_list = {
        "Binəqədi Rayonu": [ "2-ci Alatava","28 May","6-cı mikrorayon","7-ci mikrorayon","8-ci mikrorayon","9-cu mikrorayon","Biləcəri","Binəqədi","Xocasən","Xutor","M.Ə.Rəsulzadə","Sulutəpə"],
        "Qaradağ Rayonu": ["Ələt","Quzildaş","Qobustan","Lökbatan","Müşfiqabad","Puta","Sahil","Səngəçal","Şubanı"],
        "Xətai Rayonu": ["Ağ şəhər", "Əhmədli", "Həzi Aslanov", "Köhnə Günəşli", "NZS"],
        "Xəzər Rayonu": ["Binə","Buzovna","Dübəndi","Gürgən","Qala","Mərdəkan","Şağan","Şimal DRES","Şüvəlan","Türkan","Zirə"], 
        "Nərimanov Rayonu":["Böyükşor"], 
        "Nəsimi Rayonu":["1-ci mikrorayon","2-ci mikrorayon","3-cü mikrorayon","4-cü mikrorayon","5-ci mikrorayon","Kubinka"],
        "Nizami Rayonu": ["8-ci mikrayon","Keşlə"],
        "Pirallahı Rayonu":[],
        "Səbail Rayonu":["20-ci sahə","Badamdar","Bayıl","Bibi Heybət","Şıxov"],
        "Sabunçu Rayonu":["Albalılıq","Bakıxanov","Balaxanı","Bilgəh","Kürdəxanı","Maştağa","Nardaran","Pirşağı","Ramana","Sabunçu","Savalan","Yeni Balaxanı","Yeni Ramana","Zabrat"], 
        "Suraxanı Rayonu":["Bahar","Bülbülə","Dədə Qorqud","Əmircan","Günəşli","Hövsan","Qaraçuxur","Massiv A","Massiv B","Massiv D","Massiv G","Massiv V","Suraxanı","Şərq","Yeni Günəşli","Yeni Suraxanı","Zığ"], 
        "Yasamal Rayonu":["Yasamal","Yeni Yasamal"]
    }
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Rayon")
    name = models.CharField(max_length = 50, verbose_name="Qəsəbə və ya bölgə adı")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str: return self.name 
    class Meta: verbose_name_plural = "Qəsəbələr və ya Bölgələr"

    @staticmethod
    def CreateZoneForBaku():
        regions = Region.objects.all()
        for r in regions:
            r_zones =  ZoneForBaku.zone_list
            for r_zone in r_zones[f"{r.name}"]:
                ZoneForBaku.objects.create(name=r_zone, region=r)

class ZoneForAbsheron(models.Model):
    # For Absheron
    zone_list = ["Aşağı Güzdək", "Ceyranbatan", "Çiçək", "Fatmayı", "Görədil", "Köhnə Corat", "Qobu", "Masazır","Mehdiabad","Məmmədli","Novxanı","Pirəkəşkül","Yeni Corat","Zuğulba","Saray",]
    name = models.CharField(max_length = 50, verbose_name="Bölgə adı")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str: return self.name 
    class Meta: verbose_name_plural = "Abşeron bölgələri"

    @staticmethod
    def CreateZoneForAbsheron():
        for zone in ZoneForAbsheron.zone_list:
            ZoneForAbsheron.objects.create(name=zone)

from typing import Iterable
from django.db import models
from Auth.models import CustomUser
from Category.models import CategoryModel
from django.core.validators import MinValueValidator, MaxValueValidator
from string import ascii_lowercase

class AnnouncementModel(models.Model):
    ch = (("DOLLAR", "DOLLAR"), ("MANAT", "MANAT"))
    
    picture = models.ImageField(blank=True, null=True, verbose_name="Əsas şəkil", upload_to='AnnouncementMainPics/')

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Elan sahibi")
    type_of = models.BooleanField(default=False, verbose_name="Elan növu") # Default Satış
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, verbose_name="Kateqoriya")

    title = models.CharField(max_length = 225, verbose_name = "Başlıq")

    currency = models.CharField(choices = ch, default="MANAT", max_length = 10, verbose_name = "Valyuta")
    price = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(1000000)], verbose_name="Qiymət")
    the_initial_payment = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(1000000)], verbose_name="İlkin ödəniş")

    description = models.TextField(verbose_name="Açıqlama")

    room_count = models.SmallIntegerField(verbose_name="Otaq sayı")
    area = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(1000000)], verbose_name="Sahə")

    slug = models.CharField(max_length=255, verbose_name="SLUG", blank=True, null=True)

    has_internet = models.BooleanField(default=False, verbose_name="İnternet qoşulub")
    has_gas = models.BooleanField(default=False, verbose_name="Qaz çəkilib")
    has_electricity = models.BooleanField(default=False, verbose_name="Elektriklı təchiz olunub")
    has_water = models.BooleanField(default=False, verbose_name="Su çəkilib")
    has_water_tank = models.BooleanField(default=False, verbose_name="Əlavə su çəni var")
    has_combi = models.BooleanField(default=False, verbose_name="Kombi var") 
    has_elevator = models.BooleanField(default=False, verbose_name="Lift var")
    renovated = models.BooleanField(default=False, verbose_name="Təmirlidir") 
    furnished = models.BooleanField(default=False, verbose_name="Əşyalıdır")
    is_active = models.BooleanField(default=False, verbose_name="Elan aktivdir")

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs) -> None:
        new_slug = ""
        self.slug = self.title.lower().replace("ü", "u").replace("ç", "c").replace("ş", "s").replace("ğ","g").replace("ö","o").replace("ı", "i").replace("ə", "e").replace(" ", "-")
        for letter in self.slug:
            if letter in f"{ascii_lowercase}0123456789-":
                new_slug += letter 
        self.slug = new_slug.strip("-")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name_plural = "Elanlar"


class AnnouncementPics(models.Model):
    img = models.ImageField(upload_to="AnnouncementPics/", verbose_name="Şəkil")
    announcement = models.ForeignKey(AnnouncementModel, on_delete=models.CASCADE, verbose_name="Elan")

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str: return self.announcement.title 

    class Meta: verbose_name_plural = "Elan şəkilləri"
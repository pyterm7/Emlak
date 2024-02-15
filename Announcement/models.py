from django.db import models
from Auth.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator
from Category.models import CategoryModel

class AnnouncementModel(models.Model):
    ch = (("DOLLAR", "DOLLAR"), ("MANAT", "MANAT"))

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Elan sahibi")
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, verbose_name="Kateqoriya")

    picture = models.ImageField(blank=True, null=True, verbose_name="Əsas şəkil", upload_to='announcement/')
    title = models.CharField(max_length = 225, verbose_name = "Başlıq")

    currency = models.CharField(choices = ch, default="MANAT", max_length = 10, verbose_name = "Valyuta")
    price = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(1000000)], verbose_name="Qiymət")

    description = models.TextField(verbose_name="Açıqlama")

    room_count = models.SmallIntegerField(verbose_name="Otaq sayı")
    area = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(1000000)], verbose_name="Sahə")

    has_internet = models.BooleanField(default=False, verbose_name="İnterneti var")
    

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name_plural = "Elanlar"
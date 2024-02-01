from django.db import models
from tinymce.models import HTMLField

class About(models.Model):

    meta_author = "Mushvig Shukurov"
    meta_description = models.TextField(verbose_name = "Meta açıqlama")
    meta_keywords = models.TextField(verbose_name = "Meta açar sözlər")

    image = models.ImageField(blank=True, null=True, upload_to="about/", verbose_name="Haqqımızda səhifəsi üçün şəkil")
    experience_year = models.SmallIntegerField(verbose_name = "Təcrübə ili")
    title = models.CharField(max_length = 50, verbose_name = "Başlıq")
    subtitle = models.CharField(max_length = 50, verbose_name = "Alt başlıq")

    location = models.CharField(max_length = 225, verbose_name="Ünvan")

    description = HTMLField(verbose_name="Haqqımızda məlumat") 
    short_description = models.TextField(verbose_name="Qısa məlumat") 

    phone = models.CharField(max_length = 20, verbose_name="Telefon 1")
    phone_2 = models.CharField(max_length = 20, verbose_name="Telefon 2")

    email = models.EmailField(verbose_name="E-poçt 1")
    email_2 = models.EmailField(verbose_name="E-poçt 2")

    usage_ruler = HTMLField(verbose_name = "İstifadə qaydası")
    terms_and_conditions = HTMLField(verbose_name = "Qaydalar və şərtlər")

    facebook = models.CharField(max_length = 225, verbose_name = "Facebook", blank=True, null=True)
    instagram = models.CharField(max_length = 225, verbose_name = "İnstagram", blank=True, null=True)
    youtube = models.CharField(max_length = 225, verbose_name = "YouTube", blank=True, null=True)
    twitter = models.CharField(max_length = 225, verbose_name = "Twitter", blank=True, null=True)
    tiktok = models.CharField(max_length = 225, verbose_name = "TikTok", blank=True, null=True)
    vimeo = models.CharField(max_length = 225, verbose_name = "Vimeo", blank=True, null=True)
    pinterest = models.CharField(max_length = 225, verbose_name = "Pinterest", blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str: return self.title
    class Meta: verbose_name_plural = "Haqqımızda"


from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length = 50, verbose_name = "Ad")
    surname = models.CharField(max_length = 50, verbose_name = "Soyad")
    message = models.TextField(blank = True, null = True, verbose_name = "Mesaj")

    show = models.BooleanField(default=False, verbose_name = "Saytda görülsün")

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return self.name + " " + self.surname
    
    class Meta:
        verbose_name_plural = "Rəylər"
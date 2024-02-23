from django.db import models



class City(models.Model): 
    name = models.CharField(max_length = 50) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str: return self.name 
    class Meta: verbose_name_plural = "Şəhərlər"



class Region(models.Model): 
    name = models.CharField(max_length = 50) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str: return self.name 
    class Meta: verbose_name_plural = "Rayonlar"
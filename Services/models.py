from django.db import models

class Service(models.Model):
    title = models.CharField(max_length=225, verbose_name="Başlıq")
    description = models.TextField(verbose_name="Açıqlama") 
    icon = models.CharField(max_length = 50,verbose_name="İkon")

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name_plural = "Xidmətlərimiz"
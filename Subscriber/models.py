from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(verbose_name = "E-poçt")
    ip_address = models.CharField(verbose_name = "İP ünvan", max_length = 30)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email
    
    class Meta: 
        verbose_name_plural = "Abunəçilər"

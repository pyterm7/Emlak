from django.db import models

class ContactMessage(models.Model):
    email = models.EmailField(verbose_name = "E-poçt")
    subject = models.CharField(max_length=100, verbose_name = "Mövzu")
    message = models.TextField(verbose_name = "Mesaj")

    # Ip adresinə də bax
    ip_address = models.CharField(verbose_name = "İP ünvan", max_length = 30)

    # Cavablandımı
    answer = models.BooleanField(default = False, verbose_name = "Baxıldı və cavablandırıldı kimi işarələ")

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return self.email
    
    class Meta:
        verbose_name_plural = "Əlaqə mesajları"
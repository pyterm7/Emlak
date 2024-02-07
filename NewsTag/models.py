from django.db import models

class NewsTagModel(models.Model):
    name = models.CharField(max_length = 50, verbose_name = "Teq")

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return self.name 
    
    class Meta:
        verbose_name_plural = "Teq adları"
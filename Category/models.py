from django.db import models

class CategoryModel(models.Model):
    name = models.CharField(max_length = 100, verbose_name = "Kateqoriya adı")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name = "Ana kateqoriyası", blank=True, null=True, related_name='child_categories')

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Kateqoriyalar"
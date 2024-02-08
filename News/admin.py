from django.contrib import admin
from News.models import NewsModel

@admin.register(NewsModel)
class NewsModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    readonly_fields = ['slug'] 
    search_fields = (
        "title",
        "description", 
    )
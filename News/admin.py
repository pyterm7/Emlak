from django.contrib import admin
from News.models import NewsModel, LikedNews, CommentNews

@admin.register(NewsModel)
class NewsModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    readonly_fields = ['slug'] 
    search_fields = (
        "title",
        "description", 
    )


admin.site.register(LikedNews)
admin.site.register(CommentNews)
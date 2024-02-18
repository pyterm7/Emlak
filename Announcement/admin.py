from django.contrib import admin
from Announcement.models import AnnouncementModel, AnnouncementPics

# admin.site.register(AnnouncementModel)
admin.site.register(AnnouncementPics)

@admin.register(AnnouncementModel)
class AnnouncementModelAdmin(admin.ModelAdmin):
    list_display = ['title','author','is_active']
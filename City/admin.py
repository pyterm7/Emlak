from django.contrib import admin
from City.models import City, Region, ZoneForBaku, ZoneForAbsheron

admin.site.register(Region)
admin.site.register(ZoneForBaku)
admin.site.register(ZoneForAbsheron)

@admin.register(City)
class CityAdminModel(admin.ModelAdmin):
    list_display = ['name']
    search_fields = (
        "name", 
    )
from django.contrib import admin
from City.models import City, Region, Village

# admin.site.register(City)
admin.site.register(Region)
# admin.site.register(Village)

@admin.register(City)
class CityAdminModel(admin.ModelAdmin):
    list_display = ['name']
    search_fields = (
        "name", 
    )
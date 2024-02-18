from django.contrib import admin
from Auth.models import CustomUser

# admin.site.register(CustomUser)

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['phone', 'is_staff', 'is_superuser','passport', 'created_at']
    search_fields = (
        "phone",
        "name", 
        "surname", 
        "email", 
        "bio", 
        "location", 
    )
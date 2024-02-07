from django.contrib import admin
from Auth.models import CustomUser

# admin.site.register(CustomUser)

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['phone', 'is_staff', 'is_superuser', 'created_at']
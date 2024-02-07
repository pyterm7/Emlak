from django.contrib import admin

from Contact.models import ContactMessage

# admin.site.register(ContactMessage)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['email', 'subject', 'answer']
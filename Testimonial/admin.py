from django.contrib import admin
from Testimonial.models import Testimonial

# admin.site.register(Testimonial)
@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'show']
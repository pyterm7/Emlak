from django.urls import path 

from Testimonial.views import CreateTestimonial

urlpatterns = [
    path('create/', CreateTestimonial, name="create-testimonial"),
]
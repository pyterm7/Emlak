from django.urls import path
from Contact.views import ContactPage


urlpatterns = [
    path('', ContactPage, name='contact-page'),
]
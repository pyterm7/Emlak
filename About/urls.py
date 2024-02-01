from django.urls import path 
from About.views import AboutPage, GetAboutData

urlpatterns = [
    path('', AboutPage, name="about-page"),
    path('get-data/', GetAboutData, name="get-about-data"),
]
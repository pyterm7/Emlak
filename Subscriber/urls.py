from django.urls import path
from Subscriber.views import Subscribe

urlpatterns = [
    path('', Subscribe, name="subscribe-page"),
]
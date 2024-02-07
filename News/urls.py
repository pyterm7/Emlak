from django.urls import path

from News.views import NewsDetail

urlpatterns = [
    path('detail/', NewsDetail, name="news-detail"),
]
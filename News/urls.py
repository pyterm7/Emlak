from django.urls import path

from News.views import NewsDetail

urlpatterns = [
    path('detail/<str:news>', NewsDetail, name="news-detail"),
]
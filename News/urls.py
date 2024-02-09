from django.urls import path

from News.views import NewsDetail, AllNews

urlpatterns = [
    path('', AllNews, name="all-news"),
    path('detail/<str:news>', NewsDetail, name="news-detail"),
]
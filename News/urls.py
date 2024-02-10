from django.urls import path

from News.views import NewsDetail, AllNews, LikeNews

urlpatterns = [
    path('', AllNews, name="all-news"),
    path('detail/<str:news>', NewsDetail, name="news-detail"),
    path('like/<int:id>', LikeNews, name="like-news"),
]
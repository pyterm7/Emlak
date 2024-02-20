from django.urls import path

from News.views import NewsDetail, AllNews, LikeNews, CreateNewComment

urlpatterns = [
    path('', AllNews, name="all-news"),
    path('detail/<str:news>', NewsDetail, name="news-detail"),
    path('like/<int:id>', LikeNews, name="like-news"),
    path('add-comment/<int:id>', CreateNewComment, name="add-comment"),
]
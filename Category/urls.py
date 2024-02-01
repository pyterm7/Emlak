from django.urls import path 
from Category.views import ShowCategories


urlpatterns = [
    path('list/', ShowCategories, name='show-categories'),
]
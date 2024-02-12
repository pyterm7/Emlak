from django.urls import path 
from Announcement.views import ShareAnnouncement

urlpatterns = [
    path('share/', ShareAnnouncement, name="share-announcement"),
]
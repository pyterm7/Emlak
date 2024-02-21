from django.urls import path 
from Announcement.views import ShareAnnouncement, AnnouncementDetail

urlpatterns = [
    path('share/', ShareAnnouncement, name="share-announcement"), 
    path('detail/', AnnouncementDetail, name="announcement-detail"),
]
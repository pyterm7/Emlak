from django.urls import path 
from Announcement.views import ShareAnnouncement, Announcements, AnnouncementDetail

urlpatterns = [
    path('share/', ShareAnnouncement, name="share-announcement"),
    path('list/', Announcements, name="announcement-list"),
    path('detail/', AnnouncementDetail, name="announcement-detail"),
]
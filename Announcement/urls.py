from django.urls import path 
from Announcement.views import ShareAnnouncement, AnnouncementDetail, GetZoneForRegion

urlpatterns = [
    path('share/', ShareAnnouncement, name="share-announcement"), 
    path('detail/', AnnouncementDetail, name="announcement-detail"),
    path('get-zone-for-region/', GetZoneForRegion, name='get-zone-for-region'),
]
from django.contrib import admin
from django.urls import path, include
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('tinymce/', include('tinymce.urls')),
    # URLS
    path('', include("Home.urls")),
    path('subscribe/', include("Subscriber.urls")),
    path('about/', include("About.urls")),
    path('contact/', include("Contact.urls")),
    path('auth/', include('Auth.urls')),
    path('category/', include("Category.urls")),
    path('announcement/', include("Announcement.urls")),
    path('testimonial/', include("Testimonial.urls")),
    # End URLS
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Admin panel"
admin.site.site_title = "Admin panel"
admin.site.index_title = "Daşınmaz əmlak"
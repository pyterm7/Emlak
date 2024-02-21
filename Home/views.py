from django.shortcuts import render
from Services.models import Service 
from Testimonial.models import Testimonial
from Announcement.models import AnnouncementModel


def Home(request):
    data = {}

    sort = request.GET.get("sort", False) 
    if sort == "lifo":
        sort = "-id"
        data["sort"] = "lifo"
    elif sort == "fifo":
        sort = "id"
        data["sort"] = "fifo"
    else:
        sort = "-id"
        data["sort"] = "lifo" 

    # Xidmətlərimiz
    our_services = Service.objects.all()

    # Reyler
    testimonials = Testimonial.objects.filter(show=True)

    # Son 3 elan
    last_3_announcement = AnnouncementModel.objects.filter(is_active=True).order_by("-id")[0:3]

    # CollectData
    if our_services.count() >= 3: data["services"] = our_services 
    if testimonials.count() >= 3: data["testimonials"] = testimonials
    # if last_3_announcement.count() == 3 : data["announcements"] = last_3_announcement

    
        
    if sort: announcements = AnnouncementModel.objects.filter(is_active = True).order_by(sort)
    else: announcements = AnnouncementModel.objects.filter(is_active = True).order_by("-id")

    announcements_count = announcements.count()
    data["announcements"] = announcements
    data["announcements_count"] = announcements_count

    return render(request, "index.html", context=data)
from django.shortcuts import render
from Services.models import Service 
from Testimonial.models import Testimonial
from Announcement.models import AnnouncementModel


def Home(request):
    data = {}

    # Xidmətlərimiz
    our_services = Service.objects.all()

    # Reyler
    testimonials = Testimonial.objects.filter(show=True)

    # Son 3 elan
    last_3_announcement = AnnouncementModel.objects.filter(is_active=True).order_by("-id")[0:3]

    # CollectData
    if our_services.count() >= 3: data["services"] = our_services 
    if testimonials.count() >= 3: data["testimonials"] = testimonials
    if last_3_announcement.count() == 3 : data["announcements"] = last_3_announcement
    return render(request, "index.html", context=data)
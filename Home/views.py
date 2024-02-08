from django.shortcuts import render
from Services.models import Service 
from Testimonial.models import Testimonial



def Home(request):
    data = {}
    # Xidmətlərimiz
    our_services = Service.objects.all()

    # Reyler
    testimonials = Testimonial.objects.filter(show=True)

    
    # CollectData
    if our_services.count() >= 3: data["services"] = our_services 
    if testimonials.count() >= 3: data["testimonials"] = testimonials
    return render(request, "index.html", context=data)
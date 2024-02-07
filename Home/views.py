from django.shortcuts import render
from Services.models import Service 
from Testimonial.models import Testimonial
from News.models import NewsModel


def Home(request):
    data = {}
    # Xidmətlərimiz
    our_services = Service.objects.all()

    # Reyler
    testimonials = Testimonial.objects.filter(show=True)

    # Xeberlerden son 3-u
    news = NewsModel.objects.order_by('-id').all()[0:3]

    
    # CollectData
    if our_services.count() >= 3: data["services"] = our_services 
    if testimonials.count() >= 3: data["testimonials"] = testimonials
    if news.count() > 0: data["news"] = news
    return render(request, "index.html", context=data)
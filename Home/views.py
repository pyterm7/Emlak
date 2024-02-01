from django.shortcuts import render
from Services.models import Service 

def Home(request):
    data = {}
    # Xidmətlərimiz
    our_services = Service.objects.all()
    
    # CollectData
    data["services"] = our_services 
    return render(request, "index.html", context=data)
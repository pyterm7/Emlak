import re
from django.shortcuts import render, redirect, HttpResponse
from Subscriber.models import Subscriber
from django.contrib import messages


def Subscribe(request): 
    #  Get IP address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for: ip = x_forwarded_for.split(',')[0]
    else: ip = request.META.get('REMOTE_ADDR')
    # Email Regex
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if request.POST:
        email = request.POST.get("subscriber_email", "") 
        if(re.fullmatch(email_regex, email)):
            if not Subscriber.objects.filter(email=email).first():
                Subscriber.objects.create(email=email, ip_address=ip)
                messages.success(request, "Təşəkkürlər. Abunə oldunuz.")
            else: messages.info(request, "Daha öncədən abunə olunmuşdur.")
            return redirect("home-page") 
        else: messages.info(request, "Email doğru formatda deyil.") 
    return redirect("home-page")
from django.shortcuts import render, redirect
from django.contrib import messages
from Testimonial.models import Testimonial


# Create your views here.
def CreateTestimonial(request):

    if request.POST:
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        message = request.POST.get("message")
        if len(name) > 50 or len(name) < 3:
            messages.info(request, "Ad maksimum 50, minimum 3 simvoldan ibarət olmalıdır.")
            return redirect("home-page")
        if len(surname) > 50 or len(surname) < 3:
            messages.info(request, "Soyad maksimum 50, minimum 3 simvoldan ibarət olmalıdır.")
            return redirect("home-page")
        if len(message) > 250 or len(message) < 10:
            messages.info(request, "Rəyiniz minimum 10 simvoldan, maksimum 250 simvoldan ibarət olmalıdır.")
            return redirect("home-page")
        try:
            Testimonial.objects.create(name=name, surname=surname, message=message)
            messages.success(request, "Rəy bildirdiyiniz üçün təşəkkür edirik.")
        except:
            messages.info(request, "Rəy qeydə alınmadı. Daha sonra yenidən cəhd edin.")
    return redirect('home-page')
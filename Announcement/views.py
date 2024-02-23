import os 
from PIL import Image
from io import BytesIO
from django.conf import settings
from Auth.models import CustomUser
from django.contrib import messages
from Category.models import CategoryModel
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from Announcement.models import AnnouncementModel, AnnouncementPics


def AnnouncementDetail(request):
    title = request.GET.get("title", False)
    if title:
        announcement = AnnouncementModel.objects.filter(slug=title, is_active=True).first()
        announcement_pics = AnnouncementPics.objects.filter(announcement=announcement)
        if announcement:
            data = {"announcement":announcement, "announcement_pics":announcement_pics}
            return render(request, "announcement-detail.html", context=data)
    messages.info(request, "Xəta oldu.")
    return redirect("home-page")

def ReturnMessagesAndData(request, data, msg):
    messages.info(request, msg)
    return render(request, "share-announcement.html", context=data)


@login_required(login_url="sign-in-page", redirect_field_name=None)
def ShareAnnouncement(request): 
    user = CustomUser.objects.filter(id=request.user.id).first() 
    if request.user.is_authenticated: 
        data = {}
        # Kateqoriyaları göndərdim
        categories = CategoryModel.objects.all()
        data['categories'] = categories
        # Valyutaları göndərdim
        ch_tuple = AnnouncementModel.ch
        ch_list = []
        for ch in ch_tuple: ch_list.append({f"key":ch[1]}) 
        data['ch_tuple'] = ch_list 
        
        
        if request.POST:
            announcement_type_of = request.POST.get("announcement_type_of", False) 
            announcement_category = request.POST.get("announcement_category", False)
            announcement_room_count = request.POST.get("announcement_room_count", False)
            announcement_currency = request.POST.get("announcement_currency", False) 
            announcement_description = request.POST.get("announcement_description", "")
            announcement_price = request.POST.get("announcement_price", False)
            announcement_the_initial_payment = request.POST.get("announcement_the_initial_payment", False)
            announcement_area = request.POST.get("announcement_area", False)
            announcement_has_internet = request.POST.get("announcement_has_internet", False)
            announcement_has_gas = request.POST.get("announcement_has_gas", False)
            announcement_has_electricity = request.POST.get("announcement_has_electricity", False)
            announcement_has_water = request.POST.get("announcement_has_water", False)
            announcement_has_water_tank = request.POST.get("announcement_has_water_tank", False)
            announcement_has_combi = request.POST.get("announcement_has_combi", False)
            announcement_furnished = request.POST.get("announcement_furnished", False)
            announcement_renovated = request.POST.get("announcement_renovated", False)
            announcement_picture = request.FILES.get("announcement_picture", False)
            announcement_pictures = request.FILES.getlist("announcement_pictures")
            
            # Addım - 1
            # Elanın növü : Satış(1||False) ya da Kirayə(2||True) olmalıdır.
            if announcement_type_of == "1": announcement_type_of = False 
            elif announcement_type_of == "2": announcement_type_of = True 
            else: announcement_type_of = False

            # Addım - 2
            # Kateqoriya : Həyət evi, Mənzil, Obyekt
            try: announcement_category = CategoryModel.objects.filter(id=announcement_category).first()
            except: return ReturnMessagesAndData(request, data, "Kateqoriya seçimində xəta oldu. Yenidən cəhd edin.")
            
            # Addım - 3
            # Otaq sayını yoxladım. Minimum 1, Maksimum 30 olmalıdır.
            try: announcement_room_count = int(announcement_room_count)
            except: return ReturnMessagesAndData(request, data, "Otaq sayını doğru formada (ədəd) daxil edin.")
            if announcement_room_count < 1 or announcement_room_count > 30: return ReturnMessagesAndData(request, data, "Otaq sayı minimum 1, maksimum 30 ola bilər.")
            
            # Addım - 4
            # Valyuta seçimini yoxlayaq / Ya DOLLAR Ya MANAT olmalıdır
            if announcement_currency != "DOLLAR" and announcement_currency != "MANAT": return ReturnMessagesAndData(request, data, "Valyuta seçimində xəta oldu.")

            # Addım - 
            # Açıqlamanı yoxladım
            announcement_description = announcement_description.strip()
            if len(announcement_description) < 50 or len(announcement_description) > 1000: return ReturnMessagesAndData(request, data, "Açıqlama minimum 50, maksimum 1000 simvoldan ibarət olmalıdır.")


        return render(request, "share-announcement.html", context=data)
            
    messages.info(request, "İcazəsiz cəhd.")
    return redirect("home-page")
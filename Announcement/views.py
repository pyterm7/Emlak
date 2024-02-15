from Auth.models import CustomUser
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Announcement.models import AnnouncementModel
from Category.models import CategoryModel

def ReturnMessagesAndData(request, data, msg):
    messages.info(request, msg)
    return render(request, "share-announcement.html", context=data)


@login_required(login_url="sign-in-page", redirect_field_name=None)
def ShareAnnouncement(request):
    categories = CategoryModel.objects.all()
    ch_tuple = AnnouncementModel.ch
    ch_list = []
    for ch in ch_tuple: ch_list.append({f"key":ch[1]}) 
    user = CustomUser.objects.filter(id=request.user.id).first()
    if user.parent_agent or user.is_staff: 
        data = {}
        data['ch_tuple'] = ch_list
        data['categories'] = categories
        if request.POST:  
            announcement_title = request.POST.get("announcement_title", False)
            announcement_location = request.POST.get("announcement_location", False)
            announcement_room_count = request.POST.get("announcement_room_count", False)
            announcement_currency = request.POST.get("announcement_currency", False) 
            announcement_price = request.POST.get("announcement_price", False)

            # 1-Basligi yoxladim
            announcement_title = announcement_title.strip()
            data["announcement_title"] = announcement_title 
            if announcement_title == "" or len(announcement_title) < 10 or len(announcement_title) > 225:
                return ReturnMessagesAndData(request, data, "Başlıq minimum 10, maksimum 225 simvoldan ibarət olmalıdır.")
            # 2-Ünvanı yoxladım 
            announcement_location = announcement_location.strip()
            data['announcement_location'] = announcement_location
            if announcement_location == "" or len(announcement_location) < 3 or len(announcement_location) > 255:
                return ReturnMessagesAndData(request, data, "Ünvan minimum 3, maksimum 255 simvoldan ibarət olmalıdır.")
            # 3-Otaq sayını yoxladım
            announcement_room_count = announcement_room_count.strip()
            data['announcement_room_count'] = announcement_room_count
            try: 
                announcement_room_count = int(announcement_room_count)
                if announcement_room_count < 1 or announcement_room_count > 100: 
                    return ReturnMessagesAndData(request, data, "Otaq sayı minimum 1, maksimum 100 olmalıdır.")
            except: return ReturnMessagesAndData(request, data, "Otaq sayı hissəsinə yalnız rəqəmlər daxil edilməlidir.")
            # 4 - Valyutanı yoxladım
            announcement_currency = announcement_currency.strip()
            data['announcement_currency'] = announcement_currency
            if announcement_currency != "DOLLAR" and announcement_currency != "MANAT":
                return ReturnMessagesAndData(request, data, "Valyuta seçimində xəta oldu.")
            # 5 - Kateqoriyanı yoxladım
            announcement_category_int = request.POST.get("announcement_category", False)  
            announcement_category_int = announcement_category_int.strip()
            data['announcement_category_int'] = announcement_category_int
            try: 
                announcement_category_int = int(announcement_category_int)
                announcement_category = CategoryModel.objects.filter(id=int(announcement_category_int)).first()
                if not announcement_category: return ReturnMessagesAndData(request, data, "Kateqoriya tapılmadı.")
            except: return ReturnMessagesAndData(request, data, "Kateqoriya seçimində xəta oldu.")
            # 6 - Qiyməti yoxladım
            announcement_price = announcement_price.strip()
            try:
                announcement_price = float(announcement_price)
                data['announcement_price'] = announcement_price
                if announcement_price < 1 or announcement_price > 1000000:
                    return ReturnMessagesAndData(request, data, "Qiymət minimum 1, maksimum 1000000 olmalıdır.")
            except: return ReturnMessagesAndData(request, data, "Qiymət hissəsinə yalnız ədəd daxil edilməlidir.")


            # try:
            #     new_announcement = AnnouncementModel()
            #     new_announcement.author = user 
            #     new_announcement.picture = announcement_picture
            #     new_announcement.title = announcement_title
            #     new_announcement.room_count = announcement_room_count
            #     new_announcement.currency = announcement_currency
            #     new_announcement.price = announcement_price
            #     new_announcement.area = announcement_area
            #     new_announcement.description = announcement_description
            #     new_announcement.category = announcement_category
            #     new_announcement.save() 

            #     messages.success(request, "Elan uğurla paylaşıldı.")
            #     return redirect("home-page")
            # except:
            #     messages.info(request, "Elan paylaşma prosesində xəta oldu.")
            #     return redirect("share-announcement")  
        return render(request, "share-announcement.html", context=data)
    messages.info(request, "İcazəsiz cəhd.")
    return redirect("home-page")
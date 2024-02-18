import os 
from PIL import Image
from io import BytesIO
from django.conf import settings
from Auth.models import CustomUser
from django.contrib import messages
from Category.models import CategoryModel
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Announcement.models import AnnouncementModel, AnnouncementPics

def Announcements(request):
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
        
    if sort: announcements = AnnouncementModel.objects.filter(is_active = True).order_by(sort)
    else: announcements = AnnouncementModel.objects.filter(is_active = True).order_by("-id")

    announcements_count = announcements.count()
    data["announcements"] = announcements
    data["announcements_count"] = announcements_count
    
    return render(request, "announcements.html", context=data)

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
    categories = CategoryModel.objects.all()
    ch_tuple = AnnouncementModel.ch
    ch_list = []
    for ch in ch_tuple: ch_list.append({f"key":ch[1]}) 
    user = CustomUser.objects.filter(id=request.user.id).first()
    # if user.parent_agent or user.is_staff: 
    if request.user.is_authenticated: 
        data = {}
        data['ch_tuple'] = ch_list
        data['categories'] = categories
        if request.POST:  
            announcement_title = request.POST.get("announcement_title", False)
            announcement_location = request.POST.get("announcement_location", False)
            announcement_room_count = request.POST.get("announcement_room_count", False)
            announcement_currency = request.POST.get("announcement_currency", False) 
            announcement_price = request.POST.get("announcement_price", False)
            announcement_the_initial_payment = request.POST.get("announcement_the_initial_payment", False)
            announcement_area = request.POST.get("announcement_area", False)
            announcement_description = request.POST.get("announcement_description", False)
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
            try: 
                data['announcement_category_int'] = int(announcement_category_int)
                announcement_category_int = int(announcement_category_int)
                announcement_category = CategoryModel.objects.filter(id=int(announcement_category_int)).first()
                if not announcement_category: return ReturnMessagesAndData(request, data, "Kateqoriya tapılmadı.")
            except: return ReturnMessagesAndData(request, data, "Kateqoriya seçimində xəta oldu.")
            # 6 - Qiyməti yoxladım
            try: 
                announcement_price = float(announcement_price.strip())
                data['announcement_price'] = announcement_price
                if announcement_price < 1 or announcement_price > 1000000:
                    return ReturnMessagesAndData(request, data, "Qiymət minimum 1, maksimum 1000000 olmalıdır.")
            except: return ReturnMessagesAndData(request, data, "Qiymət hissəsinə yalnız ədəd daxil edilməlidir.")
            # 7 - İlkin ödənişi yoxladım
            try:
                announcement_the_initial_payment = float(announcement_the_initial_payment.strip())
                data['announcement_the_initial_payment'] = announcement_the_initial_payment
                if announcement_the_initial_payment < 0 or announcement_the_initial_payment > 1000000:
                    return ReturnMessagesAndData(request, data, "İlkin ödəniş minimum 0, maksimum 1000000 olmalıdır.")
            except: return ReturnMessagesAndData(request, data, "İlkin ödəniş hissəsinə yalnız ədəd daxil edilməlidir.")
            # 8 - Sahəni yoxladım
            try:
                announcement_area = float(announcement_area.strip())
                data['announcement_area'] = announcement_area
                if announcement_area < 0 or announcement_area > 10000:
                    return ReturnMessagesAndData(request, data, "Sahə minimum 0, maksimum 10000 olmalıdır.") 
            except:
                return ReturnMessagesAndData(request, data, "Sahə hissəsinə yalnızca ədəd daxil edilməlidir.")
            # 9 - Açıqlamanı yoxladım 
            if announcement_description is False or announcement_description.strip() == "":
                return ReturnMessagesAndData(request, data, "Açıqlama yazın.") 
            announcement_description = announcement_description.strip()
            data['announcement_description'] = announcement_description
            if len(announcement_description) < 10 or len(announcement_description) > 1000:
                return ReturnMessagesAndData(request, data, "Açıqlama minimum 10, maksimum 1000 simvoldan ibarət olmalıdır.")
            # 10 - İnterneti yoxladım
            if announcement_has_internet and announcement_has_internet == "on": announcement_has_internet = True 
            else: announcement_has_internet = False
            data['announcement_has_internet'] = announcement_has_internet
            # 11 - Qaz sistemi yoxladım
            if announcement_has_gas and announcement_has_gas == "on": announcement_has_gas = True 
            else: announcement_has_gas = False 
            data['announcement_has_gas'] = announcement_has_gas
            # 12 - Elektrik sistemi yoxladım
            if announcement_has_electricity and announcement_has_electricity == "on": announcement_has_electricity = True 
            else: announcement_has_electricity = False 
            data['announcement_has_electricity'] = announcement_has_electricity
            # 13 - Su sistemini yoxladım
            if announcement_has_water and announcement_has_water == "on": announcement_has_water = True 
            else: announcement_has_water = False 
            data['announcement_has_water'] = announcement_has_water
            # 14 - Su çəni
            if announcement_has_water_tank and announcement_has_water_tank == "on": announcement_has_water_tank = True 
            else: announcement_has_water_tank = False 
            data['announcement_has_water_tank'] = announcement_has_water_tank
            # 15 - Kombini yoxladim
            if announcement_has_combi and announcement_has_combi == "on": announcement_has_combi = True 
            else: announcement_has_combi = False 
            data['announcement_has_combi'] = announcement_has_combi
            # 16 - Əşyalıdır
            if announcement_furnished and announcement_furnished == "on": announcement_furnished = True 
            else: announcement_furnished = False 
            data['announcement_furnished'] = announcement_furnished
            # 17 - Temirlidir
            if announcement_renovated and announcement_renovated == "on": announcement_renovated = True 
            else: announcement_renovated = False 
            data['announcement_renovated'] = announcement_renovated
            # 18 - Əsas şəkili yoxlayaq
            if announcement_picture == False:
                return ReturnMessagesAndData(request, data, "Əsas şəkil seçilməyib.")
            # 19 - Digər şəkillər
            if not announcement_pictures:
                return ReturnMessagesAndData(request, data, "Digər şəkilləri daxil edin.")
            if len(announcement_pictures) > 7:
                return ReturnMessagesAndData(request, data, "Əsas şəkildən əlavə maksimum 7 şəkil daxil edə bilərsiniz.")

            try:
                new_announcement = AnnouncementModel()
                new_announcement.author = user 
                new_announcement.picture = announcement_picture
                new_announcement.title = announcement_title
                new_announcement.room_count = announcement_room_count
                new_announcement.currency = announcement_currency
                new_announcement.price = announcement_price
                new_announcement.the_initial_payment = announcement_the_initial_payment
                new_announcement.location = announcement_location

                new_announcement.area = announcement_area
                new_announcement.description = announcement_description
                new_announcement.category = announcement_category
                new_announcement.renovated = announcement_renovated
                new_announcement.has_combi = announcement_has_combi
                new_announcement.furnished = announcement_furnished
                new_announcement.has_electricity = announcement_has_electricity
                new_announcement.has_gas = announcement_has_gas
                new_announcement.has_internet = announcement_has_internet 
                new_announcement.has_water = announcement_has_water
                new_announcement.has_water_tank = announcement_has_water_tank
                new_announcement.save()  
                
                for img in announcement_pictures: 
                    pics_count = AnnouncementPics.objects.all().count()
                    img = Image.open(BytesIO(img.read()))
                    new_image_name = f"{user.phone[1:]}-{pics_count}.{img.format.lower()}"
                    new_path = os.path.join(settings.MEDIA_ROOT, 'AnnouncementPics', new_image_name)
                    img.save(new_path) 
                    new_img_for_announcement = AnnouncementPics(announcement=new_announcement)
                    # new_img_for_announcement.img = new_path
                    new_img_for_announcement.img = os.path.join("AnnouncementPics",new_image_name)
                    new_img_for_announcement.save()

                messages.success(request, "Elan uğurla paylaşıldı.")
                return redirect("home-page")
            except : 
                messages.info(request, "Elan paylaşma prosesində xəta oldu. Daha sonra yenidən cəhd edin.")
                return redirect("share-announcement")  
        return render(request, "share-announcement.html", context=data)
    messages.info(request, "İcazəsiz cəhd.")
    return redirect("home-page")
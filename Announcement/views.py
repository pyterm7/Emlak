import os
import json
from PIL import Image
from io import BytesIO
from django.conf import settings
from Auth.models import CustomUser
from django.contrib import messages
from django.http import HttpResponse
from Category.models import CategoryModel
from City.models import City, Region, ZoneForBaku, ZoneForAbsheron
from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from Announcement.models import AnnouncementModel, AnnouncementPics

def GetZoneForRegion(request):
    if request.GET:
        region_id = request.GET.get("region").strip()
        try: 
            region_id = int(region_id)
            if region := Region.objects.filter(id=region_id).first():
                context = { "regions": [zone.name for zone in ZoneForBaku.objects.filter(region=region).all() ] }
                return HttpResponse(json.dumps(context), content_type='application/json')
        except: return HttpResponse(json.dumps({"error":False}), content_type='application/json')
    return HttpResponse(json.dumps({"error":False}), content_type='application/json')

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
    if user and request.user.is_authenticated: 
        data = {}
        # Kateqoriyaları göndərdim
        categories = CategoryModel.objects.all()
        data['categories'] = categories
        # Valyutaları göndərdim
        ch_tuple = AnnouncementModel.ch
        ch_list = []
        for ch in ch_tuple: ch_list.append({f"key":ch[1]}) 
        data['ch_tuple'] = ch_list 
        # Şəhərləri göndərdim
        cities = City.objects.all()
        data['cities'] = cities
        # Rayonları göndərdim
        regions = Region.objects.all()
        data['regions'] = regions
        # Abşeron Zonalarını göndərdim
        data['zone_for_absheron'] = ZoneForAbsheron.objects.all()

        if request.POST: 
            # Əsas şəkil
            announcement_picture = request.FILES.get("announcement_picture", False)
            if announcement_picture:
                cover_img = Image.open(BytesIO(announcement_picture.read()))
                if( cover_img.width < 770  or cover_img.height < 520) : return ReturnMessagesAndData(request, data, "Əsas şəklin ölçüləri minimum 770x520 olmalıdır.")
            else: return ReturnMessagesAndData(request, data, "Əsas şəkli seçin.")
            # Şəhər
            announcement_city = request.POST.get("announcement_city", False)
            if announcement_city:
                if City.objects.filter(name=announcement_city).first():
                    announcement_city = City.objects.filter(name=announcement_city).first()
                else: return ReturnMessagesAndData(request, data, "Şəhər seçimində xəta oldu.")
            else: return ReturnMessagesAndData(request, data, "Şəhər seçin.")
            # Rayon
            region = None
            announcement_zone_for_baku_region = None
            if announcement_city.name == "Bakı":
                announcement_region = request.POST.get("announcement_region", False)
                if announcement_region:
                    if Region.objects.filter(id=announcement_region).first():
                        region = Region.objects.filter(name=announcement_region).first()
                        # Zone 4 Baku
                        if region:
                            announcement_zone_for_region = request.POST.get("announcement_zone_for_region", False)
                            if announcement_zone_for_region:
                                announcement_zone_for_baku_region = ZoneForBaku.objects.filter(region=region, name=announcement_zone_for_region).first()
                                if not announcement_zone_for_baku_region: return ReturnMessagesAndData(request, data, "Bölgə seçimində xəta oldu.") 
            
                    else: return ReturnMessagesAndData(request, data, "Rayon seçimində xəta oldu.")
            # Zone 4 Absheron
            announcement_zone_for_absheron_region = None
            if announcement_city.name == "Abşeron":
                announcement_zone_for_absheron = request.POST.get("announcement_zone_for_absheron", False)
                if announcement_zone_for_absheron:
                    announcement_zone_for_absheron_region = ZoneForAbsheron.objects.filter(name=announcement_zone_for_absheron).first()
                else: return ReturnMessagesAndData(request, data, "Abşeron bölgələri seçimində xəta oldu.")
            # Elanın növü / Default = False
            # Elanın növü : Satış(1||False) ya da Kirayə(2||True) olmalıdır.
            announcement_type_of = request.POST.get("announcement_type_of", False) 
            if announcement_type_of == "1": announcement_type_of = False 
            elif announcement_type_of == "2": announcement_type_of = True 
            else: announcement_type_of = False
            # Kateqoriya : Həyət evi, Mənzil, Obyekt
            checked_apartment = False
            announcement_category = request.POST.get("announcement_category", False)
            try: announcement_category = CategoryModel.objects.filter(name=announcement_category).first()
            except: return ReturnMessagesAndData(request, data, "Kateqoriya seçimində xəta oldu. Yenidən cəhd edin.")
            if announcement_category.name == "Mənzil": checked_apartment = True
            else: checked_apartment = False 
            # Mənzil seçilibsə hansı mərtəbədədir ?
            # Mənzilin nömrəsi nədir ?
            if checked_apartment:
                # Mərtəbə
                announcement_floor = request.POST.get("announcement_floor", False)
                if announcement_floor:
                    try: announcement_floor = int(announcement_floor)
                    except: return ReturnMessagesAndData(request, data, "Mərtəbə doğru daxil edilmədi.")
                else: return ReturnMessagesAndData(request, data, "Mərtəbə daxil edilmədi.")
                # Mənzil nömrəsi 
                announcement_apartment = request.POST.get("announcement_apartment", False)
                if announcement_apartment:
                    try: announcement_apartment = int(announcement_apartment)
                    except: return ReturnMessagesAndData(request, data, "Mənzil nömrəsi doğru daxil edilmədi.")
                else: return ReturnMessagesAndData(request, data, "Mənzil nömrəsi daxil edilmədi.")
                #  Lift varmı
                announcement_elevator = request.POST.get("announcement_elevator", False)
                if announcement_elevator and announcement_elevator == "on": announcement_elevator = True 
                else: announcement_elevator = False
            # Əks halda Mərtəbə sayını yoxlayaq
            else:
                # Mərtəbə sayı
                announcement_floor_count = request.POST.get("announcement_floor_count", False)
                if announcement_floor_count:
                    try: announcement_floor_count = int(announcement_floor_count)
                    except: return ReturnMessagesAndData(request, data, "Mərtəbə sayı doğru daxil edilmədi.")
                else: return ReturnMessagesAndData(request, data, "Mərtəbə sayı daxil edilmədi.")
                # İlkin ödəniş
                announcement_the_initial_payment = request.POST.get("announcement_the_initial_payment", 0)
                try: 
                    announcement_the_initial_payment = float(announcement_the_initial_payment)
                    if announcement_the_initial_payment < 0 or announcement_the_initial_payment > 100000:
                        return ReturnMessagesAndData(request, data, "İlkin ödəniş minimum 0, maksimum 100000 ola bilər.")
                except: return ReturnMessagesAndData(request, data, "İlkin ödənişi doğru formada daxil edin.")
            # Otaq sayı
            announcement_room_count = request.POST.get("announcement_room_count", False)
            if announcement_room_count:
                try: 
                    announcement_room_count = int(announcement_room_count)
                    if announcement_room_count < 1 or announcement_room_count > 30:
                        return ReturnMessagesAndData(request, data, "Otaq sayı minimum 1, maksimum 30 ola bilər.")
                except: return ReturnMessagesAndData(request, data, "Otaq sayı doğru daxil edilmədi.")
            else: return ReturnMessagesAndData(request, data, "Otaq sayı daxil edilmədi.")
            # Valyuta
            # Valyuta seçimini yoxlayaq / Ya DOLLAR Ya MANAT olmalıdır
            announcement_currency = request.POST.get("announcement_currency", False) 
            if announcement_currency != "DOLLAR" and announcement_currency != "MANAT": return ReturnMessagesAndData(request, data, "Valyuta seçimində xəta oldu.")
            # Qiymət
            announcement_price = request.POST.get("announcement_price", 0)
            try: 
                announcement_price = float(announcement_price)
                if announcement_price < 10 or announcement_price > 1000000:
                    return ReturnMessagesAndData(request, data, "Qiymət minimum 10, maksimum 1 000 000 olmalıdır.")
            except: return ReturnMessagesAndData(request, data, "Qiyməti doğru formada daxil edin.")
            # Sahə
            announcement_area = request.POST.get("announcement_area", 0)
            if announcement_area:
                try: 
                    announcement_area = float(announcement_area)
                    if announcement_area < 5:
                        return ReturnMessagesAndData(request, data, "Sahə minimum 5.0 kv olmalıdır.")
                except: return ReturnMessagesAndData(request, data, "Sahəni doğru formada daxil edin.")
            else: return ReturnMessagesAndData(request, data, "Sahəni daxil edin.")
            # Açıqlama
            announcement_description = request.POST.get("announcement_description", "")
            if announcement_description:
                if len(announcement_description) < 50 or len(announcement_description) > 1000:
                    return ReturnMessagesAndData(request, data, "Açıqlama minimum 50, maksimum 1000 simvoldan ibarət olmalıdır.")
            else: return ReturnMessagesAndData(request, data, "Açıqlama yazın.")
            # İnternet
            announcement_has_internet = request.POST.get("announcement_has_internet", False)
            if announcement_has_internet and announcement_has_internet == "on": announcement_has_internet = True
            else: announcement_has_internet = False 
            # Qaz
            announcement_has_gas = request.POST.get("announcement_has_gas", False)
            if announcement_has_gas and announcement_has_gas == "on": announcement_has_gas = True 
            else: announcement_has_gas = False 
            # Elektrik
            announcement_has_electricity = request.POST.get("announcement_has_electricity", False)
            if announcement_has_electricity and announcement_has_electricity == "on": announcement_has_electricity = True 
            else: announcement_has_electricity = False 
            # Su
            announcement_has_water = request.POST.get("announcement_has_water", False)
            if announcement_has_water and announcement_has_water == 'on': announcement_has_water = True 
            else: announcement_has_water = False 
            # Su çəni
            announcement_has_water_tank = request.POST.get("announcement_has_water_tank", False)
            if announcement_has_water_tank and announcement_has_water_tank == "on": announcement_has_water_tank = True 
            else: announcement_has_water_tank = False
            # Kombi
            announcement_has_combi = request.POST.get("announcement_has_combi", False)
            if announcement_has_combi and announcement_has_combi == "on": announcement_has_combi = True 
            else: announcement_has_combi = False 
            # Əşyalıdır
            announcement_furnished = request.POST.get("announcement_furnished", False)
            if announcement_furnished and announcement_furnished == "on": announcement_furnished = True 
            else: announcement_furnished = False 
            # Təmirlidir
            announcement_renovated = request.POST.get("announcement_renovated", False)
            if announcement_renovated and announcement_renovated == "on": announcement_renovated = True 
            else: announcement_renovated = False 
            # Razılıq
            i_agree_terms_and_conditions = request.POST.get("i_agree_terms_and_conditions", False)
            if i_agree_terms_and_conditions and i_agree_terms_and_conditions == "on":
                announcement_pictures = request.FILES.getlist("announcement_pictures", []) 
                # Maks 7 Minimum 3 şəkil
                if len(announcement_pictures) > 7 or len(announcement_pictures) < 3: return ReturnMessagesAndData(request, data, "Əsas şəkildən əlavə maksimum 7, minimum 3 şəkil daxil edilməlidir.")       
                """
                    # # Ölçüləri 520-dən az olmaz
                    # for img in announcement_pictures_copy: 
                    #     img = Image.open(BytesIO(img.read())) 
                    #     width, height = img.size
                    #     if width < 520 or height < 520: 
                    #         return ReturnMessagesAndData(request, data, "Şəkillərin ölçüsü minimum 520x520 olmalıdır.") 
                """                
                # Create Et Elani
                try: 
                    new_announcement = AnnouncementModel(author=user) 
                    # Başlıq
                    if announcement_city.name=="Bakı": new_announcement.title = f"{announcement_city.name}, {announcement_region}, {announcement_room_count} otaq, {announcement_area} kv, {announcement_category.name}"
                    if announcement_city.name=="Abşeron": new_announcement.title = f"{announcement_city.name}, {announcement_zone_for_absheron_region.name}, {announcement_room_count} otaq, {announcement_area} kv, {announcement_category.name}"
                    else: new_announcement.title = f"{announcement_city.name}, {announcement_room_count} otaq, {announcement_area} kv, {announcement_category.name}"
                    # Elan növü
                    new_announcement.type_of = announcement_type_of
                    # Kateqoriya
                    new_announcement.category = announcement_category
                    # Şəhər
                    new_announcement.city = announcement_city
                    # Region
                    if announcement_city.name == "Bakı" : new_announcement.region = region 
                    # Bakı Bölgəsi
                    if region and announcement_zone_for_baku_region:
                        if announcement_city.name == "Bakı": new_announcement.zone_for_baku = announcement_zone_for_baku_region
                    # Abşeron bölgəsi
                    if announcement_zone_for_absheron_region:
                        if announcement_city.name == "Abşeron": new_announcement.zone_for_absheron = announcement_zone_for_absheron_region
                    # Valyuta
                    new_announcement.currency = announcement_currency
                    # Qiymət
                    new_announcement.price = announcement_price
                    if announcement_category.name == "Mənzil":
                        # Lift
                        new_announcement.has_elevator = announcement_elevator
                        # Mərtəbə
                        new_announcement.floor = announcement_floor
                        # Mənzil
                        new_announcement.apartment = announcement_apartment
                    else:
                        # Mərtəbə sayı
                        new_announcement.floor_count = announcement_floor_count
                        # İlkin ödəniş
                        new_announcement.the_initial_payment = announcement_the_initial_payment
                    # Açıqlama
                    new_announcement.description = announcement_description
                    # Otaq sayı
                    new_announcement.room_count = announcement_room_count
                    # Sahə
                    new_announcement.area = announcement_area
                    # İnternet
                    new_announcement.has_internet = announcement_has_internet
                    # Qaz
                    new_announcement.has_gas = announcement_has_gas
                    # Elektrik
                    new_announcement.has_electricity = announcement_has_electricity
                    # Su
                    new_announcement.has_water = announcement_has_water
                    # Su bakı
                    new_announcement.has_water_tank = announcement_has_water_tank
                    # Kombi
                    new_announcement.has_combi = announcement_has_combi
                    # Təmirlidir
                    new_announcement.renovated = announcement_renovated
                    # Əşyalıdır
                    new_announcement.furnished = announcement_furnished
                    new_announcement.save()

                    # Əsas şəkil
                    new_image_name = f"{user.phone[1:]}-{new_announcement.id}.webp"
                    new_path = os.path.join(settings.MEDIA_ROOT, 'AnnouncementMainPics', new_image_name)
                    cover_img.thumbnail((770, 520))
                    cover_img.save(new_path, quality=20, optimize=True) 
                    new_announcement.picture = os.path.join("AnnouncementMainPics", new_image_name)
                    new_announcement.save()
                    # Digər şəkillər 
                    for img in announcement_pictures:  
                        pics_count = AnnouncementPics.objects.all().count()
                        img = Image.open(BytesIO(img.read())) 
                        new_image_name = f"{user.phone[1:]}-{pics_count}.webp"
                        new_path = os.path.join(settings.MEDIA_ROOT, 'AnnouncementPics', new_image_name)
                        img.thumbnail((770, 520)) 
                        img.save(new_path, quality=20, optimize=True) 
                        new_img_for_announcement = AnnouncementPics(announcement=new_announcement) 
                        new_img_for_announcement.img = os.path.join("AnnouncementPics",new_image_name)
                        new_img_for_announcement.save() 
                    messages.info(request, "Elan uğurla paylaşıldı. 24-saat ərzində yoxlanılacaq.")
                    return redirect("home-page")
                except : return ReturnMessagesAndData(request, data, "Elanın paylaşılmasında xəta oldu. Daha sonra yenidən cəhd edin.")
            else: return ReturnMessagesAndData(request, data, "Elanı paylaşmaq üçün Qaydalar və Şərtlərlə tanış olmalı və qəbul etməlisiniz.")
        return render(request, "share-announcement.html", context=data)
            
    messages.info(request, "İcazəsiz cəhd.")
    return redirect("home-page")
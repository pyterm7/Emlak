from math import ceil
from django.shortcuts import render, redirect
from Services.models import Service 
from Testimonial.models import Testimonial
from Announcement.models import AnnouncementModel
from Category.models import CategoryModel
from django.db.models import Q

def Home(request):
    data = {}

    sort = request.GET.get("sort", False) 
    page = request.GET.get("page", 1)
    filter_for = request.GET.get("for", False)
    search_text = request.GET.get("search_text", False)
    currency = request.GET.get("currency", False)
    min_price = request.GET.get("min_price", False)
    max_price = request.GET.get("max_price", False)
    room_count = request.GET.get("room_count", False)
    category = request.GET.get("category", False)
    renovated = request.GET.get("renovated", False)
    furnished = request.GET.get("furnished", False)
    has_internet = request.GET.get("has_internet", False)
    has_elevator = request.GET.get("has_elevator", False)
    has_gas = request.GET.get("has_gas", False)
    has_electricity = request.GET.get("has_electricity", False)
    has_water = request.GET.get("has_water", False)
    has_water_tank = request.GET.get("has_water_tank", False)
    has_combi = request.GET.get("has_combi", False)

    try: page = int(page)
    except: page = 1

    if sort == "lifo":
        sort = "-id"
        data["sort"] = "lifo"
    elif sort == "fifo":
        sort = "id"
        data["sort"] = "fifo"
    else:
        sort = "-id"
        data["sort"] = "lifo" 

    # Xidmətlərimiz
    our_services = Service.objects.all()

    # Reyler
    testimonials = Testimonial.objects.filter(show=True)

    # CollectData
    if our_services.count() >= 3: data["services"] = our_services 
    if testimonials.count() >= 3: data["testimonials"] = testimonials 


    # Sırala
    if sort: announcements = AnnouncementModel.objects.filter(is_active = True).order_by(sort)
    else: announcements = AnnouncementModel.objects.filter(is_active = True).order_by("-id")
    total_announcement = announcements.count()

    # For - Kiraye - Satis
    data["for_rent"] = announcements.filter(type_of=True).count()
    data["for_sale"] = announcements.filter(type_of=False).count()
    

    # Elan növü
    if filter_for:
        if filter_for == "sale": announcements = announcements.filter(type_of=False)
        elif filter_for == "rent": announcements = announcements.filter(type_of=True)
        data["filter_for"] = filter_for

    # Sözlərə görə axtar
    if search_text: announcements = announcements.filter(title__icontains = search_text.strip().lower())

    # Mezenne
    if currency and currency == "DOLLAR": announcements = announcements.filter(currency="DOLLAR")
    if currency and currency == "MANAT": announcements = announcements.filter(currency="MANAT")

    # Minimum|Maksimum qiymət
    if min_price:
        try: 
            min_price = int(min_price) 
            announcements = announcements.filter(price__gte=min_price)
        except: pass
    if max_price:
        try:
            max_price = int(max_price) 
            announcements = announcements.filter(price__lte=max_price)
        except: pass 
    
    # Room Count
    if room_count:
        if room_count == '1': announcements = announcements.filter(room_count = 1)
        if room_count == '2': announcements = announcements.filter(room_count = 2) 
        if room_count == '3': announcements = announcements.filter(room_count = 3)
        if room_count == '4': announcements = announcements.filter(room_count = 4)
        if room_count == '5+': announcements = announcements.filter(room_count__gte = 5)

    # Kateqoriya
    if category:
        if category == "all": pass 
        else: 
            try:
                category = int(category)
                announcements = announcements.filter(category__id=category)
            except: pass
    
    # Temirli
    if renovated: announcements = announcements.filter(renovated=True)
    # Esyali
    if furnished: announcements = announcements.filter(furnished=True)
    # Internetli
    if has_internet: announcements = announcements.filter(has_internet=True)
    # Elektrikle techiz olunub
    if has_electricity: announcements = announcements.filter(has_electricity=True)
    # Lift var
    if has_elevator: announcements = announcements.filter(has_elevator=True)
    # Qaz cekilib
    if has_gas: announcements = announcements.filter(has_gas=True)
    # Su cekilib
    if has_water: announcements = announcements.filter(has_water=True)
    # Su ceni var elave
    if has_water_tank: announcements = announcements.filter(has_water_tank=True)
    # Kombi var
    if has_combi: announcements = announcements.filter(has_combi=True)
 

    limit = 6
    total_page = 1 
    if total_announcement != 0: total_page = ceil(total_announcement / limit) 
    if page > total_page: return redirect("home-page")
    elif page < 1: return redirect("home-page") 
    page_start = (page - 1) * limit
    page_end = page * limit  
    page_numbers = [] 
    if total_page <= 5: 
        for page_num in range(1, total_page+1): page_numbers.append(page_num)
    elif total_page > 5:
        if page > 2 and page < total_page - 2:
            for page_num in range(page - 2, page + 3): page_numbers.append(page_num) 
        elif page > 2 and page > total_page - 3:
            for page_num in range(total_page - 4, total_page + 1): page_numbers.append(page_num)
        else: 
            for page_num in range(1, 6): page_numbers.append(page_num)


    announcements = announcements[page_start:page_end] 
    data["announcements"] = announcements
    data["announcements_count"] = total_announcement
    data["aktiv_page"] = page 
    data["page_numbers"] = page_numbers
    data["a_categories"] = CategoryModel.objects.all()
    data["total_page"] = total_page

    return render(request, "index.html", context=data)
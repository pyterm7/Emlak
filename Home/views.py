from math import ceil
from django.shortcuts import render, redirect
from Services.models import Service 
from Testimonial.models import Testimonial
from Announcement.models import AnnouncementModel
from Category.models import CategoryModel


def Home(request):
    data = {}

    sort = request.GET.get("sort", False) 
    page = request.GET.get("page", 1)
    filter_for = request.GET.get("for", False)
    search_text = request.GET.get("search_text", False)
   

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

    # For
    data["for_rent"] = announcements.filter(type_of=True).count()
    data["for_sale"] = announcements.filter(type_of=False).count()
    

    # Elan növü
    if filter_for:
        if filter_for == "sale": announcements = announcements.filter(type_of=False)
        elif filter_for == "rent": announcements = announcements.filter(type_of=True)
        data["filter_for"] = filter_for

    # Sözlərə görə axtar
    if search_text: announcements = announcements.filter(title__icontains = search_text.lower())

    limit = 6
    total_page = 1

    if total_announcement != 0:
        total_page = ceil(total_announcement / limit)

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
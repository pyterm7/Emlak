from Auth.models import CustomUser
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Announcement.models import AnnouncementModel
from Category.models import CategoryModel

@login_required(login_url="sign-in-page", redirect_field_name=None)
def ShareAnnouncement(request):
    categories = CategoryModel.objects.all()
    ch_tuple = AnnouncementModel.ch
    ch_list = []
    for ch in ch_tuple:
        ch_list.append({f"key":ch[1]}) 
    user = CustomUser.objects.filter(id=request.user.id).first()
    if user.parent_agent or user.is_staff: 
        if request.POST:
            announcement_picture = request.FILES.get("announcement_picture", False)
            announcement_title = request.POST.get("announcement_title", False)
            announcement_room_count = request.POST.get("announcement_room_count", False)
            announcement_currency = request.POST.get("announcement_currency", False)
            announcement_price = request.POST.get("announcement_price", False)
            announcement_area = request.POST.get("announcement_area", False)
            announcement_description = request.POST.get("announcement_description", False)
            announcement_category = request.POST.get("announcement_category", False)
            announcement_category = CategoryModel.objects.filter(id=int(announcement_category)).first()
            try:
                new_announcement = AnnouncementModel()
                new_announcement.author = user 
                new_announcement.picture = announcement_picture
                new_announcement.title = announcement_title
                new_announcement.room_count = announcement_room_count
                new_announcement.currency = announcement_currency
                new_announcement.price = announcement_price
                new_announcement.area = announcement_area
                new_announcement.description = announcement_description
                new_announcement.category = announcement_category
                new_announcement.save() 

                messages.success(request, "Elan uğurla paylaşıldı.")
                return redirect("home-page")
            except:
                messages.info(request, "Elan paylaşma prosesində xəta oldu.")
                return redirect("share-announcement")

        return render(request, "share-announcement.html", context={"ch_tuple":ch_list, "categories":categories})
    messages.info(request, "İcazəsiz cəhd.")
    return redirect("home-page")
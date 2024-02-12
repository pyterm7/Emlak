from Auth.models import CustomUser
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Announcement.models import AnnouncementModel


@login_required(login_url="sign-in-page", redirect_field_name=None)
def ShareAnnouncement(request):
    ch_tuple = AnnouncementModel.ch
    ch_list = []
    for ch in ch_tuple:
        ch_list.append({f"key":ch[1]})
    
    user = CustomUser.objects.filter(id=request.user.id).first()
    if user.parent_agent or user.is_staff: 
        return render(request, "share-announcement.html", context={"ch_tuple":ch_list})
    messages.info(request, "İcazəsiz cəhd.")
    return redirect("home-page")
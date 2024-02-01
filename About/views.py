import json
from django.shortcuts import render, redirect  
from About.models import About   
from django.http import HttpResponse

def AboutPage(request):
    data = {}
    if About.objects.all().count() > 0: 
        if about_us := About.objects.last(): data["about"] = about_us 
        return render(request, "about.html", context=data)
    return redirect('home-page')


def GetAboutData(request): 
    if About.objects.all().count() > 0: 
        if About.objects.last(): 
            data = About.objects.last() 
            return HttpResponse(json.dumps({
                "short_description":data.short_description,
                "location":data.location,
                "phone_1":data.phone,
                "phone_2":data.phone_2,
                "email_1":data.email,
                "email_2":data.email_2,
                "safe_phone": data.phone.replace("-", ""),
                "facebook":data.facebook,
                "instagram":data.instagram,
                "youtube":data.youtube,
                "vimeo":data.vimeo,
                "twitter":data.twitter,
                "pinterest":data.pinterest,
                "tiktok":data.tiktok,
                }), content_type='application/json')
    return HttpResponse(json.dumps({"about":False}), content_type='application/json')


 
 
    
            


    
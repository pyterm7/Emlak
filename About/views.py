import json
from django.shortcuts import render, redirect  
from About.models import About   
from django.http import HttpResponse
from News.models import NewsModel

def AboutPage(request):
    data = {}
    if About.objects.all().count() > 0: 
        if about_us := About.objects.last(): data["about"] = about_us 
        return render(request, "about.html", context=data)
    return redirect('home-page')


def GetAboutData(request): 
    domain = "http://127.0.0.1:8000" 
    news = None
    if NewsModel.objects.filter(is_active=True).count() >= 5: news = NewsModel.objects.filter(is_active=True).order_by('-id').all()[0:5]  

    if About.objects.all().count() > 0: 
        if About.objects.last(): 
            data = About.objects.last() 
            if news != None:
                context = {
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
                }

                if news:
                    for i in range(min(5, len(news))):
                        context[f"news_n{i}"] = {
                            "title": news[i].title,
                            "slug": news[i].slug,
                            "url": f"{domain}",
                        }
                return HttpResponse(json.dumps(context), content_type='application/json')
            else:
                context = {
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
                }
                return HttpResponse(json.dumps(context), content_type='application/json')

    return HttpResponse(json.dumps({"about":False}), content_type='application/json')


 
 
    
            


    
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
    # Xeberlerden son 3-u 
    news = None
    if NewsModel.objects.all().count() >= 5: news = NewsModel.objects.order_by('-id').all()[0:5]  

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
                    "news_n0": {
                        "title": news[0].title,
                        "slug": news[0].slug, 
                        "url": request.META['REMOTE_HOST'],
                    },
                    "news_n1": { 
                        "title": news[1].title,
                        "slug": news[1].slug, 
                        "url": request.META['REMOTE_HOST'],
                    },
                    "news_n2": { 
                        "title": news[2].title,
                        "slug": news[2].slug, 
                        "url": request.META['REMOTE_HOST'],
                    },
                    "news_n3": { 
                        "title": news[3].title,
                        "slug": news[3].slug, 
                        "url": request.META['REMOTE_HOST'],
                    },
                    "news_n4": { 
                        "title": news[4].title,
                        "slug": news[4].slug, 
                        "url": request.META['REMOTE_HOST'],
                    },
                }
                return HttpResponse(json.dumps(context), content_type='application/json')
    return HttpResponse(json.dumps({"about":False}), content_type='application/json')


 
 
    
            


    
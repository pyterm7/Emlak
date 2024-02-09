from django.shortcuts import render, redirect
from News.models import NewsModel
from NewsTag.models import NewsTagModel

def NewsDetail(request, news):
    data = {}
    if NewsTagModel.objects.all().count() > 5:
        data['tags'] = NewsTagModel.objects.all()[0:5]
        
    if news_detail := NewsModel.objects.filter(slug=news).first():
        data["news_detail"] = news_detail
        return render(request, "news-detail.html", context=data)



def AllNews(request):
    all_news = NewsModel.objects.filter(is_active=True)
    if all_news.count() == 0: return redirect("home-page")
    return render(request, "news.html", context={"news":all_news})



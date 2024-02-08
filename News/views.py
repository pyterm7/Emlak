from django.shortcuts import render
from News.models import NewsModel
from NewsTag.models import NewsTagModel

def NewsDetail(request, news):
    data = {}
    if NewsTagModel.objects.all().count() > 5:
        data['tags'] = NewsTagModel.objects.all()[0:5]
        
    if news_detail := NewsModel.objects.filter(slug=news).first():
        data["news_detail"] = news_detail
        return render(request, "news-detail.html", context=data)







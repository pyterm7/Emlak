import json 
from math import ceil
from django.conf import settings
from Auth.models import CustomUser 
from django.contrib import messages
from django.http import HttpResponse
from NewsTag.models import NewsTagModel
from django.shortcuts import render, redirect
from News.models import NewsModel, LikedNews, CommentNews
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

def NewsDetail(request, news):
    data = {}
 
    if NewsTagModel.objects.all().count() > 5:
        data['tags'] = NewsTagModel.objects.all()
        
    if news_detail := NewsModel.objects.filter(slug=news).first():
        comments = CommentNews.objects.filter(news=news_detail).order_by("-id")
        data['comments_count'] = comments.count()
        if comments: data['comments'] = comments
        
        likes_count = LikedNews.objects.filter(news=news_detail).count()
        if user:=CustomUser.objects.filter(id=request.user.id).first():
            liked_it = LikedNews.objects.filter(news=news_detail, user=user).first()
            if liked_it: data["liked_it"] = True
        data["news_detail"] = news_detail
        data["likes_count"] = likes_count
        data["share_url"] = request.build_absolute_uri()
        return render(request, "news-detail.html", context=data)



def AllNews(request):
    data = {}
    page = request.GET.get("page", 1)

    if filter_tag := request.GET.get("tag", "").strip():
        tag = NewsTagModel.objects.filter(name=filter_tag).first() 
        all_news = NewsModel.objects.filter(tags__id = tag.id).order_by("-id")
    else:
        all_news = NewsModel.objects.filter(is_active=True).order_by("-id")
    
    if all_news.count() == 0: return redirect("home-page")
    try: page = int(page)
    except: page = 1

    limit = 9
    total_news = all_news.count() 
    total_page = 1

    if total_news != 0: total_page = ceil(total_news / limit)

    if page > total_page: return redirect("all-news")
    elif page < 1: return redirect("all-news")

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

    
    data["news"] = all_news[page_start:page_end] 
    data["aktiv_page"] = page 
    data["page_numbers"] = page_numbers
    
    return render(request, "news.html", context=data)



# @login_required(login_url="sign-in-page", redirect_field_name=None)
# def LikeNews(request, id):
#     user = CustomUser.objects.filter(id=request.user.id).first()
#     if user:
#         if news := NewsModel.objects.filter(id=id).first():
#             if liked_it := LikedNews.objects.filter(user=user, news=news).first():
#                 liked_it.delete()
#                 messages.success(request, "Xəbər bəyəndiklərinizin sırasından çıxarıldı.")
#                 return redirect("news-detail", news=news.slug)
#             LikedNews.objects.create(user=user, news=news)
#             messages.success(request, "Bu xəbər bəyəndiklərinizin sırasına əlavə edildi.")
#             return redirect("news-detail", news=news.slug)
#     messages.info(request, "İcazəsiz cəhd.")
#     return redirect("home-page")


def LikeNews(request, id):
    # AJAX
    user = CustomUser.objects.filter(id=request.user.id).first()
    if user:
        if news := NewsModel.objects.filter(id=id).first(): 
            if liked_it := LikedNews.objects.filter(user=user, news=news).first():
                liked_it.delete()
                like_count = LikedNews.objects.filter(news=news).count()
                return HttpResponse(json.dumps({"count":like_count, "deleted":True, "liked":False}), content_type='application/json') 
            LikedNews.objects.create(user=user, news=news) 
            like_count = LikedNews.objects.filter(news=news).count()
            return HttpResponse(json.dumps({"count":like_count, "deleted":False, "liked":True}), content_type='application/json') 
    return HttpResponse(json.dumps({"error":True, "href": settings.SITE_URL + "/auth/sign-in/" }), content_type='application/json') 




@login_required(login_url="sign-in-page", redirect_field_name=None)
def CreateNewComment(request, id):
    if request.POST:
        comment = request.POST.get("your_comment")
        news = NewsModel.objects.filter(id=id).first()
        if news:
            user = CustomUser.objects.filter(id=request.user.id).first()
            if user:
                comment = comment.strip()
                if len(comment) < 3:
                    messages.info(request, "Şərh minimum 3 simvoldan ibarət olmalıdır.")
                    return redirect("news-detail", news=news.slug)
                CommentNews.objects.create(news=news, author=user, comment=comment)
                messages.success(request, "Şərhiniz qeydə alındı.")
                return redirect("news-detail", news=news.slug)
    messages.info(request, "İcazəsiz cəhd.")
    return redirect("home-page")







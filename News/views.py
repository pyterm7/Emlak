from django.shortcuts import render, redirect
from News.models import NewsModel, LikedNews, CommentNews
from NewsTag.models import NewsTagModel
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from Auth.models import CustomUser 
from django.contrib import messages

def NewsDetail(request, news):
    data = {}
 
    if NewsTagModel.objects.all().count() > 5:
        data['tags'] = NewsTagModel.objects.all()[0:5]
        
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
    all_news = NewsModel.objects.filter(is_active=True)
    if all_news.count() == 0: return redirect("home-page")
    return render(request, "news.html", context={"news":all_news})



@login_required(login_url="sign-in-page", redirect_field_name=None)
def LikeNews(request, id):
    user = CustomUser.objects.filter(id=request.user.id).first()
    if user:
        if news := NewsModel.objects.filter(id=id).first():
            if liked_it := LikedNews.objects.filter(user=user, news=news).first():
                liked_it.delete()
                messages.success(request, "Xəbər bəyəndiklərinizin sırasından çıxarıldı.")
                return redirect("news-detail", news=news.slug)
            LikedNews.objects.create(user=user, news=news)
            messages.success(request, "Bu xəbər bəyəndiklərinizin sırasına əlavə edildi.")
            return redirect("news-detail", news=news.slug)
    messages.info(request, "İcazəsiz cəhd.")
    return redirect("home-page")


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







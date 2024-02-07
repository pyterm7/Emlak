from django.shortcuts import render


def NewsDetail(request):
    return render(request, "news-detail.html")
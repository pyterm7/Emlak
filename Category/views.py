from django.shortcuts import render
from Category.models import CategoryModel

def MakeCategory(html_text, categories):
    html_text += "<ul class='reset-css'>"
    for category in categories:
        html_text += f"<li> {category.name}"
        if categories:=CategoryModel.objects.filter(parent=category):
            html_text += MakeCategory(html_text="", categories=categories)
        html_text += "</li>"
    html_text += "</ul>"
    return html_text


def ShowCategories(request):  
    categories = CategoryModel.objects.filter(parent__isnull=True) 
    html_text = MakeCategory("", categories) 
    return render(request, "category.html", context={"html_text":html_text})
 
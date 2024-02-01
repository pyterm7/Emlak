import os
from PIL import Image
from Auth.models import CustomUser
from django.contrib import messages
from django.shortcuts import render, redirect
from validator_collection import validators, checkers
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from string import ascii_lowercase, ascii_uppercase, digits, ascii_letters
from django.conf import settings

def SignIn(request):
    if request.user.is_authenticated: return redirect("home-page")
    
    if request.POST:
        phone = request.POST.get("login_phone")
        password = request.POST.get("login_password")
        user = authenticate(phone=phone, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Hesabınıza giriş etdiniz.")
            return redirect("home-page")
        else:
            messages.info(request, "Xəta oldu. Yenidən cəhd edin.")
            return redirect("sign-in-page")
    return render(request, "sign-in.html")


def SignUp(request):
    if request.user.is_authenticated: return redirect("home-page") 

    if request.POST:
        data = {}
        name = request.POST.get("name", False)
        surname = request.POST.get("surname", False)
        phone = request.POST.get("phone", False)
        location = request.POST.get("loc", False)
        password = request.POST.get("password", False)
        repassword = request.POST.get("repassword", False) 

        data["name"] = name
        data["surname"] = surname
        data["phone"] = phone
        data["location"] = location

        if password and repassword: 
            if password != repassword:
                messages.info(request, "Şifrələr eyni deyil.")
                return render(request, "sign-up.html", context=data) 
            if len(password) < 8:
                messages.info(request, "Şifrə minimum 8 simvoldan ibarət olmalıdır.")
                return render(request, "sign-up.html", context=data) 
            
            has_lower = False
            has_upper = False 
            has_digit = False
            has_other_char = False
            for char in password:
                if char in ascii_lowercase:
                    has_lower = True 
                if char in ascii_uppercase:
                    has_upper = True
                if char in digits:
                    has_digit = True
                if char not in f"{ascii_letters}{digits}":
                    has_other_char = True
            if not has_lower:
                messages.info(request, "Şifrədə ən az 1 kiçik hərf olmalıdır.")
                return render(request, "sign-up.html", context=data)
            if not has_upper:
                messages.info(request, "Şifrədə ən az 1 böyük hərf olmalıdır.")
                return render(request, "sign-up.html", context=data)
            if not has_digit:
                messages.info(request, "Şifrədə ən az 1 rəqəm olmalıdır.")
                return render(request, "sign-up.html", context=data)
            if has_other_char:
                messages.info(request, f"Şifrədə yalnız bu hərflər {ascii_lowercase} {ascii_uppercase}, və rəqəmlər olmalıdır.")
                return render(request, "sign-up.html", context=data)

            if CustomUser.objects.filter(phone=phone).first():
                messages.info(request, f"{phone} ilə qeydiyyatdan keçmək mümkün olmadı.")
                return render(request, "sign-up.html", context=data)
            if len(name) < 3 and len(surname) < 3:
                messages.info(request, f"Ad və soyad minimum 3 simvoldan ibarət olmalıdır.")
                return render(request, "sign-up.html", context=data)
            if len(location) < 3:
                messages.info(request, "Ünvan adı minimum 3 simvoldan ibarət olmalıdır.")
                return render(request, "sign-up.html", context=data)
            try:
                new_user = CustomUser(
                    name=name.title(), 
                    surname=surname.title(),
                    phone=phone,
                    location=location, )
                new_user.set_password(password)
                new_user.save()
                messages.success(request, "Qeydiyyat tamamlandı. Hesabınıza daxil ola bilərsiniz.")
                return redirect("sign-in-page")
            except:
                messages.info(request, "Qeydiyyat prosesində xəta oldu.")
                return render(request, "sign-up.html", context=data)
        else:
            messages.info(request, "Şifrə və şifrə təkrarını düzgün daxil edin.")
            return render(request, "sign-up.html", context=data)
    return render(request, "sign-up.html")


def SignOut(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Hesabınızdan çıxış etdiniz.")
    else: 
        messages.info(request, "İcazəsiz cəhd.")
    return redirect("home-page")

@login_required(login_url="sign-in-page", redirect_field_name=None)
def MyAccount(request):
    if not request.user.is_staff: return redirect("home-page") 
    data = {}
    if my_account := CustomUser.objects.filter(phone=request.user.phone).first(): data["my_account"] = my_account 
    return render(request, "my-account.html", context=data)



@login_required(login_url="sign-in-page", redirect_field_name=None)
def SetSocialAccount(request):
    if not request.user.is_staff: return redirect("home-page")
    if request.POST:
        account_instagram = request.POST.get("account_instagram", False)
        account_facebook = request.POST.get("account_facebook", False)
        account_twitter = request.POST.get("account_twitter", False)
        account_youtube = request.POST.get("account_youtube", False)
        account_pinterest = request.POST.get("account_pinterest", False)
        account_vimeo = request.POST.get("account_vimeo", False)
        account_tiktok = request.POST.get("account_tiktok", False)
        
        if user := CustomUser.objects.filter(id=request.user.id).first():
            try:
                if account_instagram: 
                    if checkers.is_url(account_instagram): user.instagram = account_instagram
                    else: 
                        messages.info(request, "İnstagram üçün daxil edilən url doğru deyil.")
                        return redirect("my-account")

                if account_facebook: 
                    if checkers.is_url(account_facebook): user.facebook = account_facebook
                    else: 
                        messages.info(request, "Facebook üçün daxil edilən url doğru deyil.")
                        return redirect("my-account")
                    
                if account_twitter: 
                    if checkers.is_url(account_twitter): user.twitter = account_twitter
                    else: 
                        messages.info(request, "Twitter üçün daxil edilən url doğru deyil.")
                        return redirect("my-account")
                
                if account_youtube: 
                    if checkers.is_url(account_youtube): user.youtube = account_youtube
                    else: 
                        messages.info(request, "YouTube üçün daxil edilən url doğru deyil.")
                        return redirect("my-account")
                    
                if account_pinterest: 
                    if checkers.is_url(account_pinterest): user.pinterest = account_pinterest
                    else: 
                        messages.info(request, "Pinterest üçün daxil edilən url doğru deyil.")
                        return redirect("my-account")
                    
                if account_vimeo: 
                    if checkers.is_url(account_vimeo): user.vimeo = account_vimeo
                    else: 
                        messages.info(request, "Vimeo üçün daxil edilən url doğru deyil.")
                        return redirect("my-account")
                
                if account_tiktok: 
                    if checkers.is_url(account_tiktok): user.tiktok = account_tiktok
                    else: 
                        messages.info(request, "TikTok üçün daxil edilən url doğru deyil.")
                        return redirect("my-account")
                
                user.save()
                messages.success(request, "Sosial hesablar güncəlləndi.")
                return redirect("my-account") 
            except: messages.info(request, "Xəta oldu.")
        else: messages.info(request, "Xəta oldu.")
    return redirect("my-account")


@login_required(login_url="sign-in-page", redirect_field_name=None)
def ChangeAvatar(request):
    if not request.user.is_staff:
        messages.info(request, "İcazəsiz cəhd.")
        return redirect("home-page")

    if request.POST and request.FILES:
        if user := CustomUser.objects.filter(id=request.user.id).first():
            avatar = request.FILES['user_avatar']
            img = Image.open(avatar)
            width = img.width
            height = img.height
            if width < 270 or height < 330:
                messages.info(request, "Profil şəkli minimum 270x330 ölçüdə olmalıdır.")
                return redirect("my-account")
            else: 
                left = (width - 270) // 2
                top = (height - 330) // 2
                right = (width + 270) // 2
                bottom = (height + 330) // 2
                cropped_image = img.crop((left, top, right, bottom))
                save_path = os.path.join(settings.MEDIA_ROOT, 'profile', avatar.name)
                cropped_image.save(save_path)

                user.avatar = save_path
                user.save()
                messages.success(request, "Profil şəkli güncəlləndi.")
                return redirect("my-account")
        else:
            messages.info(request, "İcazəsiz cəhd.")
            return redirect("home-page")
    messages.info(request, "İcazəsiz cəhd.")
    return redirect("my-account")






import os 
import re
from PIL import Image
from io import BytesIO
from random import shuffle
from City.models import City
from django.conf import settings
from Auth.models import CustomUser
from django.contrib import messages
from django.shortcuts import render, redirect
from validator_collection import validators, checkers
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from string import ascii_lowercase, ascii_uppercase, digits, ascii_letters  

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
     
    return render(request, "sign-up.html" )
 
@login_required(login_url="sign-in-page", redirect_field_name=None)
def SignOut(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Hesabınızdan çıxış etdiniz.")
    else: messages.info(request, "İcazəsiz cəhd.")
    return redirect("home-page")

@login_required(login_url="sign-in-page", redirect_field_name=None)
def MyAccount(request):
    if not request.user.is_staff: return redirect("home-page") 
    data = {}
    if cities := City.objects.all(): data['cities'] = cities
    if my_account := CustomUser.objects.filter(phone=request.user.phone).first(): data["my_account"] = my_account 
    if our_team := CustomUser.objects.filter(parent_agent__id=request.user.id).all(): data["our_team"] = our_team
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
            img = Image.open(BytesIO(avatar.read()))
            width = img.width
            height = img.height
            if width < 270 or height < 330:
                messages.info(request, "Profil şəkli minimum 270x330 ölçüdə olmalıdır.")
                return redirect("my-account")
            else:
                random_chars = list(ascii_lowercase) 
                shuffle(random_chars) 
                random_str = "".join(random_chars) 
                try: 
                    if width > 270: width = (width - (width % 270))
                    if height > 330: height = (height - (height % 330))
                    left = 0
                    top = 0 
                    if width>height: width = height
                    else: height = width
                    right = width
                    bottom = height
                    cropped_image = img.crop((left, top, right, bottom))
                    cropped_image = cropped_image.resize((330, 330), Image.Resampling.LANCZOS)
                    new_image_name = f"{user.phone[1:]}-{random_str[0:4]}.{img.format.lower()}"
                    new_path = os.path.join(settings.MEDIA_ROOT, 'profile', new_image_name) 
                    cropped_image.save(new_path)
                    user.avatar = new_path 
                    user.save()
                    messages.success(request, "Profil şəkli güncəlləndi.") 
                    return redirect("my-account") 
                except Exception as e:  
                    messages.info(request, f"Xəta oldu. {e}")  
                    return redirect("my-account") 

        else:
            messages.info(request, "İcazəsiz cəhd.")
            return redirect("home-page")
    messages.info(request, "İcazəsiz cəhd.")
    return redirect("my-account")

@login_required(login_url="sign-in-page", redirect_field_name=None)
def EditAccount(request):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not request.user.is_staff: return redirect("home-page") 
    if user := CustomUser.objects.filter(id=request.user.id).first():
        if request.POST:
            position = request.POST.get("edit_position", user.position)
            bio = request.POST.get("edit_bio", user.bio)
            email = request.POST.get("edit_email", user.email)

            if len(position) > 100:
                messages.info(request, "Vəzifə maksimum 100 simvoldan ibarət olmalıdır.")
                return redirect("my-account")
            
            if len(bio) > 1000:
                messages.info(request, "Haqqında məlumat maksimum 1000 simvoldan ibarət olmalıdır.")
                return redirect("my-account")
            
            if not (re.fullmatch(regex, email)):
                messages.info(request, "E-poçt doğru daxil edilməyib.")
                return redirect("my-account")
            
            try:
                user.position = position 
                user.bio = bio 
                user.email = email
                user.save()
                messages.success(request, "Məlumatlar uğurla güncəlləndi.")
            except:
                messages.info(request, "Xəta oldu. Daha sonra yenidən cəhd edin.")
            return redirect("my-account")

    messages.info(request, "İcazəsiz cəhd.")
    return redirect("home-page")

@login_required(login_url="sign-in-page", redirect_field_name=None)
def GetPassport(request):
    if request.user.is_staff: return redirect("home-page")  

    if request.POST and request.FILES:
        passport = request.FILES['passport']

        passport_byte = passport.size 
        if passport_byte / (1024 * 1024) > 2:
            messages.info(request, "Şəklin həcmi maksimum 2MB olmalıdır.")
            return redirect("get-passport")

        img = Image.open(passport)
        width = img.width
        height = img.height
        if width < 400 or height < 300:
            messages.info(request, "Şəklin ölçüləri minimum 400x300 olmalıdır.")
            return redirect("get-passport")
        
        if user:= CustomUser.objects.filter(id=request.user.id).first():
            try:
                user.passport = passport 
                user.save()
                messages.success(request, "Müraciətiniz qeydə alındı. Tezliklə telefonunuza təsdiq mesajı göndəriləcək.")
                return redirect("home-page")
            except:
                messages.info(request, "Müraciət qeydə alınmadı. Daha sonra yenidən cəhd edin.")
                return redirect("get-passport")
        messages.info(request, "İcazəsiz cəhd.")
        return redirect("home-page")

    return render(request, "get-passport.html")

@login_required(login_url="sign-in-page", redirect_field_name=None)
def AddUser2AgencyTeam(request):
    if not CustomUser.objects.filter(id=request.user.id).first():
        messages.info(request, "İcazəsiz cəhd.")
        return redirect("home-page")
    
    agent = CustomUser.objects.filter(id=request.user.id).first()

    if not request.user.is_staff: 
        messages.info(request, "İcazəsiz cəhd.")
        return redirect("home-page") 
    
    if request.POST:
        name = request.POST.get("agent_user_name", False)
        surname = request.POST.get("agent_user_surname", False)
        phone = request.POST.get("agent_user_phone", False)
        location = request.POST.get("agent_user_location", False)
        password = request.POST.get("agent_user_password", False)
        repassword = request.POST.get("agent_user_repassword", False)  

        city = City.objects.filter(id=location).first()

        if password != repassword:
                messages.info(request, "Şifrələr eyni deyil.")
                return redirect("my-account")
        
        if len(password) < 8:
            messages.info(request, "Şifrə minimum 8 simvoldan ibarət olmalıdır.")
            return redirect("my-account")
        
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
            return redirect("my-account")
        if not has_upper:
            messages.info(request, "Şifrədə ən az 1 böyük hərf olmalıdır.")
            return redirect("my-account")
        if not has_digit:
            messages.info(request, "Şifrədə ən az 1 rəqəm olmalıdır.")
            return redirect("my-account")
        if has_other_char:
            messages.info(request, f"Şifrədə yalnız bu hərflər {ascii_lowercase} {ascii_uppercase}, və rəqəmlər olmalıdır.")
            return redirect("my-account")

        if CustomUser.objects.filter(phone=phone).first():
            messages.info(request, f"{phone} ilə qeydiyyat mümkün olmadı.")
            return redirect("my-account")
        if len(name) < 3 and len(surname) < 3:
            messages.info(request, f"Ad və soyad minimum 3 simvoldan ibarət olmalıdır.")
            return redirect("my-account")
        
        if not city:
            messages.info(request, f"Ünvan seçimində xəta oldu.")
            return redirect("my-account")
        
        try:
            new_user = CustomUser(parent_agent = agent, name=name.title(), surname=surname.title(), phone=phone, location=city.name)
            new_user.set_password(password)
            new_user.save()
            messages.success(request, "Agentliyə istifadəçi əlavə edildi.")
            return redirect("my-account")
        except:
            messages.info(request, "İstifadəçi əlavə edilmədi. Yenidən cəhd edin və ya texniki dəstəyə bildirin.")
            return redirect("my-account")

    messages.info(request, "İcazəsiz cəhd.")
    return redirect("home-page")


def SeeUser(request):
    phone = request.GET.get("phone")
    phone = f"+{phone}"
    user = CustomUser.objects.filter(phone=phone).first()
    if user:
        our_team = CustomUser.objects.filter(parent_agent__id=user.id).all() 
        data = {"user":user}
        if our_team.count()>0: data["our_team"] = our_team
        return render(request, "user.html", context=data) 
    messages.info(request, "İcazəsiz cəhd.")
    return redirect("home-page")




import os 
from django.db import models
from City.models import City
from django.contrib import auth
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from PIL import Image
from string import ascii_lowercase
from random import shuffle

class CustomUserManager(BaseUserManager):
    use_in_migrations = True 
    def _create_user(self, phone, password, **extra_fields):
        user = self.model(phone = phone, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True) 
        if extra_fields.get("is_staff") is not True: raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True: raise ValueError("Superuser must have is_superuser=True.") 
        return self._create_user(phone, password, **extra_fields)

    def with_perm( self, perm, is_active=True, include_superusers=True, backend=None, obj=None ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1: backend, _ = backends[0]
            else: raise ValueError( "You have multiple authentication backends configured and "  "therefore must provide the `backend` argument." )
        elif not isinstance(backend, str): raise TypeError( "backend must be a dotted import path string (got %r)." % backend )
        else: backend = auth.load_backend(backend)

        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()



class CustomUser(AbstractBaseUser, PermissionsMixin):

    parent_agent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name="Daxil olduğu agentlik", blank=True, null=True, related_name="agency_team")

    avatar = models.ImageField(blank=True, null=True, verbose_name = "Profil şəkli", upload_to="profile/")
    passport = models.ImageField(blank=True, null=True, verbose_name = "Şəxsiyyət vəsiqəsi", upload_to="passport/")

    name = models.CharField(max_length = 50, verbose_name = "Ad", blank = True, null = True)
    surname = models.CharField(max_length = 50, verbose_name = "Soyad", blank = True, null = True)

    position = models.CharField(max_length = 100, verbose_name = "Vəzifə", blank = True, null = True)

    username = models.CharField(max_length = 50, verbose_name = "İstifadəçi adı", blank = True, null = True)
    phone = models.CharField(max_length = 13, verbose_name = "Telefon", unique = True)
    email = models.EmailField(verbose_name = "E-poçt", blank = True, null = True)
    bio = models.TextField(verbose_name = "Haqqında", blank=True, null=True)

    facebook = models.CharField(max_length = 225, verbose_name = "Facebook", blank=True, null=True)
    instagram = models.CharField(max_length = 225, verbose_name = "İnstagram", blank=True, null=True)
    youtube = models.CharField(max_length = 225, verbose_name = "YouTube", blank=True, null=True)
    twitter = models.CharField(max_length = 225, verbose_name = "Twitter", blank=True, null=True)
    tiktok = models.CharField(max_length = 225, verbose_name = "TikTok", blank=True, null=True)
    vimeo = models.CharField(max_length = 225, verbose_name = "Vimeo", blank=True, null=True)
    pinterest = models.CharField(max_length = 225, verbose_name = "Pinterest", blank=True, null=True)

    voen = models.CharField(max_length = 100, blank=True, null = True, verbose_name = "Vöen")

    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name = "İş ünvanı", blank = True, null = True) 
    location = models.CharField(max_length = 225, verbose_name="Yaşadığı ünvan", blank=True, null=True)

    is_active = models.BooleanField(default = True, verbose_name = "Aktiv kimi işarələ")

    is_staff = models.BooleanField(default = False, verbose_name = "Agent kimi işarələ")
    is_superuser = models.BooleanField(default = False, verbose_name = "Admin kimi işarələ")

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self) -> str: return self.phone

    def save(self, **kwargs):
        super(CustomUser, self).save(**kwargs)
        if self.avatar:
            random_chars = list(ascii_lowercase) 
            shuffle(random_chars) 
            random_str = "".join(random_chars) 
            try:
                img = Image.open(self.avatar.path)
                width = img.width
                height = img.height
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
                new_image_name = f"{self.phone[1:]}-{random_str[0:4]}.{img.format.lower()}"
                new_path = os.path.join(settings.MEDIA_ROOT, 'profile', new_image_name)
                # self.avatar.delete()
                cropped_image.save(new_path)
                self.avatar = new_path
                super(CustomUser, self).save(**kwargs)
            except: pass
            
            

    class Meta:  
        verbose_name = "istifadəçi"
        verbose_name_plural = "İstifadəçilər"

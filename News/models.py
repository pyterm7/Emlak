from collections.abc import Iterable
from django.db import models
from tinymce.models import HTMLField
from Auth.models import CustomUser
from PIL import Image
from NewsTag.models import NewsTagModel
from string import ascii_lowercase

class NewsModel(models.Model):
    author = models.ForeignKey(CustomUser, verbose_name = "Müəllif", on_delete=models.CASCADE)
    cover = models.ImageField(blank=True, null=True, verbose_name="Şəkil", upload_to="news-covers/")
    title = models.CharField(max_length = 255, verbose_name = "Başlıq")
    description = HTMLField(verbose_name="Məzmun")
    is_active = models.BooleanField(default = False, verbose_name = "Aktiv")
    slug = models.CharField(max_length=255, verbose_name="SLUG", blank=True, null=True)

    tags = models.ManyToManyField(to=NewsTagModel, related_name="tags", blank=True, verbose_name="Teqlər")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs) -> None:
        new_slug = ""
        self.slug = self.title.lower().replace("ü", "u").replace("ç", "c").replace("ş", "s").replace("ğ","g").replace("ö","o").replace("ı", "i").replace("ə", "e").replace(" ", "-")
        for letter in self.slug:
            if letter in f"{ascii_lowercase}0123456789-":
                new_slug += letter 
        try:
            txt = new_slug
            new_txt = " "
            for i in range(0, len(txt)): 
                if new_txt[len(new_txt)-1] == "-" and txt[i] == "-": continue
                else: new_txt+= txt[i]
            new_slug = new_txt
        except: pass
        

        self.slug = new_slug.strip("-").strip(" ")
        super().save(*args, **kwargs)

        img = Image.open(self.cover.path) 
        if img.height > 520 or img.width > 770:
            new_img = (770, 520)
            img.thumbnail(new_img)
            img.save(self.cover.path)



    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name_plural = "Xəbərlər"


class LikedNews(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="İstifadəçi")
    news = models.ForeignKey(NewsModel, on_delete=models.CASCADE, verbose_name="Xəbər")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.phone 
    
    class Meta:
        verbose_name_plural = "Bəyənilmiş xəbərlər"


class CommentNews(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Müəllif")
    news = models.ForeignKey(NewsModel, on_delete=models.CASCADE, verbose_name="Xəbər")

    comment = models.CharField(max_length = 255, verbose_name = "Şərh")


    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        if len(self.comment) > 30: return self.comment[0:30] + "..."
        return self.comment
    
    class Meta: verbose_name_plural = "Şərhlər"










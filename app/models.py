from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField("タイトル", max_length=200)
    content = models.TextField("本文")
    address = models.TextField("住所")
    latitude = models.FloatField("緯度")
    longitude = models.FloatField("経度")
    problemCategory = models.TextField("カテゴリー")
    peopleNum = models.IntegerField("募集人員")
    purpose = models.TextField("目的")
    organization = models.TextField("搭載者種別")
    problemSize = models.TextField("規模")
    status = models.TextField("募集状態")
    created = models.DateTimeField("作成日", default=timezone.now)


    def __str__(self):
        return self.title

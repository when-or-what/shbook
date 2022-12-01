import datetime
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


class UserInfo(models.Model):
    # UserID = models.AutoField(primary_key=True)
    # Username = models.CharField(max_length=20)
    # password = models.CharField(max_length=20)
    # Email = models.EmailField(max_length=30)
    # Img = models.CharField(max_length=40, null=True, blank=True)
    # verification_code = models.CharField(max_length=10, null=True, blank=True)
    # 用户名，用户注册时输入的内容，是主键
    user_id = models.CharField(primary_key=True, max_length=15)
    password = models.CharField(max_length=64)  # 密码密文，采用SHA256算法加密，定长64位字符串
    # 用户邮箱，注册时输入的内容，必须具有唯一性
    email = models.EmailField(max_length=256, unique=True)
    img_path = models.CharField(
        max_length=256, null=True, default=r'D:\DjangoPro\transaction\secondhand_book\static\head\user.webp')  # 用户头像路径
    ver_code = models.CharField(max_length=6, null=True, blank=True)  # 验证码


class Goods(models.Model):
    # Commodity_ID = models.AutoField(primary_key=True)
    # Commodity_Name = models.CharField(max_length=120, null=True, blank=True)
    # Price = models.IntegerField()
    # Contact_QQ = models.DecimalField(max_digits=11, decimal_places=0)
    # Note = models.CharField(max_length=120)
    # Date = models.DateTimeField(auto_now=False, auto_now_add=True)
    # UserID = models.ForeignKey('UserInfo', related_name='UserID_Goods', on_delete=models.CASCADE)
    # Img = models.CharField(max_length=40, null=True, blank=True)
    commodity_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        'UserInfo', related_name='UserInfo_Goods', on_delete=models.CASCADE, max_length=15)
    commodity_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user_contact = models.CharField(max_length=100)
    note = models.CharField(max_length=120, null=True, default='请添加描述')
    due_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    picture = models.CharField(
        max_length=256, null=True, default='D:/DjangoPro/transaction/secondhand_book/static/homepage/img/Math.webp')  # 商品的图片路径

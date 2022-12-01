# -*- coding: gbk -*-
from django.test import TestCase

# Create your tests here.
from secondhand_book.models import *
# UserInfo:
# UserID = models.AutoField(primary_key=True)
# Username = models.CharField(max_length=20)
# password = models.CharField(max_length=20)
# Email = models.EmailField(max_length=30)

# Goods:
# Commodity_ID = models.AutoField(primary_key=True)
# Price = models.IntegerField()
# Contact_QQ = models.DecimalField(max_digits=11, decimal_places=0)
# Note = models.CharField(max_length=120)
# Date = models.DateTimeField(auto_now=False, auto_now_add=True)
# UserID = models.ForeignKey('UserInfo', related_name='UserID_Goods', on_delete=models.CASCADE)
# Commodity_Name = models.CharField(max_length=120, null=True, blank=True)
if __name__ == '__main__':
    UserInfo.objects.create(
        Username='麻阔', password='123456', Email='765019392@qq.com')
    q = UserInfo.objects.filter(Username='麻阔')
    newImg = str(q[0].UserID) + '.jpg'
    q.update(Img=newImg)

    Goods.objects.create(Price=25, Contact_QQ=765019392,
                         Note='无', UserID=q[0], Commodity_Name='高等数学')
    q = Goods.objects.filter(Commodity_Name='高等数学')

    UserInfo.objects.create(Username='刘忠东',
                            password='123456', Email='2328954508@qq.com')
    q = UserInfo.objects.filter(Username='刘忠东')
    newImg = str(q[0].UserID) + '.jpg'
    q.update(Img=newImg)

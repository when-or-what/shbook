from django.urls import path
from . import views

app = 'secondhand_book'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('findpswd/', views.findpswd, name='findpswd'),
    path('login_view/', views.login_view, name='login_view'),
    path('enter_ver_code/', views.enter_ver_code, name='enter_ver_code'),
    path('homepage/', views.homepage, name='homepage'),
    path('person_info/', views.person_info, name='person_info'),
    path('goods_detail&id=<int:id>/', views.goods_detail, name='goods_detail'),
    path('homepage&keyword=<str:keyword>/', views.homepage),
    path('login/', views.login),
    path('changepht/', views.changepht, name='changepht'),
]

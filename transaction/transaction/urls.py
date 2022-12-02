"""transaction URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from secondhand_book import views
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path('', views.login),
    path('login/', views.login),
    path('homepage/', views.homepage),
    path('homepage&keyword=<str:keyword>/', views.homepage),
    path('index/', views.index),
    path('individual_info/', views.personal_info),
    path('person_info/', views.person_info, name='person_info'),
    path('changepht/', views.changepht, name='changepht'),
    path('changepswd/', views.changepswd, name='changepswd'),
    path('changename/', views.changename, name='changename'),
    path('mygoods/', views.mygoods, name='mygoods'),
    path('goods_detail&id=<int:id>/', views.goods_detail, name='goods_detail'),
    path('secondhand_book/', include('secondhand_book.urls')),
]

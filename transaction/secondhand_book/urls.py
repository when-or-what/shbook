from django.urls import path
from . import views

app = 'secondhand_book'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('findpswd/', views.findpswd, name='findpswd'),
    path('login_view/', views.login_view, name='login_view'),
    path('enter_ver_code/', views.enter_ver_code, name='enter_ver_code'),
]

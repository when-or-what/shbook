import json
import os.path
from django.core.exceptions import *
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from secondhand_book.models import *
from django.core.mail import send_mail
import random
import string
# Create your views here.


def index(request):
    return redirect('../homepage/')


def login_view(request):
    '''
    登录页面
    '''
    return render(request, 'pages/login.html')


def register(request):
    '''
    注册页面
    '''
    if request.method == 'GET':
        return render(request, 'pages/register.html')

    email = request.POST.get('email')
    username = request.POST.get('username')
    pswd = request.POST.get('pswd')
    print(email, username, pswd)

    userinfo = UserInfo.objects.filter(user_id=username)
    if not userinfo.exists():
        # 不存在则可以注册
        # 再判断邮箱是否唯一
        eml = UserInfo.objects.filter(email=email)
        if not eml.exists():
            # 如果邮箱也不存在，那么才可以注册
            UserInfo.objects.create(
                user_id=username,
                email=email,
                password=pswd
            )
            # 如果成功就返回登录页面
            return redirect('../login_view')

    # 否则就在注册页面
    return redirect('../register')


def findpswd(request):
    '''
    找回密码页面
    '''
    if request.method == 'GET':
        errmsg = request.session.get('errmsg')
        return render(request, 'pages/findpw.html', {'errmsg': errmsg})

    email = request.POST.get('email')
    userinfo = UserInfo.objects.filter(email=email)
    if not userinfo.exists():
        return render(request, 'pages/findpw.html', {'errmsg': '请重新输入'})

    request.session['email'] = str(email)
    # 生成随机验证码
    s_code = string.ascii_letters+string.digits
    code = random.sample(s_code, 6)
    vcode = "".join(code)
    # 验证码存到数据库
    UserInfo.objects.filter(email=email).update(ver_code=vcode)
    # 发送验证码
    message_text = '你正在登录校园二手书交易平台，验证码为%s' % (vcode)
    send_mail(subject='你好', message=message_text, from_email=email,
              recipient_list=[email], fail_silently=False)
    response = redirect('../enter_ver_code/')  # 跳到输入验证码的界面
    return response


def login(request):
    if request.method == 'GET':
        rstpwd_message = request.session.get('rstpwd_message')
        message = '欢迎'
        return render(request, 'pages/login.html', {'message': message, 'rstpwd_message': rstpwd_message})
    if request.method == 'POST':
        ID = request.POST.get("username")
        pwd = str(request.POST.get('password'))
        try:
            user = UserInfo.objects.get(user_id=ID)
            if pwd == user.password:
                request.session['is_login'] = True
                request.session['ID'] = user.user_id
                request.session.set_expiry(0)
                response = redirect('../homepage/')
                response.set_cookie('ID', ID)
                # message_text = '你正在登录校园二手书交易平台，我们向你发送这个邮件进行验证以保证是你本人登录，此上'
                # send_mail(subject='你好', message=message_text, from_email='765019392@qq.com',
                #           recipient_list=['765019392@qq.com'], fail_silently=False)
                return response
            else:
                return render(request, 'pages/login.html', {'message': '用户名或密码错误'})
        except Exception as e:
            print(e)
            return render(request, 'pages/login.html', {'message': '用户名或密码错误'})


def homepage(request, keyword=''):
    print(request.session['ID'])
    if not request.session.get('is_login'):
        request.session['message'] = '登录信息已失效，请重新登入'
        return redirect('../login/')
    if request.method == 'GET':
        goods_list = Goods.objects.filter(
            models.Q(commodity_name__icontains=keyword)).values(
            'picture',
            'commodity_name',
            'price',
            'commodity_id')
        if not goods_list.exists():
            print("nothing")
            return render(request, 'pages/index.html', {'errmsg': '无查询结果'})

        response = render(request, 'pages/index.html',
                          {'goods_list': goods_list})
        return response


def personal_info(request):
    if not request.session.get('is_login'):
        request.session['message'] = '登录信息已失效，请重新登入'
        return redirect('../login/')

    # 在判断完登录信息后，我需要获取这个人的信息
    ID = request.session['ID']
    user = UserInfo.objects.get(user_id=ID)

    # 如果这是POST方法
    if request.method == 'POST':
        try:
            file_object = request.FILES.get("head")
            print(file_object.name)
            img_name = str(ID) + '.jpg'
            DIR = os.path.join('secondhand_book', 'static', 'head', img_name)
            f = open(DIR, mode='wb')
            f.seek(0)
            f.truncate()
            for chunk in file_object.chunks():
                f.write(chunk)
            f.close()
        except Exception as e:
            my_info = {'img_path': user.img_path, 'user_id': user.user_id}
            return render(request, 'pages/personIfo.html', {'img_path': user.img_path, 'user_id': user.user_id,
                                                            'errmsg': '你没有提交任何图片！'})

    # 无论post还是get都需要返回来一个网页
    my_info = {'img_path': user.img_path, 'user_id': user.user_id}
    return render(request, 'pages/personIfo.html', my_info)


def enter_ver_code(request):
    '''
    输入验证码
    '''
    if request.method == 'GET':
        return render(request, 'pages/yanzheng.html')

    email = request.session.get('email')
    vercode = request.POST.get('vercode')
    userinfo = UserInfo.objects.filter(email=email, ver_code=vercode)
    if not userinfo.exists():
        request.session['errmsg'] = '验证码不正确或超时，请重新验证'
        return redirect('../findpswd')

    # 生成随机密码
    s_code = string.ascii_letters+string.digits
    code = random.sample(s_code, 6)
    vcode = "".join(code)
    UserInfo.objects.filter(email=email).update(password=vcode)
    # 将重置的密码发送到用户邮箱
    message_text = '你正在登录校园二手书交易平台，密码重置为%s' % (vcode)
    send_mail(subject='你好', message=message_text, from_email=email,
              recipient_list=[email], fail_silently=False)
    request.session['rstpwd_message'] = '密码重置成功'
    response = redirect('../login_view/')
    return response

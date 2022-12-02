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
        reg_failed_msg = request.session.get('reg_failed_msg')
        response = render(request, 'pages/register.html',
                          {'reg_failed_msg': reg_failed_msg})
        request.session['reg_failed_msg'] = None
        return response

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
            request.session['reg_suc_msg'] = '注册成功！'
            return redirect('../login')

    # 否则就在注册页面
    request.session['reg_failed_msg'] = '注册失败！'
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
        reg_suc_msg = request.session.get('reg_suc_msg')
        response = render(request, 'pages/login.html',
                          {'rstpwd_message': rstpwd_message, 'reg_suc_msg': reg_suc_msg})
        request.session['reg_suc_msg'] = None
        request.session['rstpwd_message'] = None
        return response
    if request.method == 'POST':
        ID = request.POST.get("username")
        pwd = str(request.POST.get('password'))
        try:
            user = UserInfo.objects.get(user_id=ID)
            if pwd == user.password:
                request.session['is_login'] = True
                request.session['ID'] = user.user_id
                request.session['pswd'] = user.password
                request.session.set_expiry(0)
                response = redirect('../homepage/')
                response.set_cookie('ID', ID)
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

    # POST
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        print(keyword)
        return redirect('../homepage&keyword=%s' % (keyword))


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
            print("123456")
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
            print("!!!!!!")
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
    response = redirect('../login')
    return response


def goods_detail(request, id):
    if request.method == 'GET':
        good = Goods.objects.filter(
            models.Q(commodity_id=id)).values(
            'picture',
            'commodity_id',
            'commodity_name',
            'price',
            'note',
            'user_contact')
        print(good.values())
        return render(request, 'pages/goodsDetails.html', {'good': good.values()[0]})


def person_info(request):
    if request.method == 'GET':
        uid = request.COOKIES['ID']
        user_id_change_success_msg = request.session.get(
            'user_id_change_success_msg')
        chg_pswd_suc_msg = request.session.get('chg_pswd_suc_msg')
        user = UserInfo.objects.filter(user_id=uid).values('img_path')
        response = render(request,
                          'pages/personIfo.html',
                          {'user': user.values()[0],
                           'uid': uid,
                           'user_id_change_success_msg': user_id_change_success_msg,
                           'chg_pswd_suc_msg': chg_pswd_suc_msg
                           }
                          )
        request.session['user_id_change_success_msg'] = None
        request.session['chg_pswd_suc_msg'] = None
        print('chg_pswd_suc_msg', request.session['chg_pswd_suc_msg'])
        return response


def changepht(request):
    if request.method == 'GET':
        return render(request, 'pages/changhead.html')

    # POST
    try:
        ID = request.COOKIES['ID']
        file_object = request.FILES.get("head")
        print(file_object.name)
        img_name = '1' + '.jpg'
        DIR = os.path.join('secondhand_book', 'static', 'img', img_name)
        f = open(DIR, mode='wb')
        f.seek(0)
        f.truncate()
        for chunk in file_object.chunks():
            f.write(chunk)
        f.close()
    except Exception as e:
        return render(request, 'pages/changhead.html', {'no_img': '你没有提交任何图片！'})

    # 无论post还是get都需要返回来一个网页
    return redirect('../person_info')


def changepswd(request):
    if request.method == 'GET':
        chg_pswd_failed_msg = request.session.get('chg_pswd_failed_msg')
        response = render(request, 'pages/changepsd.html',
                          {'chg_pswd_failed_msg': chg_pswd_failed_msg})
        request.session['chg_pswd_failed_msg'] = None
        return response

    # POST
    # 获得现在登录的用户ID和密码
    username = request.COOKIES['ID']
    pswd = request.session.get('pswd')
    # 获得输入的密码
    oldpswd = request.POST.get('oldpswd')
    newpswd1 = request.POST.get('newpswd1')
    newpswd2 = request.POST.get('newpswd2')
    if oldpswd == pswd and newpswd1 == newpswd2:
        # 如果密码一致且两遍密码一致，则修改
        UserInfo.objects.filter(user_id=username).update(password=newpswd1)
        # 修改session里的pswd值
        request.session['pswd'] = newpswd1
        response = redirect('../person_info/')
        request.session['chg_pswd_suc_msg'] = '密码修改成功'
        # 跳回去
        return response

    # 否则就在当前页面
    response = redirect('../changepswd/')
    request.session['chg_pswd_failed_msg'] = '密码修改失败！'
    return response


def changename(request):
    if request.method == 'GET':
        user_id_change_failed_msg = request.session.get(
            'user_id_change_failed_msg')
        print(user_id_change_failed_msg)
        response = render(request, 'pages/changeid.html',
                          {'user_id_change_failed_msg': user_id_change_failed_msg})
        request.session['user_id_change_failed_msg'] = None
        print(request.session['user_id_change_failed_msg'])
        return response

    # POST
    # 获得现在登录的用户ID
    oldname = request.COOKIES['ID']
    newname = request.POST.get('newname')
    if oldname == newname:
        # 要修改的和修改后的一样，说明不用修改，就在当前页面
        response = render(request, 'pages/changeid.html',
                          {'user_id_same_msg': '用户名与当前用户名一致！'})
        return response
    # 先找一下是否重复
    user = UserInfo.objects.filter(user_id=newname)
    if not user.exists():
        # 不存在才修改
        # 先修改商品表
        Goods.objects.filter(user_id=oldname).update(user_id=newname)
        # 再修改用户表
        UserInfo.objects.filter(user_id=oldname).update(user_id=newname)
        # 修改cookies里的ID值
        response = redirect('../person_info/')
        response.set_cookie('ID', newname)
        # 给一个信号
        request.session['user_id_change_success_msg'] = '用户名修改成功'
        # 跳回去
        return response
    # 否则就在当前页面
    request.session['user_id_change_failed_msg'] = '该用户名已存在'
    return redirect('../changename/')


def mygoods(request):

    def get_data(id):
        goods_list = Goods.objects.filter(
            models.Q(user_id=id)).values(
            'picture',
            'commodity_id',
            'commodity_name',
            'price',
            'note',
            'user_contact')
        return goods_list

    uid = request.COOKIES['ID']
    if request.method == 'GET':
        goods_list = get_data(uid)
        return render(request, 'pages/myGoods.html', {'goods_list': goods_list})

    # POST
    cid = request.POST.get('cid')
    Goods.objects.filter(commodity_id=cid).delete()
    goods_list = get_data(uid)
    return render(request, 'pages/myGoods.html', {'goods_list': goods_list})

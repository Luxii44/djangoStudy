import datetime
import uuid
from hashlib import sha1

from django.core.paginator import Paginator
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from redis import StrictRedis
from goods.models import GoodsInfo
from order.models import Order
from user_center.models import UserInfo, AddressInfo, AreaInfo
from user_center import task


def register(request):
    """
    用户注册
    :param request:
    :return:
    """
    if request.method == 'POST':
        post = request.POST
        username = post.get('username')
        password = post.get('password')
        email = post.get('email')
        is_username_exist = UserInfo.objects.filter(username=username).count() == 0
        is_email_exist = UserInfo.objects.filter(email=email).count() == 0
        if is_email_exist and is_username_exist:
            user = UserInfo()
            user.username = username
            user.email = email
            user.password = sha1(password.encode('utf8')).hexdigest()
            user.save()
            # 发送验证邮件
            token = uuid.uuid1()
            redis = StrictRedis()
            key = 'user_verify_email_key_' + str(user.id)
            redis.set(key, token)
            html_message = "<a href='http://127.0.0.1:8000/user/verify_email/?id=%d&token=%s'>激活邮箱</a>" % (user.id, token)
            task.send_verify_email.delay('生鲜商城用户注册邮箱激活', user.email, html_message)
            return render(request, 'tips.html', {'info': '请登录邮箱进行激活操作'})
        else:
            return render(request, 'user_center/register.html', {'error': '用户名或邮箱已经存在'})
    else:
        return render(request, 'user_center/register.html', {'title': '注册', 'hide_header': True})


def login(request):
    """登录处理"""
    if request.method == 'POST':
        # pre_url = request.session.get('pre_url')  # 上次访问的URL
        pre_url = request.session.get('pre_url', '/')
        try:
            post = request.POST
            username = post.get('username')
            password = post.get('password')
            user = UserInfo.objects.get(username=username)
            remember = post.get('remember')
            if sha1(password.encode('utf8')).hexdigest() == user.password:
                # 密码校验成功
                # 邮箱激活校验
                if user.verification is False:
                    code = 403
                    msg = '请您登录邮箱点击激活邮箱链接'
                else:
                    code = 200
                    msg = '登录成功'
                    # 保存用户信息到session
                    request.session['uid'] = user.id
                    request.session['username'] = user.username
            else:
                # 密码校验失败
                code = 401
                msg = '密码错误'
        except:
            # 密码校验失败
            code = 402
            msg = '用户名错误'
        # 返回数据
        response = JsonResponse({'code': code, 'msg': msg, 'pre_url': pre_url})
        if code == 200 and remember == '1':
            # 登录成功设置cookies
            now = datetime.datetime.now()
            date = now + datetime.timedelta(days=7)
            response.set_cookie('username', user.username, expires=date)
        return response
    else:
        username = request.COOKIES.get('username', '')
        from_url = request.GET.get('from', '')
        context = {
                   'title': '登录',
                   'username': username,
                   'hide_header': True,
                    'from_url': from_url
        }
        return render(request, 'user_center/login.html', context)


def username_exist(request):
    """
    检测用户名是否重名
    :param request:
    :return:
    """
    username = request.GET.get('username')
    num = UserInfo.objects.filter(username=username).count()
    if num > 0:
        return JsonResponse({'code': 400, 'msg': '该用户名已存在，请您更换用户名注册'})
    else:
        return JsonResponse({'code': 200, 'msg': '该用户名可以注册'})


def email_exist(request):
    """
    检测邮箱是否重名
    :param request:
    :return:
    """
    email = request.GET.get('email')
    num = UserInfo.objects.filter(email=email).count()
    if num > 0:
        return JsonResponse({'code': 400, 'msg': '该邮箱已被占用，请您更换邮箱注册'})
    else:
        return JsonResponse({'code': 200, 'msg': '该邮箱可以注册'})


def verify_email(request):
    try:
        get = request.GET
        uid = get.get('id')
        key = 'user_verify_email_key_' + str(uid)
        user_token = get.get('token')
        redis = StrictRedis()
        redis_token = redis.get(key)
        verify_flag = False # 邮箱激活成功与否flag
        if user_token == bytes.decode(redis_token):
                user = UserInfo.objects.get(id=uid)
                if user.verification is False:
                    user.verification = True
                    user.save()
                    verify_flag = True
                    # 激活成功后，删除token
                    redis.delete(key)
    except:
        pass
    if verify_flag is True:
        return HttpResponseRedirect('/user/login/')
    else:
        return render(request, 'tips.html', {'info': '邮箱验证失败，请您重试'})


def find_password(request):
    """
    找回密码
    :param request:
    :return:
    """
    if request.method == 'POST':
        post = request.POST
        username = post.get('username')
        email = post.get('email')
        try:
            user = UserInfo.objects.get(username=username)
            if user.email == email:
                # 发送验证邮件
                token = uuid.uuid1()
                redis = StrictRedis()
                key = 'user_verify_fpwd_email_key_' + str(user.id)
                redis.set(key, token)
                html_message = "<a href='http://127.0.0.1:8000/user/verify_fpwd_email/?id=%d&token=%s'>找回密码验证</a>" % (user.id, token)
                task.send_verify_email.delay('生鲜商城用户找回密码邮箱验证', user.email, html_message)
                code = 200
                msg = '请您登录邮箱，点击邮件里的邮箱验证链接'
            else:
                code = 401
                msg = '输入的邮箱不正确'
        except:
            code = 400
            msg = '该用户名尚未注册'
        return JsonResponse({'code': code, 'msg': msg})
    else:
        return render(request, 'user_center/find_password.html')


def reset_password(request):
    try:
        post = request.POST
        uid = post.get('id')
        key = 'user_verify_fpwd_email_key_' + str(uid)
        user_token = post.get('token')
        pwd = post.get('pwd')
        cpwd = post.get('cpwd')
        redis = StrictRedis()
        redis_token = redis.get(key)
        if user_token == bytes.decode(redis_token) and pwd == cpwd:
            user = UserInfo.objects.get(id=uid)
            user.password = sha1(pwd.encode('utf8')).hexdigest()
            user.save()
            redis.delete(key)
            info = '密码重置成功'
        else:
            info = '密码重置失败'
    except:
        info = '密码重置失败'

    return render(request, 'tips.html', {'info': info})


def verify_fpwd_email(request):
    """
    验证找回密码邮箱链接
    :param request:
    :return:
    """
    try:
        get = request.GET
        uid = get.get('id')
        key = 'user_verify_fpwd_email_key_' + str(uid)
        user_token = get.get('token')
        redis = StrictRedis()
        redis_token = redis.get(key)
        verify_flag = False  # 邮箱验证成功与否flag
        if user_token == bytes.decode(redis_token):
            verify_flag = True
            # redis.delete(key)
    except:
        pass
    if verify_flag is True:
        return render(request, 'user_center/reset_password.html', {'title': '重置密码', 'id': uid, 'token':user_token})
    else:
        return render(request, 'tips.html', {'info': '邮箱验证失败，请您重试'})


def center(request):
    """
    用戶中心
    :param request:
    :return:
    """
    # 用户信息
    user = UserInfo.objects.get(id=request.session.get('uid'))
    # 浏览记录
    view_goods = []
    view_goods_str = request.COOKIES.get('view_goods', '')
    view_goods_list = view_goods_str.split(',')
    view_goods_list.pop()
    if view_goods_str != '':
        for goods_id in view_goods_list:
            goods = GoodsInfo.objects.get(id=goods_id)
            view_goods.append(goods)
    context = {
             'title': '用户中心',
             'app_name': '用户中心',
             'user': user,
             'view_goods': view_goods
    }
    return render(request, 'user_center/user_center_info.html', context)


def logout(request):
    """
    退出登录
    :param request:
    :return:
    """
    request.session.flush()
    return HttpResponseRedirect('/')


def address(request):
    """地址列表"""
    uid = request.session.get('uid')
    address_list = AddressInfo.objects.filter(uid=uid)
    if len(address_list) > 0:
        new_list = list()
        for add in address_list:
            province_name = AreaInfo.get_province_name(add.province_id)
            city_name = AreaInfo.get_city_name(add.province_id, add.city_id)
            district_name = AreaInfo.get_district_name(add.province_id, add.city_id, add.district_id)
            data={
                'area': province_name + city_name + district_name,
                'address': add.address,
                'realname': add.realname,
                'phone': add.phone,
                'is_default': add.is_default,
                'id': add.id,
                'app_name': '用户中心',
                'title': '收货地址列表',
            }
            new_list.append(data)
        return render(request, 'user_center/user_center_site.html', {'address_list': new_list})
    else:
        return HttpResponseRedirect('/user/add_address/')


def add_address(request):
    """添加或编辑收货地址"""
    if request.method == 'POST':
        uid = request.session.get('uid')
        post = request.POST
        address_id = post.get('address_id')
        if address_id != '':
            # 编辑
            address = AddressInfo.objects.get(id=address_id)
        else:
            # 新增
            address = AddressInfo()
        address.uid = uid
        address.realname = post.get('realname')
        address.province_id = post.get('province')
        address.city_id = post.get('city')
        address.district_id = post.get('district')
        address.address = post.get('detail')
        address.phone = post.get('phone')
        address.save()
        return HttpResponseRedirect('/user/address/')
    else:
        # 查询全部省份
        # province = AreaInfo.objects.filter(Q(city_id=0) & Q(district_id=0))
        province = AreaInfo.objects.filter(city_id=0, district_id=0)
        context = {
            'app_name': '用户中心',
            'title': '添加收货地址',
            'province': province
        }
        return render(request, 'user_center/user_center_site_edit.html', context)


def get_address_city(request):
    """ajax获取一个省下的城市"""
    province_id = request.GET.get('province_id')
    city_list = AreaInfo.objects.filter(province_id=province_id, city_id__gt=0, district_id=0).values('city_id', 'name')
    return JsonResponse({"city_list": list(city_list)})


def get_address_district(request):
    """ajax获取一个市下的县区"""
    city_id = request.GET.get('city_id')
    district_list = AreaInfo.objects.filter(city_id=city_id,district_id__gt=0).values('district_id', 'name')
    return JsonResponse({'district_list': list(district_list)})


def edit_address(request, address_id):
    """编辑收货地址信息"""
    province = AreaInfo.objects.filter(city_id=0, district_id=0)
    address_info = AddressInfo.objects.get(id=address_id)
    city = AreaInfo.objects.filter(province_id=address_info.province_id,city_id__gt=0, district_id=0)
    district = AreaInfo.objects.filter(province_id=address_info.province_id, city_id=address_info.city_id, district_id__gt=0)
    context = {
        'province': province,
        'address_info': address_info,
        'city': city,
        'district': district,
        'app_name': '用户中心',
        'title': '编辑收货地址',
    }
    return render(request, 'user_center/user_center_site_edit.html',context)


def del_address(request, address_id):
    """删除地址"""
    try:
        AddressInfo.objects.filter(id=address_id).delete()
        return JsonResponse({'code': 200, 'msg': '删除成功'})
    except Exception:
        return JsonResponse({'code': 400, 'msg': '删除失败'})


@transaction.atomic
def set_default_address(request, address_id):
    """设置默认地址"""
    address = AddressInfo.objects.get(id=address_id)
    # 记录事务开始保存点
    save_point = transaction.savepoint()
    try:
        # 设置（取消）默认地址
        address.is_default = not address.is_default
        address.save()
        undefault_address_id = 0  # 记录被取消默认地址的id
        if not address.is_default:
            # 如果当前选中的不是默认地址
            # 就要考虑有没有其他地址是默认地址
            uid = request.session.get('uid')
            address_list = AddressInfo.objects.filter(uid=uid, is_default=True)
            # 如果有其他地址是已经被设置为默认地址，就把这个取消掉
            if len(address_list) == 1:
                address_list[0].is_default = False
                undefault_address_id = address_list[0].id
                address_list[0].save()
        # 事务提交
        transaction.savepoint_commit(save_point)
        return JsonResponse({'code': 200, 'msg': '设置成功', 'undefault_address_id': undefault_address_id})
    except Exception:
        # 事务回滚
        transaction.savepoint_rollback(save_point)
        return JsonResponse({'code': 400, 'msg': '设置失败'})


def order(request):
    """用户订单列表"""
    current_page = int(request.GET.get('page', '1'))

    uid = request.session['uid']
    order_list = Order.objects.filter(user_id=uid).order_by('-add_time')

    paginator = Paginator(order_list, 1)
    order_list = paginator.page(current_page)

    context = {
               'title': '用户中心',
               'order_list': order_list
    }
    return render(request, 'user_center/user_center_order.html', context)


def del_view_goods(request):
    """删除浏览记录"""
    try:
        response = JsonResponse({'code': 200, 'msg': '删除成功'})
        goods_id = request.POST.get('goods_id')
        view_goods = request.COOKIES.get('view_goods').split(',')
        # goods_id 为0 时，删除全部
        # 不为0时，删除某一个
        if goods_id != '0':
            if goods_id in view_goods:
                view_goods.remove(goods_id)
            view_goods_str = ','.join(view_goods)
            response.set_cookie('view_goods', view_goods_str, max_age=7 * 86400)
        else:
            response.set_cookie('view_goods', '', max_age=7 * 86400)
        return response
    except Exception:
        return JsonResponse({'code': 400, 'msg': '删除失败'})
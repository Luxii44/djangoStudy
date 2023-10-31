import datetime
import random

from django.db import transaction
from django.shortcuts import render, HttpResponseRedirect

# Create your views here.
from cart.models import CartInfo
from order.models import Order, OrderDetail
from user_center.models import AddressInfo


def add_order(request):
    uid = request.session.get('uid')
    cart_ids = request.POST.getlist('cart_id')
    cart_list = []
    cart_id_list_str = ''
    # 购物车数据
    for cart_id in cart_ids:
        cart = CartInfo.objects.get(id=cart_id)
        cart_list.append(cart)
        cart_id_list_str += cart_id+','
    # 收货地址信息
    address_list = AddressInfo.objects.filter(uid=uid).order_by('-is_default')
    context = {
        'cart_list': cart_list,
        'address_list': address_list,
        'cart_id_list': cart_id_list_str,
        'title': '提交订单',
        'app_name': '提交订单'
    }
    return render(request, 'order/place_order.html', context)


@transaction.atomic()
def handle_order(request):
    address_id = request.POST.get('address')
    cart_id_list = request.POST.get('cart_id_list').split(',')
    sp = transaction.savepoint()
    try:
        # 订单表
        order = Order()
        now_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        order.id = '%s%s' % (now_str, random_str())
        order.user_id = request.session['uid']
        order.address_id = address_id
        order.save()
        total_price = 0
        # 订单详情表
        cart_list = CartInfo.objects.filter(id__in=cart_id_list)
        for cart in cart_list:
            if cart.count <= cart.goods.store:
                detail = OrderDetail()
                detail.order = order
                detail.goods = cart.goods
                detail.count = cart.count
                detail.price = cart.goods.price*detail.count
                detail.save()

                goods = cart.goods
                goods.store -= cart.count
                goods.save()

                cart.delete()
                total_price += detail.price
        order.total_price = total_price
        order.save()
        transaction.savepoint_commit(sp)
        return HttpResponseRedirect('/user/order/')
    except Exception:
        transaction.savepoint_rollback(sp)
        return HttpResponseRedirect('/cart/')


def random_str(random_len=6):
    str = ''
    chars = '0123456789'
    # 依据长度，随机chars中下标，依据随机下标获取数据
    for i in range(random_len):
        str += chars[random.randint(0, (len(chars) - 1))]
    return str

import uuid
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from cart.models import CartInfo
from goods.models import GoodsInfo

# import os,django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_name.settings")
# django.setup()

def index(request):
    """购物车页面"""
    uid = request.session.get('uid')
    cart_goods = CartInfo.objects.filter(user_id=uid)
    context = {
        'app_name': '购物车',
        'cart_goods': cart_goods,
        'title': '购物车'
    }
    return render(request, 'cart/cart.html', context)


def count(request):
    """购物车购物项数量"""
    uid = request.session.get('uid')
    num = CartInfo.objects.filter(user_id=uid).count()
    return JsonResponse({'num': num})


def add_goods(request):
    """添加商品到购物车"""
    uid = request.session.get('uid')
    goods_id = int(request.POST.get('goods_id', 0))
    goods_num = int(request.POST.get('goods_num', 1))
    goods = GoodsInfo.objects.get(id=goods_id)
    if goods_num <= goods.store:
        carts = CartInfo.objects.filter(goods_id=goods_id, user_id=uid)
        if len(carts) == 1:
            cart = carts[0]
            # 更新
            cart.count += goods_num
        else:
            cart = CartInfo()
            cart.id = uuid.uuid1()
            cart.user_id = uid
            cart.goods_id = goods_id
            cart.count = goods_num
        # 保存数据
        cart.save()
        cart_num = CartInfo.objects.filter(user_id=uid).count()
        return JsonResponse({'code': 200, 'msg': '添加购物车成功', 'cart_num': cart_num})
    else:
        return JsonResponse({'code': 400, 'msg': '添加购物车失败,库存不足，请修改购买数量'})


def del_goods(request):
    """删除购物车商品"""
    uid = request.session.get('uid')
    cart_id = request.POST.get('cart_id')
    CartInfo.objects.filter(user_id=uid, id=cart_id).delete()
    return JsonResponse({'code': 200, 'msg': '删除商品成功'})


def edit(request):
    cart_id = request.POST.get('cart_id')
    num = int(request.POST.get('num'))
    try:
        cart = CartInfo.objects.get(id=cart_id)
        cart.count = num
        cart.save()
        return JsonResponse({'code': 200, 'msg': '编辑成功'})
    except Exception:
        return JsonResponse({'code': 400, 'msg': '编辑失败'})

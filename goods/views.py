from django.core.paginator import Paginator
from django.shortcuts import render
from haystack.generic_views import SearchView

from goods.models import CateInfo, GoodsInfo

# Create your views here.


def index(request):
    # 分类
    cates = CateInfo.objects.filter(is_del=False)
    cate_goods = []
    for cate in cates:
        hot_goods = cate.goodsinfo_set.order_by('-click')[0:3]
        new_goods = cate.goodsinfo_set.order_by('-id')[0:4]
        cate_goods.append({
            'cate': cate,
            'hot_goods': hot_goods,
            'new_goods': new_goods
        })
    context = {
        'title': '生鲜商城首页',
        'is_goods': True,
        'cates': cates,
        'cate_goods': cate_goods
    }
    return render(request, 'goods/index.html', context)


def cate_goods(request, cate_id, page):
    """分类下的商品列表"""
    now_cate = CateInfo.objects.get(id=cate_id)
    cates = CateInfo.objects.filter(is_del=False)
    new_goods = now_cate.goodsinfo_set.order_by('-id')[0:3]
    # 排序
    orderby = request.GET.get('orderby', '-id')
    goods_list = now_cate.goodsinfo_set.order_by(orderby)
    # 分页
    page_goods_num = 10  # 每页显示多少条商品
    paginator = Paginator(goods_list,page_goods_num)
    page_goods = paginator.page(page)
    context = {
        'title': now_cate.name + '商品列表',
        'is_goods': True,
        'now_cate': now_cate,
        'cates': cates,
        'new_goods': new_goods,
        'goods_list': page_goods,
        'orderby': orderby
    }
    return render(request, 'goods/list.html', context)


def detail(request, goods_id):
    """商品详情"""
    goods = GoodsInfo.objects.get(id=goods_id)
    now_cate = CateInfo.objects.get(id=goods.cate_id)
    cates = CateInfo.objects.filter(is_del=False)
    new_goods = GoodsInfo.objects.filter(cate_id=goods.cate_id).exclude(id=goods_id).order_by('-id')[0:2]
    context = {
        'title': goods.name,
        'is_goods': True,
        'is_detail': True,
        'goods': goods,
        'cates': cates,
        'now_cate': now_cate,
        'new_goods': new_goods
    }
    # 返回对象
    response = render(request, 'goods/detail.html', context)
    # 更新点击量
    goods.click += 1
    goods.save()
    # 记录用户浏览历史
    if request.COOKIES.get('view_goods', '') == '':
        view_goods = []
    else:
        view_goods = request.COOKIES.get('view_goods', '').split(',')
    # 如果历史记录中已有当前商品，就删除之前的
    if goods_id in view_goods:
        view_goods.remove(goods_id)
    # 插入商品到历史记录的首位
    view_goods.insert(0, goods_id)
    # 如果历史记录 >5条时，删除最后一个
    if len(view_goods) > 6:
        view_goods.pop()
    # 设置cookie
    view_goods_str = ','.join(view_goods)
    response.set_cookie('view_goods', view_goods_str, max_age=7*86400)
    return response


class MySearchView(SearchView):
    """自定义搜索视图"""
    def get_context_data(self, **kwargs):
        context = super(MySearchView, self).get_context_data(**kwargs)
        context['is_goods'] = True
        context['is_search'] = True
        context['title'] = '"'+context['query']+'"搜索结果'
        return context


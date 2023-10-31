from django.contrib import admin
from goods.models import *
# Register your models here.


class GoodsInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cate_id', 'name', 'sub_name', 'image', 'price', 'click', 'unit', 'store', 'is_del']


admin.site.register(GoodsInfo, GoodsInfoAdmin)
from django.db import models

# Create your models here.
from goods.models import GoodsInfo
from user_center.models import UserInfo, AddressInfo


class Order(models.Model):
    class Meta:
        db_table = 'order'
    id = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    add_time = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(AddressInfo,on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    state = models.IntegerField(default=0)


class OrderDetail(models.Model):
    class Meta:
        db_table = 'order_detail'
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    goods = models.ForeignKey(GoodsInfo,on_delete=models.CASCADE)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
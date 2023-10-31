from django.db import models

# Create your models here.
from goods.models import GoodsInfo
from user_center.models import UserInfo


class CartInfo(models.Model):

    class Meta:
        db_table = 'cart'

    id = models.CharField(max_length=36, primary_key=True)
    goods = models.ForeignKey(GoodsInfo,on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo,on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
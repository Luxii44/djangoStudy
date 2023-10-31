from django.db import models
from tinymce.models import HTMLField
# Create your models here.


class CateInfo(models.Model):

    class Meta:
        db_table = 'cates'

    name = models.CharField(max_length=20)
    is_del = models.BooleanField(default=False)


class GoodsInfo(models.Model):

    class Meta:
        db_table = 'goods'

    cate = models.ForeignKey(CateInfo,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    click = models.IntegerField()
    sub_name = models.CharField(max_length=200)
    unit = models.CharField(max_length=10)
    store = models.IntegerField(default=100)
    details = HTMLField()
    is_del = models.BooleanField(default=False)
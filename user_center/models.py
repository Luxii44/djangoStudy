from django.db import models

# Create your models here.


class UserInfo(models.Model):

    class Meta:
        db_table = 'user'

    username = models.CharField(max_length=20)
    password = models.CharField(max_length=40)
    email = models.CharField(max_length=30)
    verification = models.BooleanField(default=False)
    reg_time = models.DateTimeField(auto_now_add=True)


class AreaInfo(models.Model):

    class Meta:
        db_table = 'area'

    name = models.CharField(max_length=50)
    province_id = models.CharField(max_length=10)
    city_id = models.CharField(max_length=10)
    district_id = models.CharField(max_length=10)

    @classmethod
    def get_province_name(cls, province_id):
        try:
            address = cls.objects.filter(province_id=province_id, city_id=0, district_id=0)
            return address[0].name
        except  Exception:
            return ''

    @classmethod
    def get_city_name(cls, province_id, city_id):
        try:
            address = cls.objects.filter(province_id=province_id, city_id=city_id, district_id=0)
            return address[0].name
        except  Exception:
            return ''

    @classmethod
    def get_district_name(cls, province_id, city_id, district_id):
        try:
            address = cls.objects.filter(province_id=province_id, city_id=city_id, district_id=district_id)
            return address[0].name
        except  Exception:
            return ''


class AddressInfo(models.Model):

    class Meta:
        db_table = 'user_address'

    uid = models.IntegerField()
    realname = models.CharField(max_length=10)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    province_id = models.CharField(max_length=10)
    city_id = models.CharField(max_length=10)
    district_id = models.CharField(max_length=10)
    is_default = models.BooleanField(default=False)


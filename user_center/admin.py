from django.contrib import admin
from user_center.models import *
# Register your models here.


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'verification', 'reg_time']


admin.site.register(UserInfo, UserInfoAdmin)
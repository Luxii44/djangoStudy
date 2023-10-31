from django.conf.urls import url
from user_center import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^username_exist/$', views.username_exist),
    url(r'^email_exist/$', views.email_exist),
    url(r'^verify_email/$', views.verify_email),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^find_password/$', views.find_password),
    url(r'^verify_fpwd_email/$', views.verify_fpwd_email),
    url(r'^reset_password/$', views.reset_password),
    url(r'^address/$', views.address),
    url(r'^add_address/$', views.add_address),
    url(r'^edit_address/(?P<address_id>\d+)$', views.edit_address),
    url(r'^del_address/(?P<address_id>\d+)$', views.del_address),
    url(r'^get_address_city/$', views.get_address_city),
    url(r'^get_address_district/$', views.get_address_district),
    url(r'^set_default_address/(?P<address_id>\d+)$', views.set_default_address),
    url(r'^order/$', views.order),
    url(r'^del_view_goods/$', views.del_view_goods),
    url(r'^$', views.center),
]

from django.conf.urls import url
from cart import views

urlpatterns = [
    url(r'^count/$', views.count),
    url(r'^add_goods/$', views.add_goods),
    url(r'^del_goods/$', views.del_goods),
    url(r'^edit/$', views.edit),
    url(r'^$', views.index),
]

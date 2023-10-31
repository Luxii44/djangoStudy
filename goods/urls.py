from django.conf.urls import url, include
from goods import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^category(\d+)_goods_(\d+)/$', views.cate_goods),
    url(r'^detail_(\d+)/$', views.detail),
    # url(r'^search/$', include('haystack.urls')),
    url(r'^search/$', views.MySearchView.as_view()),
]

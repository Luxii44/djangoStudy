from django.conf.urls import url
from order import views

urlpatterns = [
    url(r'^add_order/$', views.add_order),
    url(r'^handle_order/$', views.handle_order),
]

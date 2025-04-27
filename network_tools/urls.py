from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("ping/", views.ping, name="ping"),
    path("ip_addr/", views.ip_addr, name="ip_addr"),
]

from django.conf.urls import url,include
from django.urls.resolvers import URLPattern
from AdminSide import views
from django.urls import path

urlpatterns = [
    url(r"^AdminSide/adminhome/$",views.admindash, name="admindash"),
    url(r"^AdminSide/finance/$",views.finance, name="adminfinance"),
    url(r"^AdminSide/sermons/$",views.sermons, name="adminsermon"),
    url(r"^AdminSide/users/$",views.users, name="adminusers"),
    url(r"^AdminSide/announcement/$",views.announce, name="adminannouncement"),
]

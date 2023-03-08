from django.conf.urls import url,include
from django.urls.resolvers import URLPattern
from UserSide import views
from django.urls import path

urlpatterns = [
    url(r"^UserSide/userhome/$",views.userdash, name="userdash"),
    url(r"^UserSide/sermons/$",views.sermons, name="sermons"),
    url(r"^UserSide/profile/$",views.profile, name="profile"),
    url(r"^UserSide/tithe/$",views.tithe, name="tithe"),
    url(r"^UserSide/announcement/$",views.announce, name="announcement"),
    path('<str:ref>/', views.verify_payment, name="verify-payment"),
]

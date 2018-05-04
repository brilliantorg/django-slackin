from django.conf.urls import url

from slackin import views

urlpatterns = [
    url(r'^$', views.SlackinInviteView.as_view(), name='slackin_invite'),
]

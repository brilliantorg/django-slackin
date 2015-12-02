from django.conf.urls import patterns, url

from slackin.views import SlackinInviteView

urlpatterns = patterns(
    '',
    url(r'^$', SlackinInviteView.as_view(), name='slackin_invite'),
)

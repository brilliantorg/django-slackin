from django.utils.functional import cached_property
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.views.generic.base import View

from slackin.conf import settings
from slackin.slack import Slack
from slackin.forms import SlackinInviteForm


class SlackinMixin(object):
    @cached_property
    def slackin_context(self):
        slack = Slack(token=settings.SLACKIN_TOKEN, subdomain=settings.SLACKIN_SUBDOMAIN)
        slack_team_response = slack.get_team()
        slack_user_response = slack.get_users()
        users_total = slack_user_response['members']
        users_online = [user for user in users_total if user['presence'] == 'active']
        team_context = slack_team_response['team']
        team_context['image'] = slack_team_response['team']['icon']['image_132']
        return {
            'team': team_context,
            'users': users_total,
            'users_online': len(users_online),
            'users_total': len(users_total),
        }

class SlackinInviteView(SlackinMixin, View):
    template_name = 'slackin/invite/page.html'

    def get_generic_context(self):
        return {
            'slackin': self.slackin_context,
        }

    def get_redirect_url(self):
        if '/' in settings.SLACKIN_LOGIN_REDIRECT:
            return settings.SLACKIN_LOGIN_REDIRECT
        else:
            return reverse(settings.SLACKIN_LOGIN_REDIRECT)

    def response(self):
        return render_to_response(template_name=self.template_name,
                                  context=self.context,
                                  context_instance=RequestContext(self.request))

    def get(self, request):
        if settings.SLACKIN_LOGIN_REQUIRED and not request.user.is_authenticated():
            return HttpResponseRedirect(self.get_redirect_url())

        self.context = self.get_generic_context()

        email_address = ''
        if self.request.user.is_active:
            email_address = self.request.user.email
        self.context['slackin_invite_form'] = SlackinInviteForm(initial={'email_address': email_address})

        return self.response()

    def post(self, request):
        if settings.SLACKIN_LOGIN_REQUIRED and not request.user.is_authenticated():
            return HttpResponseRedirect(self.get_redirect_url())

        self.context = self.get_generic_context()
        invite_form = SlackinInviteForm(self.request.POST)
        if invite_form.is_valid():
            self.context['slackin_invite_form_success'] = True
        self.context['slackin_invite_form'] = invite_form
        return self.response()


import time

from django.utils.functional import cached_property
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.views.generic.base import View

from slackin.conf import settings
from slackin.slack import Slack
from slackin.forms import SlackinInviteForm


_team_context = None
_team_context_timeout = 60 * 60 # 1 hour
_users_context = None
_users_context_timeout = 60 * 5 # 5 minutes

class SlackinMixin(object):

    def _context_expired(self, context, timeout):
        return not context or (time.time() - context['last_fetched']) > timeout

    def _create_context(self, data):
        return {
            'data': data,
            'last_fetched': time.time(),
        }

    def _get_team_context(self, slack_instance):
        global _team_context, _team_context_timeout
        if self._context_expired(_team_context, _team_context_timeout):
            slack_team_response = slack_instance.get_team()
            team_context = slack_team_response['team']
            team_context['image'] = slack_team_response['team']['icon']['image_132']
            _team_context = self._create_context({
                'team': team_context
            })
        return _team_context['data']

    def _clean_users(self, users):
        cleaned_users = []
        for user in users:
            if user['id'] != 'USLACKBOT' and not user['is_bot'] and not user['deleted']:
                cleaned_users.append(user)
        return cleaned_users

    def _get_users_context(self, slack_instance):
        global _users_context, _users_context_timeout
        if self._context_expired(_users_context, _users_context_timeout):
            slack_user_response = slack_instance.get_users()
            users_total = self._clean_users(slack_user_response['members'])
            users_online = [user for user in users_total
                            if 'presence' in user and user['presence'] == 'active']
            _users_context = self._create_context({
                'users': users_total,
                'users_online': len(users_online),
                'users_total': len(users_total),
            })
        return _users_context['data']

    def slackin_context(self):
        slack = Slack(token=settings.SLACKIN_TOKEN, subdomain=settings.SLACKIN_SUBDOMAIN)
        context = {}
        context.update(self._get_team_context(slack))
        context.update(self._get_users_context(slack))
        return context

class SlackinInviteView(SlackinMixin, View):
    template_name = 'slackin/invite/page.html'

    def get_generic_context(self):
        return {
            'slackin': self.slackin_context(),
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
        if settings.SLACKIN_LOGIN_REQUIRED and not self.request.user.is_authenticated():
            return HttpResponseRedirect(self.get_redirect_url())

        self.context = self.get_generic_context()

        email_address = ''
        if self.request.user.is_authenticated():
            email_address = self.request.user.email
        self.context['slackin_invite_form'] = SlackinInviteForm(
            initial={'email_address': email_address},
            user=self.request.user)
        return self.response()

    def post(self, request):
        if settings.SLACKIN_LOGIN_REQUIRED and not self.request.user.is_authenticated():
            return HttpResponseRedirect(self.get_redirect_url())

        self.context = self.get_generic_context()
        invite_form = SlackinInviteForm(self.request.POST, user=self.request.user)
        if invite_form.is_valid():
            self.context['slackin_invite_form_success'] = True
        self.context['slackin_invite_form'] = invite_form
        return self.response()


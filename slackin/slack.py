import requests
import json

from slackin.signals import sent_invite_to_email_address


class SlackError(Exception):
    def __init__(self, message):
        super(SlackError, self).__init__(message)

class Slack(object):
    def __init__(self, token, subdomain):
        self.token = token
        self.subdomain = subdomain

    def api_request(self, api, data={}):
        url = 'https://{}.slack.com/api/{}'.format(self.subdomain, api)
        data['token'] = self.token
        response = requests.post(url, data=data)
        if response.status_code == 200:
            response_dict = response.json()
            if 'error' in response_dict:
                self.handle_error(response_dict['error'])
            return response_dict
        else:
            raise SlackError('Slack: Invalid API request')

    def handle_error(self, error_code):
        if error_code == 'not_authed':
            raise SlackError('Missing Slack token. Please contact an administrator.')
        elif error_code == 'invalid_auth':
            raise SlackError('Invalid Slack token. Please contact an administrator.')
        elif error_code == 'account_inactive':
            raise SlackError('Slack token is inactive. Please contact an administrator.')

        # invite errors
        elif error_code == 'missing_scope':
            raise SlackError('Slack token is for a non-admin user. Please contact an administrator.')
        elif error_code == 'already_invited':
            raise SlackError('That email address has already been invited.')
        elif error_code == 'already_in_team':
            raise SlackError('That email address is already in this team.')
        elif error_code == 'paid_teams_only':
            raise SlackError('{} {}'.format(
                'Ultra-restricted invites are only available for paid accounts.',
                'Please contact an administrator.'))
        else:
            raise SlackError('Unknown error: {}'.format(error_code))

    def get_team(self):
        return self.api_request('team.info')

    def get_users(self):
        return self.api_request('users.list', data={
            'presence': 1
        })

    def invite_user(self, email_address, ultra_restricted=False):
        response = self.api_request('users.admin.invite', data={
            'email': email_address,
            'set_active': True,
            'ultra_restricted': int(ultra_restricted),
        })

        sent_invite_to_email_address.send(sender=self.__class__, email_address=email_address)

        return response

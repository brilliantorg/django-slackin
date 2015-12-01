from django import forms

from slackin.conf import settings
from slackin.slack import Slack, SlackError


class SlackinInviteForm(forms.Form):
    email_address = forms.EmailField(required=True)

    def clean_email_address(self):
        email_address = self.cleaned_data['email_address']

        slack = Slack(token=settings.SLACKIN_TOKEN, subdomain=settings.SLACKIN_SUBDOMAIN)
        try:
            invitation = slack.invite_user(email_address=email_address,
                                           ultra_restricted=settings.SLACKIN_ULTRA_RESTRICTED_INVITES)
        except SlackError as err:
            raise forms.ValidationError(err)
        
        return email_address

    def __init__(self, *args, **kwargs):
        super(SlackinInviteForm, self).__init__(*args, **kwargs)
        if settings.SLACKIN_SHOW_EMAIL_FORM:
            self.fields['email_address'].widget.attrs['placeholder'] = 'Email address'
        else:
            self.fields['email_address'].widget = forms.HiddenInput()

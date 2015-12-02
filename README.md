# django-slackin

Django integration with a public slack organization (inspired by https://github.com/rauchg/slackin).


## Installation & setup

Install django-slackin

```bash
# (coming soon)
# pip install django-slackin
```

Add to your `INSTALLED_APPS`

```python
INSTALLED_APPS = (
    ...
    'slackin',
)
```

Include the django-slackin URLconf in your project urls.py like this

```python
url(r'^slackin/', include('slackin.urls')),
```

Update your settings.py

```python
SLACKIN_TOKEN = 'YOUR-SLACK-TOKEN' # create a token at https://api.slack.com/web
SLACKIN_SUBDOMAIN = 'your-team'    # if https://your-team.slack.com

# optional settings
SLACKIN_ULTRA_RESTRICTED_INVITES = True # only available for paid accounts
SLACKIN_SHOW_EMAIL_FORM = True          # show/hide email form
```

Visit [http://localhost:8000/slackin/](http://localhost:8000/slackin/) to send an invite to your Slack team.


## Using signals

Use signals to listen for invite events. Available signals are:
- email_address_already_invited
- email_address_already_in_team
- sent_invite_to_email_address

To listen for a signal:

```python
from slackin.signals import sent_invite_to_email_address

@receiver(sent_invite_to_email_address)
def my_invite_handler(sender, email_address, **kwargs):
    print 'SIGNAL RECEIVED: {}'.format(email_address)
```

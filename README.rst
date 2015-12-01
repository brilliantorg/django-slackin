==========================
django-slackin!
==========================

Quick start
--------------------------

1. Install django-slackin::

    $ pip install django-slackin

2. Add to your `INSTALLED_APPS`::

    INSTALLED_APPS = (
        ...
        'slackin',
    )

2. Include the django-slackin URLconf in your project urls.py like this::

    url(r'^slackin/', include('slackin.urls')),

3. Add the required settings::

    SLACKIN_TOKEN = 'YOUR SLACK TOKEN' # create a token at https://api.slack.com/web
    SLACKIN_SUBDOMAIN = 'your-team' # if https://your-team.slack.com
    # optional settings
    SLACKIN_ULTRA_RESTRICTED_INVITES = True # only available for paid accounts
    SLACKIN_SHOW_EMAIL_FORM = True # show/hide email form

4. Visit http://localhost:8000/slackin/ to send an invite to your Slack team.

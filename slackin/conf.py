from django.conf import settings as django_settings

def get_default_settings(settings):
    settings.SLACKIN_TOKEN = getattr(settings, 'SLACKIN_TOKEN', None)
    settings.SLACKIN_SUBDOMAIN = getattr(settings, 'SLACKIN_SUBDOMAIN', None)
    settings.SLACKIN_ULTRA_RESTRICTED_INVITES = getattr(
        settings, 'SLACKIN_ULTRA_RESTRICTED_INVITES', True)
    settings.SLACKIN_SHOW_EMAIL_FORM = getattr(settings, 'SLACKIN_SHOW_EMAIL_FORM', True)
    return settings

settings = get_default_settings(django_settings)

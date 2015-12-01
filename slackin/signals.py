from django.dispatch import Signal


sent_invite_to_email_address = Signal(providing_args=['email_address'])

from django.dispatch import Signal

email_address_already_invited = Signal(providing_args=['email_address'])
email_address_already_in_team = Signal(providing_args=['email_address'])
sent_invite_to_email_address = Signal(providing_args=['email_address'])

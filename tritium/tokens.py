from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, Profile, timestamp):
        return (
            six.text_type(Profile.usafa_id) + six.text_type(timestamp) +
            six.text_type(Profile.email_verified)
        )

account_activation_token = AccountActivationTokenGenerator()
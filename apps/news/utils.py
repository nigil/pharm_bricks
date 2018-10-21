from django.core.signing import Signer, BadSignature
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import reverse


class UserUnsubscriber(object):
    _salt = 'pharm'

    def __init__(self):
        self.signer = Signer(salt=self._salt)

    def make_unsubscribe_link(self, email):
        base64_email = urlsafe_base64_encode(email)
        token = self.signer.sign(email).split(':')[1]

        return '{hostname}{path}'.format(
            hostname=settings.HOSTNAME,
            path=reverse('unsubscribe_news', args=(base64_email, token)),
        )

    def parse_unsubscribe_link(self, base64_email, token):
        """
        If link is valid, return user's email
        """
        email = urlsafe_base64_decode(base64_email)

        try:
            unsigned_token = self.signer.unsign('{}:{}'.format(email, token))

            if unsigned_token == email:
                return email
        except BadSignature:
            pass

        return False

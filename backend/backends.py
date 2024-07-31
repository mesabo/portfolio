import requests
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings

class GmailOAuth2Backend(EmailBackend):
    def _send(self, email_message):
        if not email_message.recipients():
            return False
        self.connection = self.open()
        if not self.connection:
            return False
        auth_string = self._get_oauth2_auth_string()
        self.connection.ehlo_or_helo_if_needed()
        self.connection.auth('XOAUTH2', auth_string)
        return super()._send(email_message)

    def _get_oauth2_auth_string(self):
        access_token = self._get_access_token()
        auth_string = 'user={}\1auth=Bearer {}\1\1'.format(settings.EMAIL_HOST_USER, access_token)
        return auth_string

    def _get_access_token(self):
        token_url = 'https://oauth2.googleapis.com/token'
        payload = {
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'refresh_token': settings.GOOGLE_REFRESH_TOKEN,
            'grant_type': 'refresh_token'
        }
        response = requests.post(token_url, data=payload)
        response_data = response.json()
        if 'access_token' not in response_data:
            raise Exception("Unable to obtain access token")
        return response_data['access_token']

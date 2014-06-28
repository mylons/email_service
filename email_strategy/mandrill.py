import requests
import json
import os
from email_strategy.email import Email


class Mandrill(Email):

    def __init__(self):
        Email.__init__(self)
        self.api_key = os.getenv('MANDRILL_API_KEY')
        self.server = os.getenv('MANDRILL_SERVER')

    def send_email(self, to_field, from_field, subject_field, body_text):
        payload = {
            'key': self.api_key,
            'message': {
                'text': body_text,
                'subject': subject_field,
                'from_email': from_field,
                'to': [{'email': to_field}]
            }
        }
        return requests.post(self.server, data=json.dumps(payload))
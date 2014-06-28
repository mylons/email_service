import requests
import json
import os
from email_strategy.email import Email
from util.html_tools import strip_tags


class Mandrill(Email):

    def __init__(self):
        Email.__init__(self)
        self.api_key = os.getenv('MANDRILL_API_KEY')
        self.server = os.getenv('MANDRILL_SERVER')

    def send_email(self, to_field, from_field, subject_field, body_text):
        payload = {
            'key': self.api_key,
            'message': {
                'text': strip_tags(body_text),
                'subject': subject_field,
                'from_email': from_field,
                'to': [{'email': to_field}]
            }
        }
        return requests.post(self.server, data=json.dumps(payload))

    def evaluate_timeout(self, response):
        j = response.json()
        if 'status' in j and j['status'] == 'error':
            self.timeout = True
        else:
            self.timeout = False

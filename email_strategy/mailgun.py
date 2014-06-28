import os
import requests
from email_strategy.email import Email
from util.html_tools import strip_tags


class MailGun(Email):

    def __init__(self):
        Email.__init__(self)
        self.server = os.getenv('MAILGUN_SERVER')
        self.api_key = os.getenv('MAILGUN_API_KEY')

    def send_email(self, to_field, from_field, subject_field, body_text):
        return requests.post(
            self.server,
            auth=("api", self.api_key),
            data={"from": from_field,
                  "to": to_field,
                  "subject": subject_field,
                  "text": strip_tags(body_text)})

    def evaluate_timeout(self, response):
        if response.status_code != requests.codes.ok:
            self.timeout = True
        else:
            self.timeout = False

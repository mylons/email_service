import os
import requests
from email_strategy.email import Email, Singleton
from util.html_tools import strip_tags


class MailGun(Email):

    def __init__(self, *args, **kwargs):
        Email.__init__(self, *args)
        self.server = os.getenv('MAILGUN_SERVER')
        self.api_key = os.getenv('MAILGUN_API_KEY')

    def send_email(self, to_name, to_field, from_name, from_field, subject_field, body_text):
        return requests.post(
            self.server,
            auth=("api", self.api_key),
            data={"from": "%s <%s>" % (from_name, from_field),
                  "to": "%s <%s>" % (to_name, to_field),
                  "subject": subject_field,
                  "text": strip_tags(body_text)})

    def evaluate_timeout(self, response):
        if response.status_code != requests.codes.ok:
            self.timeout = True
        else:
            self.timeout = False

__author__ = 'mylons'
from email_strategy.mailgun import MailGun
from email_strategy.mandrill import Mandrill
from email_strategy.email import Email

class EmailFactory(object):
    """
    returns an object capable of sending emails
    """
    def __init__(self):
        self.mg = MailGun()
        self.md = Mandrill()

    def get_emailer(self):
        if not self.md.timeout:
            return self.md
        elif not self.mg.timeout:
            return self.mg
        else:
            return Email

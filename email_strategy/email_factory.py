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
        if not self.mg.timeout:
            return self.mg
        elif not self.md.timeout:
            return self.md
        else:
            # TODO
            # not sure what to do if both are timed out, what's a good way to get
            # back to a state where one might be up?
            return Email

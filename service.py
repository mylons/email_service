from flask import Flask
from flask import request
import requests

from email_strategy.email_factory import EmailFactory

from util import validator
from util.validator import ValidationError

#################
# initial setup #
#################


# setup the db
import os
from flask.ext.sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))
# get a flask instance
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

DB = SQLAlchemy(app)

# pre cache some objects/lists
# USING CAPS FOR GLOBALS
JSON_KEYS = ['to', 'to_name', 'from', 'from_name', 'subject', 'body']
JSON_VALIDATOR = validator.JSON()
STR_VALIDATOR = validator.StringLength(the_min=2)
EMAIL_VALIDATOR = validator.Email()

# email factory
EMAIL_FACTORY = EmailFactory()


@app.route('/email', methods=['POST'])
def process_json():
    """
    json spec (k: v):
     to: email address in to field
     to_name: the name to accompany the email
     from: email address in from field
     from_name: name to accompany from/reply emails
     subject: subject line of the email
     body: the html of the body of the email
    all fields required

    only accepts POST requests
    only operates on JSON data
    """
    try:
        if valid(request.json):
            req = send_email(request.json)
            # save to db ass successful
            insert_in_db(request.json, True)
            return req.url, 200
        else:
            insert_in_db(request.json, False)
            return "<p>return fail</p>", 400
    except ValidationError as e:
        insert_in_db(request.json, False)
        return "<p>failed {}</p>".format(e), 400


def valid(the_json):
    """
    validates json before attempting to send an email
    :param the_json: json from the request.json
    :return: true or raises ValidationError
    """
    # validate json -- return true/false
    # these call functions throw exceptions
    try:
        # validate required json keys are there
        JSON_VALIDATOR(JSON_KEYS, the_json)
        # validate those fields have strings with some content
        for k in JSON_KEYS:
            STR_VALIDATOR(k, the_json[k])
        # validate email format
        EMAIL_VALIDATOR(the_json['to'])
        EMAIL_VALIDATOR(the_json['from'])

    except ValidationError as e:
        raise e

    return True


def send_email(the_json):
    """
    sends the email using a client implementation of email_strategy.Email
    :param the_json: parsed and validated json
    :return: response object
    """
    # send the email out
    e = EMAIL_FACTORY.get_emailer()
    r = e.send_email(the_json['to_name'],
                     the_json['to'],
                     the_json['from_name'],
                     the_json['from'],
                     the_json['subject'],
                     the_json['body'])
    # this allows the email object to update itself without the service
    # having to worry about the codes from different providers
    e.evaluate_timeout(r)
    return r


def insert_in_db(the_json, success):
    """
    insert an email into the DB with status via the json
    :param the_json: parsed, and validated json
    :param success: whether the email was sent successfully or not
    :return: None
    """
    DB.session.add(email_record_from_json(the_json, success))
    DB.session.commit()


def email_record_from_json(the_json, success):
    """
    helper function to build emailrecords from json
    :param the_json: the parsed and validated json
    :param success: true if the email was sent successfully
    :return: EmailRecord
    """
    return EmailRecord(to_email=the_json['to'],
                       to_name=the_json['to_name'],
                       from_email=the_json['from'],
                       from_name=the_json['from_name'],
                       subject=the_json['subject'],
                       body=the_json['body'],
                       sent=success)


class EmailRecord(DB.Model):
    """
    model class for the database
    """
    __tablename__ = 'email'
    email_id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    to_email = DB.Column(DB.String(256))
    to_name = DB.Column(DB.String(256))
    from_email = DB.Column(DB.String(256))
    from_name = DB.Column(DB.String(256))
    subject = DB.Column(DB.String())
    body = DB.Column(DB.String())
    sent = DB.Column(DB.Boolean())

    def __repr__(self):
        return '<Email {} {} {}>'.format(self.to_email,
                                         self.from_email,
                                         self.subject)

if __name__ == '__main__':
    app.run(debug=True)

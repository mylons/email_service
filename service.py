from flask import Flask
from flask import request

from util import validator
from util.validator import ValidationError

# get a flask instance
app = Flask(__name__)
# pre cache some objects/lists
json_keys = ['to', 'to_name', 'from', 'from_name', 'subject', 'body']
json_validator = validator.JSON()
str_validator = validator.StringLength(the_min=2)
email_validator = validator.Email()


@app.route('/email', methods=['POST'])
def email():
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
    app.logger.debug(request.json)
    if valid(request.json):
        app.logger.debug("json is valid")
        send_email(request.json)
    else:
        app.logger.debug("json not valid")
    return "lawl"


def valid(the_json):
    #validate -- return true/false
    # these call functions throw exceptions
    try:
        # validate required json keys are there
        json_validator(json_keys, the_json)
        # validate those fields have strings with some content
        for k in json_keys:
            app.logger.debug("validating %s: %s" % (k, the_json[k]))
            str_validator(k, the_json[k])
        # validate email format
        email_validator('to', the_json['to'])
        email_validator('from', the_json['from'])

    except ValidationError:
        return False

    return True

def send_email(the_json):
    # send the email out


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask
# get a flask instance
app = Flask(__name__)

@app.route('/email')
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

    :return:
    """
    # get json

    # validate json

    #
    return '<p> email sent </p>'


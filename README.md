# RUN
The following environment variables need to be defined:
    MAILGUN_SERVER
    MAILGUN_API_KEY
    MANDRILL_API_KEY
    MANDRILL_SERVER

# setup
use virtualenv to setup a python3.3 environment

# install packages
pip install -r requirements.txt

# run tests
py.test tests.py

# init the database
python init_db.py

# run email service
python service.py

you should now be able to curl the address output by the program:
    curl -H "Content-Type: application/json" -d '{ "to": "mrlyons@gmail.com", "to_name": "Mike Lyons", "from": "noreply@uber.com", "from_name": "Uber", "subject": "Testing your code", "body": "<h1>Your Test</h1><p>complete</p>" }' 127.0.0.1:5000/email

# General notes on the design and application itself

It requires python 3.3! I did this for a two reasons:
  1. There are neat features in Python 3 that I wanted to
     explore like the new metaclass features, etc

  2. I haven't used Python 3 for a project yet.

  With that said, I wouldn't insist on using python3.x at Uber. I
  thought it would be a neat feature to this project.

Chose to use flask for handling the route and endpoint abstractions.
Using flask I easily setup a web app that only responds to post requests
to /email with a json payload.

Use the requests library for abstractions around the core python http libs
which are pretty ancient, and counter-intuitive to most modern web programmers.

Used the built in unittest package for testing, but have been relying on
py.test to actually run and oversee the tests. The decision to use
py.test is due to its ability to do generic testing without subclassing
the unittest.TestCase class. Automatic test discovery is also nice, and there
are other features that, if this project were to have a long future, could be
taken advantage of for larger test suites. This should make it more sustainable
for testing long term.

Also used the coverage package for a very high level evaluation of my code's
test coverage.

# additional features
The util.validator package provides more robust validation than just checking
if the required fields are there. It is capable of performing string length
validation, email format validation, and validating the json.

The email implementation classes are singletons to limit object creation in a
theoretically hig load system. the Email class is also meant to be abstract. I was
attempting to use the ABCMeta as its' metaclass, but was conflicting with my singleton
inheritance in the sub classes of Email. So, Email's in a createable state now, but
has abstract methods and as such is useless.

email_factory provides a dynamic switching between mailgun and mandrill. if one
client returns an error code, it notes itself as timed out, and the factory will
try to deliver the other functioning client.

Currently there's no way to attempt to rescue a timeout status. So, if both providers
time out eventually, and the application is never restarted, there will be no way to
send email.

This could be solved by having a load balancer in front of this application
and having a few instances of this web app running on servers behind the balancer. That
would eliminate the risk of downtime from a hardware angle.

From a software perspective, you could tweak email_factory to occasionally re-check a failed
email client, and shoot off a test email, and bring the client back into rotation if it is
successful -- trickier to implement.

Regarding the database: this is making use of sqlite3 just to show that I can use a
database. If it were in production, it'd be using something like Postgresql and possibly
on a remote box. Those are simply additional parameters or config options to
SQLAlchemy.

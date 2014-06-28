__author__ = 'mylons'

import re


class ValidationError(ValueError):
    """
    Raised when /email POST json is not valid
    """
    def __init__(self, message='', *args, **kwargs):
        ValueError.__init__(self, message, *args, **kwargs)


class StringLength(object):
    """
    validates the length of a string

    :param min:
        The minimum length of the string.
        If None, will not enforce
    :param max:
        The max length of the string.
        If None, will not enforce
    :param message:
        Error message if validation error
    """

    def __init__(self, the_min=None, the_max=None, message=''):
        assert the_min is not None or the_max is not None, 'Need a min or a max.'
        assert the_max is None or the_min <= the_max, 'max cannot be less than min'
        self.the_min = the_min
        self.the_max = the_max
        self.message = message

    def __call__(self, field, the_string):
        # check type
        if type(the_string) is not str:
            raise ValidationError("%s must be a string" % field)
        # validate
        l = len(the_string)
        if (self.the_min and self.the_min > l) or (self.the_max and self.the_max < l):
            message = self.message
            if message is None:
                if self.the_max is None:
                    message = "%s must be at least %s characters" % (field, self.the_min)
                elif self.the_min is None:
                    message = "%s must be less than %s characters" % (field, self.the_max)
            raise ValidationError(message)
        # string must be valid at this point


class Email(object):
    """
    Validates the email address with a primitive regex.
    Does not guarantee real email address.

    :param message:
        Error message if validation error
    """
    def __init__(self, message=None):
        self.regex = re.compile(r'^.+@[^.].*\.[a-z]{2,10}$', re.IGNORECASE)
        self.message = message

    def __call__(self, field, email):
        message = self.message
        if message is None:
            message = "Invalid email address"

        if not self.regex.match(email or ''):
            raise ValidationError(message)


class JSON(object):
    """
    validates that all required fields of json are present.
    very primitive validator -- only checks first level
    of json keys

    :param message:
        Error message if validation error
    """
    def __init__(self, message=None):
        self.message = message

    def __call__(self, fields, the_json):
        try:
            for field in fields:
                if field not in the_json:
                    message = self.message
                    if message is None:
                        message = "required field %s not in json" % field
                    raise ValidationError(message)
        except (KeyError, TypeError) as e:
            raise ValidationError("invalid json string %s" % e)



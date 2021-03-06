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
    :param min: The minimum length of the string. If None, will not enforce
    :param max: The max length of the string. If None, will not enforce
    :param message: Error message if validation error
    """

    def __init__(self, the_min=-1, the_max=-1, message=None):
        assert the_min != -1 or the_max != -1, \
            'Need a min or a max.'
        assert the_max == -1 or the_min <= the_max, \
            'max cannot be less than min'
        self.the_min = the_min
        self.the_max = the_max
        self.message = message

    def __call__(self, field, the_string):
        """
        raises exception if string isn't valid
        :param field: name of the field as a string
        :param the_string: string to validate
        :return: None
        """
        if type(the_string) is not str:
            raise ValidationError("%s must be a string" % field)
        # validate
        l = len(the_string)
        if (self.the_min > 0 and self.the_min > l) or \
                (self.the_max > 0 and self.the_max < l):
            message = self.message
            if message is None:
                if self.the_max < 0:
                    message = "%s must be at least %s characters" \
                              % (field, self.the_min)
                elif self.the_min < 0:
                    message = "%s must be less than %s characters" \
                              % (field, self.the_max)
            raise ValidationError(message)
        # string must be valid at this point


class Email(object):
    """
    Validates the email address with a primitive regex.
    Does not guarantee real email address.

    :param message: Error message if validation error
    """
    def __init__(self, message=None):
        self.regex = re.compile(r'^.+@[^.].*\.[a-z]{2,10}$', re.IGNORECASE)
        self.message = message

    def __call__(self, email):
        """
        raises ValidationError if email is out of range
        :param email: email address as a string
        :return: None
        """
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
        """
        :param fields: collection of the keys in
        the json that are required to be there
        :param the_json: parsed json to validate
        :return: None
        """
        for field in fields:
            if field not in the_json:
                message = self.message
                if message is None:
                    message = "required field %s not in json" % field
                raise ValidationError(message)

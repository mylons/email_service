import abc


class Email(object):
    """
    base class for emails
    it is a singleton by design.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self._timeout = False

    # enforces singleton for sub classes
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'self'):
            cls.self = object.__new__(cls)
        return cls.self

    @abc.abstractmethod
    def send_email(self, to_field, from_field, subject_field, body_text):
        raise NotImplementedError

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        if not isinstance(value, bool):
            raise TypeError('Expected boolean')
        self._timeout = value



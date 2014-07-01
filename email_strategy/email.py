import abc


class Singleton(type):
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)
        return self.__instance

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = super().__call__(*args, **kwargs)
            return self.__instance
        else:
            return self.__instance



class Email(metaclass=Singleton):
    """
    base class for emails
    it is a singleton by design.
    """
    def __init__(self):
        self._timeout = False

    @abc.abstractmethod
    #json_keys = ['to', 'to_name', 'from', 'from_name', 'subject', 'body']
    def send_email(self, to_name, to_field, from_name, from_field, subject_field, body_text):
        raise NotImplementedError

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        if not isinstance(value, bool):
            raise TypeError('Expected boolean')
        self._timeout = value

    @abc.abstractmethod
    def evaluate_timeout(self, response):
        raise NotImplementedError

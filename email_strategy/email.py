from abc import abstractmethod


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
        super().__init__()
        self._timeout = False

    def __call__(self, *args, **kwargs):
        raise TypeError("Can't instantiate directly")

    @abstractmethod
    def send_email(self, to_name, to_field, from_name, from_field, subject_field, body_text):
        """
        Sends the email
        :param to_name: the non-email recipient name
        :param to_field: recipient email
        :param from_name: the non-email sender name
        :param from_field: sender email
        :param subject_field: subject of the email
        :param body_text: body of email (may include html)
        :return:
        """
        pass

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        if not isinstance(value, bool):
            raise TypeError('Expected boolean')
        self._timeout = value

    @abstractmethod
    def evaluate_timeout(self, response):
        pass

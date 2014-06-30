import unittest
from util.validator import (StringLength, Email, ValidationError)


class StringLengthTests(unittest.TestCase):

    def setUp(self):
        self.mn = StringLength(the_min=1)
        self.mx = StringLength(the_max=5)
        self.rg = StringLength(the_min=1, the_max=5)

    def test_min_length_raise(self):
        with self.assertRaises(ValidationError):
            self.mn('test', 'test')

    def test_max_length_raise(self):
        with self.assertRaises(ValidationError):
            self.mx('testing', 'testing')

    def test_string_in_range(self):
        self.assertEqual(self.rg('test', 'test'), None)

    def test_string_out_of_range(self):
        with self.assertRaises(ValidationError):
            self.rg('testing', 'testing')

    def test_type_check(self):
        with self.assertRaises(ValidationError):
            self.mn('field', 1)

    def test_message_at_least(self):
        #message = "%s must be at least %s characters"
        pass

class EmailValidationTests(unittest.TestCase):

    def setUp(self):
        self.e = Email()

    def test_valid_email(self):
        self.assertEqual(self.e('testing@uber.com'), None)

    def test_invalid_email_no_dot_com(self):
        with self.assertRaises(ValidationError):
            self.e('testing@uber')

    def test_invalid_email_no_text_after_at_symbol(self):
        with self.assertRaises(ValidationError):
            self.e('testing@')


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()


if __name__ == '__main__':
    unittest.main()

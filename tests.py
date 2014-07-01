# python built ins
import unittest
import json

# project packages
from util.validator import (StringLength, Email as EmailValidator, JSON, ValidationError)
from email_strategy.mailgun import MailGun
import service


class StringLengthTests(unittest.TestCase):

    def setUp(self):
        self.mn = StringLength(the_min=2)
        self.mx = StringLength(the_max=5)
        self.rg = StringLength(the_min=1, the_max=5)

    def test_min_length_raise(self):
        with self.assertRaises(ValidationError):
            self.mn('test', 't')

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
        try:
            self.mn('test', '1')
        except ValidationError as e:
            self.assertEqual(e.__str__(),
                             "{} must be at least {} characters".format('test', self.mn.the_min))

    def test_message_at_most(self):
        try:
            self.mx('test', '555555')
        except ValidationError as e:
            self.assertEqual(e.__str__(),
                             "{} must be less than {} characters".format('test', self.mx.the_max))

class EmailValidationTests(unittest.TestCase):

    def setUp(self):
        self.e = EmailValidator()

    def test_valid_email(self):
        self.assertEqual(self.e('testing@uber.com'), None)

    def test_invalid_email_no_dot_com(self):
        with self.assertRaises(ValidationError):
            self.e('testing@uber')

    def test_invalid_email_no_text_after_at_symbol(self):
        with self.assertRaises(ValidationError):
            self.e('testing@')


class JSONValidationTests(unittest.TestCase):

    def setUp(self):
        import json
        self.valid_json = json.loads('{"key1": 1, "key2": 2, "key3": 3}')
        self.invalid_key_json = json.loads('{"key": 1, "key2": 2, "key3": 3}')
        self.keys = ['key1', 'key2', 'key3']
        self.jv = JSON()

    def test_valid_json(self):
        self.assertEqual(self.jv(self.keys, self.valid_json), None)

    def test_invalid_key_json(self):
        with self.assertRaises(ValidationError):
            self.jv(self.keys, self.invalid_key_json)


class ServiceTests(unittest.TestCase):

    def setUp(self):
        service.app.config['TESTING'] = True
        self.app = service.app.test_client()
        self.uber_json_str = '{"to": "fake@example.com", "to_name": "Ms. Fake", "from": "noreply@uber.com", "from_name": "Uber", "subject": "A Message from Uber", "body": "<h1>Your Bill</h1><p>$10</p>"}'
        self.uber_json_str_missing_keys = '{"to1": "fake@example.com", "to_name2": "Ms. Fake", "from": "noreply@uber.com", "from_name": "Uber", "subject": "A Message from Uber", "body": "<h1>Your Bill</h1><p>$10</p>"}'

    def test_process_json_response_code_200(self):
        resp = self.app.post('/email',
                             data=self.uber_json_str,
                             content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_process_json_response_code_400(self):
        resp = self.app.post('/email',
                             data="this isn't json",
                             content_type='application/json')
        self.assertEqual(resp.status_code, 400)

    def test_invalid_json(self):
        self.assertEqual(service.valid(json.loads(self.uber_json_str_missing_keys)), False)

    def test_valid_json(self):
        self.assertEqual(service.valid(json.loads(self.uber_json_str)), True)


class HTMLStripTest(unittest.TestCase):

    def setUp(self):
        self.html = '<h1>test</h1>'

    def test_html_strip(self):
        from util.html_tools import strip_tags
        self.assertEqual(strip_tags(self.html), 'test')


class EmailTests(unittest.TestCase):

    def setUp(self):
        self.mg_a = MailGun()
        self.mg_b = MailGun()

    def test_same_object(self):
        """
        From the python manual
        Return the ``identity'' of an object. This is an integer (or long integer)
        which is guaranteed to be unique and constant for this object during its
        lifetime. Two objects with non-overlapping lifetimes may have the same id()
        value. (Implementation note: this is the address of the object.)
        :return:
        """
        self.assertEqual(id(self.mg_a), id(self.mg_b))

    def test_member_variable_change(self):
        self.mg_a.timeout = True
        self.assertEqual(self.mg_a.timeout, self.mg_b.timeout)

if __name__ == '__main__':
    unittest.main()

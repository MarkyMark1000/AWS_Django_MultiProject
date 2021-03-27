from django.test import TestCase, RequestFactory
from django.core import mail
import unittest
from unittest import mock
import sendemail.extra_code_or_config.getIP as GI

# I found the following article interesting and useful:
# https://simpleisbetterthancomplex.com/questions/2017/07/07/mocking-emails.html

# The Django tests do not send an actual email, so you need to
# double check that this is working in the production environment.

EMAIL_TO_ADDRESS = 'mark_john_wilson@yahoo.co.uk'

class MockResponse:
    def __init__(self, text):
        self.text = text


class AWSTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_getIP(self):
        with mock.patch("sendemail.extra_code_or_config.getIP.requests.get") as gt:
            lst = []
            gt.return_value = MockResponse('99.98.97.96')
            GI.appendIPToArray(lst)
            self.assertIn('99.98.97.96', lst)

    def test_getIP_adds_once(self):
        with mock.patch("sendemail.extra_code_or_config.getIP.requests.get") as gt:
            lst = ['99.98.97.96']
            gt.return_value = MockResponse('99.98.97.96')
            GI.appendIPToArray(lst)
            self.assertEqual(len(lst), 1)

    def test_getFalseIP(self):
        with mock.patch("sendemail.extra_code_or_config.getIP.requests.get") as gt:
            lst = []
            gt.return_value = MockResponse(False)
            self.assertEqual(GI.appendIPToArray(lst), False)


class SendEmailTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_frontend_status(self):
        '''
        Check the front end returns status 200
        '''
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_frontend_content(self):
        '''
        Check the front end contains the desired text
        '''
        SEARCH_TEXT = '<input type="email"'
        response = self.client.get('/')
        self.assertContains(response, SEARCH_TEXT)

    def test_frontend_post(self):
        '''
        With this test, I post a valid version of the form,
        so it should actually send an email and I should
        get a valid response.
        '''

        SEARCH_TEXT = 'Success, your email has been sent.'

        postData = {
            'form_email': f"{EMAIL_TO_ADDRESS}",
                    }

        response = self.client.post("/", postData)
        # Ensure we get a 200 response
        self.assertEqual(response.status_code, 200)
        # Test the string in the response
        self.assertContains(response, SEARCH_TEXT)
        # Test to ensure an email has been received
        # (test won't send an actual email)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].body, 'Hello from a random user of sendemail Django App.')

    def test_frontend_invalid_post(self):
        '''
        With this test, I post an invalid version of the
        form and test the results.
        '''

        SEARCH_TEXT = 'Enter a valid email address.'

        postData = {
            'form_email': "myname_at_domain",
                    }

        response = self.client.post("/", postData)
        # We should get a 200 response
        self.assertEqual(response.status_code, 200)
        # Test the string in the response
        self.assertContains(response, SEARCH_TEXT)
        # Test to ensure an email has not been received
        # (test won't send an actual email)
        self.assertEqual(len(mail.outbox), 0)

    def test_error(self):
        '''
        Test error being raised when sending an email
        '''
        postData = {
            'form_email': f"{EMAIL_TO_ADDRESS}",
                    }

        #Add a patch here to raise an error within the code
        with mock.patch("sendemail.views.send_mail") as ge:

            ge.side_effect = Exception("Error has occurred")

            response = self.client.post("/", postData)

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Error has occurred")
            self.assertEqual(len(mail.outbox), 0)

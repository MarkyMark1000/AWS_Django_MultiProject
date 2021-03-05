from django.test import TestCase, RequestFactory
from django.core import mail

# I found the following article interesting and useful:
# https://simpleisbetterthancomplex.com/questions/2017/07/07/mocking-emails.html

# The Django tests do not send an actual email, so you need to
# double check that this is working in the production environment.

EMAIL_TO_ADDRESS = 'mark_john_wilson@yahoo.co.uk'

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
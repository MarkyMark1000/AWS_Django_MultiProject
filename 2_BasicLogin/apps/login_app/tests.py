from django.test import TestCase, RequestFactory
from django.core import mail
from apps.login_app.apps import LoginAppConfig
from django.apps import apps
from unittest import mock
from django.contrib.auth.models import User

EMAIL_TO_ADDRESS = 'mark_john_wilson@yahoo.co.uk'

class RegisterNewUserTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _register_new_user(self, registration_data):
        '''
        This registers a new user and makes sure that
        we get the appropriate response:

        Templates: register.html, activation_sent.html
        '''
        # Register new user:
        # register.html
        response = self.client.post("/accounts/register/",
                                    registration_data)

        # Doesn't return 200, but 302 and redirects
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/sent/")

        # Check redirection gets response from:
        # activation_sent.html
        response = self.client.get(response.url)
        SEARCH_TEXT = 'Activation link sent'
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, SEARCH_TEXT)

    def test_registration_page(self):
        '''
        Use get (not post) on registration page

        Templates: register.html
        '''
        response = self.client.get("/accounts/register/")

        # Doesn't return 200, but 302 and redirects
        self.assertEqual(response.status_code, 200)
        SEARCH_TEXT = 'Register New User'
        self.assertContains(response, SEARCH_TEXT)
        SEARCH_TEXT = 'Username'
        self.assertContains(response, SEARCH_TEXT)
        SEARCH_TEXT = 'Email'
        self.assertContains(response, SEARCH_TEXT)
        SEARCH_TEXT = 'Password confirmation'
        self.assertContains(response, SEARCH_TEXT)

    def test_valid_registration(self):
        '''
        Register a new user using the process that would
        typically be taken:

	    Templates Tested:   register.html, activation_sent.py,
                            activation_request.html
        '''

        registration_data = {
            'username': "TestUser",
            'email': 'test@email.com',
            'password1': "TestPWD_1",
            'password2': "TestPWD_1"
            }

        # Register the new user and make sure the response we
        # get is consistent (register.html, activation_sent.html)
        self._register_new_user(registration_data)

        # Check the mail to ensure it is consistent with:
        # activation_request.html
        SEARCH_TEXT = 'Please click the following link to confirm your registration'
        self.assertIn(SEARCH_TEXT, mail.outbox[0].body)

        # Now extract the activation link from the email, eg:
        # http://testserver/accounts/activate/MQ/aj3s3n-59f39d811176d95dc22a0bb4efb8808a/
        sent_email = mail.outbox[0].body
        start = sent_email.find('http:')
        link = sent_email[start:len(sent_email)].strip()

        # Follow the activation link.  It should redirect with
        # status code 302.   The redirected page should go to
        # the 'frontend', ie '/'
        response = self.client.get(link)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        # Get the redirected url and ensure that we can see the
        # username on the page
        response = self.client.get(response.url)
        self.assertContains(response, response.wsgi_request.user)

    def test_invalid_registration_link(self):
        '''
        Register a new user with an invalid activation link:

	    Templates Tested:   register.html, activation_sent.py,
                            activation_invalid.html,

        '''

        registration_data = {
            'username': "TestUser",
            'email': 'test@email.com',
            'password1': "TestPWD_1",
            'password2': "TestPWD_1"
            }

        # Register the new user and make sure the response we
        # get is consistent (register.html, activation_sent.html)
        self._register_new_user(registration_data)

        # Check the mail to ensure it is consistent with:
        # activation_request.html
        SEARCH_TEXT = 'Please click the following link to confirm your registration'
        self.assertIn(SEARCH_TEXT, mail.outbox[0].body)

        # Now extract the activation link from the email, eg:
        # http://testserver/accounts/activate/MQ/aj3s3n-59f39d811176d95dc22a0bb4efb8808a/
        sent_email = mail.outbox[0].body
        start = sent_email.find('http:')
        link = sent_email[start:len(sent_email)].strip()

        # Remove the second from last character from the url to
        # make it invalid.
        link_invalid = link[:-2] + link[-1:]

        # Follow the invalid activation link.   It should go to
        # the following:
        # activation_invalid.html
        response = self.client.get(link_invalid)
        SEARCH_TEXT = "Invalid user or activation token."
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, SEARCH_TEXT)

    def test_error_during_user_registration(self):
        '''
        This is largely for coverage to test when an error is
        raised when we follow the activation link:

	    Templates Tested:   register.html, activation_sent.py,
                            activation_request.html,
                            activation_invalid.html

        '''

        registration_data = {
            'username': "TestUser",
            'email': 'test@email.com',
            'password1': "TestPWD_1",
            'password2': "TestPWD_1"
            }

        # Register the new user and make sure the response we
        # get is consistent (register.html, activation_sent.html)
        self._register_new_user(registration_data)

        # Now extract the activation link from the email, eg:
        # http://testserver/accounts/activate/MQ/aj3s3n-59f39d811176d95dc22a0bb4efb8808a/
        sent_email = mail.outbox[0].body
        start = sent_email.find('http:')
        link = sent_email[start:len(sent_email)].strip()

        # When activating user, make it fail and get data from
        # activation_invalid.html
        with mock.patch("apps.login_app.views.User.objects.get") as gt:
            gt.side_effect = ValueError
            response = self.client.get(link)
            SEARCH_TEXT = "Invalid user or activation token."
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, SEARCH_TEXT)

    def test_register_unequal_password(self):
        '''
        Test registration with different passwords.
        '''

        registration_data = {
            'username': "TestUser",
            'email': 'test@email.com',
            'password1': "TestPWD_1",
            'password2': "TestPWD_2"
            }

        # Register new user:
        # register.html
        response = self.client.post("/accounts/register/",
                                    registration_data)

        # Returns 200 with invalid password message
        self.assertEqual(response.status_code, 200)
        SEARCH_TEXT = 'The two password fields did'
        self.assertContains(response, SEARCH_TEXT)

    def test_register_short_password(self):
        '''
        Test registration with short passwords.
        '''

        registration_data = {
            'username': "TestUser",
            'email': 'test@email.com',
            'password1': "AbC_1",
            'password2': "AbC_1"
            }

        # Register new user:
        # register.html
        response = self.client.post("/accounts/register/",
                                    registration_data)

        # Returns 200 with invalid password message
        self.assertEqual(response.status_code, 200)
        SEARCH_TEXT = 'Password must be at least 8 characters long'
        self.assertContains(response, SEARCH_TEXT)

    def test_register_numberless_password(self):
        '''
        Test registration without numers in password
        '''

        registration_data = {
            'username': "TestUser",
            'email': 'test@email.com',
            'password1': "AbCdEfG_h",
            'password2': "AbCdEfG_h"
            }

        # Register new user:
        # register.html
        response = self.client.post("/accounts/register/",
                                    registration_data)

        # Returns 200 with invalid password message
        self.assertEqual(response.status_code, 200)
        SEARCH_TEXT = 'Password must contain at least one digit'
        self.assertContains(response, SEARCH_TEXT)

    def test_register_characterless_password(self):
        '''
        Test registration without letters in password
        '''

        registration_data = {
            'username': "TestUser",
            'email': 'test@email.com',
            'password1': "1234567_8",
            'password2': "1234567_8"
            }

        # Register new user:
        # register.html
        response = self.client.post("/accounts/register/",
                                    registration_data)

        # Returns 200 with invalid password message
        self.assertEqual(response.status_code, 200)
        SEARCH_TEXT = 'Password must contain at least one letter'
        self.assertContains(response, SEARCH_TEXT)

    def test_register_password_withou_specialchar(self):
        '''
        Test registration for password without a special
        character.
        '''

        registration_data = {
            'username': "TestUser",
            'email': 'test@email.com',
            'password1': "AbCdEfG1",
            'password2': "AbCdEfG1"
            }

        # Register new user:
        # register.html
        response = self.client.post("/accounts/register/",
                                    registration_data)

        # Returns 200 with invalid password message
        self.assertEqual(response.status_code, 200)
        SEARCH_TEXT = 'Password must contain at least one special character'
        self.assertContains(response, SEARCH_TEXT)

    def test_apps(self):
        '''
        Largely for coverage, test login_app config.
        This test for apps was recommended here:
        https://stackoverflow.com/questions/43334953/testing-apps-py-in-django/45613899
        '''
        self.assertEqual(LoginAppConfig.name, 'login_app')
        self.assertEqual(apps.get_app_config('login_app').name,
                         'apps.login_app')

    def test_profile_string(self):
        '''
        Largely for coverage, test the str() representation
        of the Profile class in models.py
        '''
        temp_user = User.objects.create_user(
                        username='testuser',
                        email="abcd@efgh.com",
                        password='A1b2c3d_4')

        self.assertEqual(str(temp_user.profile), 'testuser')


class LoginTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_login_page(self):
        '''
		Login page with no post, ie get.

		Templates Tested:   login.py
        '''

        # SEARCH_TEXT response from login.py form
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        SEARCH_TEXT = 'Username:'
        self.assertContains(response, SEARCH_TEXT)
        SEARCH_TEXT = 'Password:'
        self.assertContains(response, SEARCH_TEXT)
        SEARCH_TEXT = 'Register'
        self.assertContains(response, SEARCH_TEXT)
        SEARCH_TEXT = 'Reset password'
        self.assertContains(response, SEARCH_TEXT)

    def test_invalid_login_post(self):
        '''
		Login when the account has not been setup with invalid
		credentials.

		Templates Tested:   login.py
        '''

        # From default login form.
        postData = {
            'username': "TestUser",
            'password': "TestPassword"}

        # SEARCH_TEXT response from login.py form
        response = self.client.post("/accounts/login/", postData)
        SEARCH_TEXT = 'Please enter a correct username and password'
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, SEARCH_TEXT)

    def test_valid_login_post(self):
        '''
		Login when the account has been setup.

		Templates Tested:   login.py
        '''
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='A1b2C3_d4')

        # for login form.
        postData = {
            'username': "testuser",
            'password': "A1b2C3_d4"}

        # Login using form
        response = self.client.post("/accounts/login/", postData)

        # Should redirect to 'frontend', ie '/'
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

    def test_logout(self):
        '''
        Take a logged in user and then follow the logout
        link.

        Templates Tested:   logged_out.py
        '''

        # Create a user and login
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='A1b2C3_d4')
        login = self.client.login(
            username='testuser',
            password='A1b2C3_d4')

        # Now follow the logged out link.
        # logged_out.html
        response = self.client.get("/accounts/logout/")
        SEARCH_TEXT = 'You have successfully logged out.'
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, SEARCH_TEXT)

class PasswordChangeTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_change_password_page(self):
        '''
		Create a logged in user, then follow link for
        user to change their password.

		Templates Tested:   login.py
        '''
        # Create a user and login
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='A1b2C3_d4')
        login = self.client.login(
            username='testuser',
            password='A1b2C3_d4')

        # SEARCH_TEXT response from login.py form
        response = self.client.get("/accounts/password_change/")
        self.assertEqual(response.status_code, 200)
        SEARCH_TEXT = 'Old password:'
        self.assertContains(response, SEARCH_TEXT)
        SEARCH_TEXT = 'New password:'
        self.assertContains(response, SEARCH_TEXT)

    def test_change_password(self):
        '''
		Create a logged in user, then post to the link to change
        the password

		Templates Tested:   password_change_form.html,
                            passowrd_change_done.html
        '''
        # Create a user and login
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='A1b2C3_d4')
        login = self.client.login(
            username='testuser',
            password='A1b2C3_d4')

        # for login form.
        postData = {
            'old_password': "A1b2C3_d4",
            'new_password1': "Banana_03",
            'new_password2': "Banana_03"}

        # Password change redirects (password_change_form.html)
        response = self.client.post("/accounts/password_change/",
                                    postData)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/password_change/done/")
        
        # Get redirected page and ensure the content is consistent
        # password_change_done.html
        response = self.client.get(response.url)
        SEARCH_TEXT = 'Password Changed'
        self.assertContains(response, SEARCH_TEXT)

class PasswordResetTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def _password_reset(self):
        '''
        Create a user, then request a password reset for the user.

        Templates: password_reset_form.html,
                   password_reset_done.html
        '''

        # Create a user and login
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='A1b2C3_d4')

        postData = {'email': "test@email.com"}

        # Password change form (password_reset_form.html)
        response = self.client.post("/accounts/password_reset/",
                                    postData)

        # Request redirected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/password_reset/done/")

        # Get redirected page and ensure the content is consistent
        # password_reset_done.html
        response = self.client.get(response.url)
        SEARCH_TEXT = 'emailed you instructions for setting your password'
        self.assertContains(response, SEARCH_TEXT)

    def test_reset_password_page(self):
        '''
		Login page with no post, ie get.

		Templates Tested:   password_reset_form.html
        '''
        # Create a user and login
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='A1b2C3_d4')

        # Ensure password reset is consistent with
        # password_reset_form.html
        response = self.client.get("/accounts/password_reset/")
        self.assertEqual(response.status_code, 200)
        SEARCH_TEXT = 'Send Password Reset'
        self.assertContains(response, SEARCH_TEXT)
        SEARCH_TEXT = 'Email:'
        self.assertContains(response, SEARCH_TEXT)

    def test_valid_password_reset(self):
        '''
		Go through the process of a password reset.   It
        is a bit long.

		Templates Tested:   password_reset_form.html,
                            password_reset_done.html,
                            password_reset_email.html,
                            password_reset_subject.txt,
                            password_reset_conform.html,

        '''

        # Get the reset password form and post
        self._password_reset()

        # Check the mail to ensure we get something consistent:
        # password_reset_email.html
        SEARCH_TEXT = 'A password reset was requested for the following account'
        self.assertIn(SEARCH_TEXT, mail.outbox[0].body)

        # Make sure the subject is same as:
        # password_reset_subject.txt
        SEARCH_TEXT = 'Password Reset Request'
        self.assertIn(SEARCH_TEXT, mail.outbox[0].subject)

        # Now extract the activation link from the email, eg:
        # http://testserver/accounts/activate/MQ/aj3s3n-59f39d811176d95dc22a0bb4efb8808a/
        sent_email = mail.outbox[0].body
        start = sent_email.find('http:')
        link = sent_email[start:len(sent_email)].strip()

        # Follow the activation link.  It should redirect with
        # status code 302.
        response = self.client.get(link)
        self.assertEqual(response.status_code, 302)

        # Now follow the link to the password reset
        # password_reset_conform.html
        str_url = response.url
        response = self.client.get(str_url)
        self.assertEqual(response.status_code, 200)
        SEARCH_TEXT = 'Please enter (and confirm) your new password'
        self.assertContains(response, SEARCH_TEXT)

        # Now actually change the password
        # for login form.
        postData = {
            'new_password1': "Banana_05",
            'new_password2': "Banana_05"}

        # Change the password
        response = self.client.post(str_url,
                                    postData)
        
        # Change in password redirects.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/reset/done/")

        # Get the actual response and ensure it is consisten with:
        # password_reset_complete.html
        str_url = response.url
        response = self.client.get(str_url)
        self.assertEqual(response.status_code, 200)
        SEARCH_TEXT = 'Password Reset Complete'
        self.assertContains(response, SEARCH_TEXT)

    def test_double_password_reset(self):
        '''
		Go through the process of a password reset when
        there are 2 accounts with the same password.

		Templates Tested:   password_reset_form.html,
                            password_reset_done.html,
                            password_reset_email.html,
                            password_reset_subject.txt,
                            password_reset_conform.html,

        '''

        # Get the reset password form and post
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='A1b2C3_d4')
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test@email.com',
            password='E1f2G3_h4')

        postData = {'email': "test@email.com"}

        # Password change form (password_reset_form.html)
        response = self.client.post("/accounts/password_reset/",
                                    postData)

        # Request redirected
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/accounts/password_reset/done/")

        # Get redirected page and ensure the content is consistent
        # password_reset_done.html
        response = self.client.get(response.url)
        SEARCH_TEXT = 'emailed you instructions for setting your password'
        self.assertContains(response, SEARCH_TEXT)

        # Make sure we have two emails in the outbox
        self.assertEqual(len(mail.outbox), 2)

        # Check the emails to ensure they look appropraite
        SEARCH_TEXT = 'A password reset was requested for the following account'
        SEARCH_TEXT2 = 'Password Reset Request'
        for i in range(len(mail.outbox)):

            self.assertIn(SEARCH_TEXT, mail.outbox[i].body)

            self.assertIn(SEARCH_TEXT2, mail.outbox[i].subject)


    def test_invalid_password_reset(self):
        '''
		Login page with no post, ie get.

		Templates: password_reset_form.html,
                   password_reset_done.html
        '''

        # Get the reset password form and post
        self._password_reset()

        # Check the mail to ensure we get something consistent
        # with the following:
        # password_reset_email.html
        SEARCH_TEXT = 'A password reset was requested for the following account'
        self.assertIn(SEARCH_TEXT, mail.outbox[0].body)

        # Make sure the subject is same as password_reset_subject.txt
        SEARCH_TEXT = 'Password Reset Request'
        self.assertIn(SEARCH_TEXT, mail.outbox[0].subject)

        # Now extract the activation link from the email, eg:
        # http://testserver/accounts/activate/MQ/aj3s3n-59f39d811176d95dc22a0bb4efb8808a/
        sent_email = mail.outbox[0].body
        start = sent_email.find('http:')
        link = sent_email[start:len(sent_email)].strip()

        # Remove the second from last character from the url to
        # make it invalid.
        link_invalid = link[:-2] + link[-1:]

        # Follow the invalid activation link.   It should go to
        # the following:
        # password_reset_form.html (I think)
        response = self.client.get(link_invalid)
        self.assertEqual(response.status_code, 200)
        SEARCH_TEXT = "The password reset link was invalid,"
        self.assertContains(response, SEARCH_TEXT)

from django.test import TestCase, Client
import unittest
from unittest import mock
from django.apps import apps
from apps.paypal_templates.apps import PaypalTemplatesConfig
from apps.paypal_templates import views


class MockResponse:
    def __init__(self, id=None):
        self.id = id

class PPBasicViewsTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_apps(self):
        '''
        Largely for coverage, test login_app config.
        This test for apps was recommended here:
        https://stackoverflow.com/questions/43334953/testing-apps-py-in-django/45613899
        '''
        self.assertEqual(PaypalTemplatesConfig.name, 'paypal_templates')
        self.assertEqual(apps.get_app_config('paypal_templates').name,
                         'apps.paypal_templates')

    def test_sandbox_view_status(self):
        '''
        Sandbox Page
        '''
        response = self.client.get('/paypal_sandbox/')
        self.assertEqual(response.status_code, 200)

    def test_sandbox_view_content(self):
        '''
        Sandbox Page
        '''
        response = self.client.get('/paypal_sandbox/')
        self.assertContains(response, 'Please use the following data')

    def test_very_basic_view_status(self):
        '''
        Very Basic Page
        '''
        response = self.client.get('/paypal_verybasic/')
        self.assertEqual(response.status_code, 200)

    def test_very_basic_view_content(self):
        '''
        Very Basic Page
        '''
        response = self.client.get('/paypal_verybasic/')
        self.assertContains(response, 'smart-button-container')

    def test_success_view_status(self):
        '''
        Success Page
        '''
        response = self.client.get('/paypal_success/')
        self.assertEqual(response.status_code, 200)

    def test_success_view_content(self):
        '''
        Success Page
        '''
        response = self.client.get('/paypal_success/')
        self.assertContains(response, 'Your payment has been successful')

    """
    def test_success_status(self):
        '''
        success page
        '''
        response = self.client.get('/stripe_success/')
        self.assertEqual(response.status_code, 200)

    def test_success_content(self):
        '''
        success page
        '''
        response = self.client.get('/stripe_success/')
        self.assertContains(response, 'We appreciate your business!')

    def test_cancel_status(self):
        '''
        cancel page
        '''
        response = self.client.get('/stripe_cancel/')
        self.assertEqual(response.status_code, 200)

    def test_cancel_content(self):
        '''
        cancel page
        '''
        response = self.client.get('/stripe_cancel/')
        self.assertContains(response, 'Your payment was cancelled.')

    def test_basic_status(self):
        '''
        basic page
        '''
        response = self.client.get('/stripe_basic/')
        self.assertEqual(response.status_code, 200)

    def test_basic_content(self):
        '''
        basic page
        '''
        response = self.client.get('/stripe_basic/')
        self.assertContains(response, 'This is the checkout button!')

class SingleCheckoutJSInterfacesTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_checkout_session(self):
        '''
        Checkout Session
        '''
        with mock.patch("apps.stripe_checkout_single.views.stripe.checkout.Session.create") as gt:
            lst = []
            gt.return_value = MockResponse(101010)
            response = self.client.get('/stripe_create_checkout_session/')
            jdata = response.json()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(jdata['id'], 101010)

class SingleCheckoutWebhookTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_checkout_session_valerr(self):
        '''
        Webhook - check response from get
        '''

        c = Client(HTTP_STRIPE_SIGNATURE='blah')

        with mock.patch("apps.stripe_checkout_subscription.views.stripe.Webhook.construct_event") as ge:

            # The code that this tests is taken from stripe and would need
            # modification for a production environment!!!

            ge.side_effect = ValueError("Error has occurred")

            # Get the data and convert it to json
            response = c.post(path='/webhook/',
                            data={'body':'hi'},
                            content_type='application/json'
                            )
            self.assertEqual(response.status_code, 400)

    def test_checkout_session_sigerr(self):
        '''
        Webhook - check response from get
        '''

        c = Client(HTTP_STRIPE_SIGNATURE='blah')

        with mock.patch("apps.stripe_checkout_subscription.views.stripe.Webhook.construct_event") as ge:

            # The code that this tests is taken from stripe and would need
            # modification for a production environment!!!

            ge.side_effect = SignatureVerificationError(message="Error has occurred", sig_header="")

            # Get the data and convert it to json
            response = c.post(path='/webhook/',
                            data={'body':'hi'},
                            content_type='application/json'
                            )
            self.assertEqual(response.status_code, 400)

    def test_checkout_session(self):
        '''
        Webhook - check response from get
        '''

        c = Client(HTTP_STRIPE_SIGNATURE='blah')

        with mock.patch("apps.stripe_checkout_subscription.views.stripe.Webhook.construct_event") as ge:

            # The code that this tests is taken from stripe and would need
            # modification for a production environment!!!

            ge.return_value = {'type': 'checkout.session.completed', 'data':{'object': 'blah'}}

            # Get the data and convert it to json
            response = c.post(path='/webhook/',
                            data={'body':'hi'},
                            content_type='application/json'
                            )
            self.assertEqual(response.status_code, 200)

    def test_checkout_session_badtype(self):
        '''
        Webhook - check response from get
        '''

        c = Client(HTTP_STRIPE_SIGNATURE='blah')

        with mock.patch("apps.stripe_checkout_subscription.views.stripe.Webhook.construct_event") as ge:

            # The code that this tests is taken from stripe and would need
            # modification for a production environment!!!

            ge.return_value = {'type': 'blah', 'data':{'object': 'blah'}}

            # Get the data and convert it to json
            response = c.post(path='/webhook/',
                            data={'body':'hi'},
                            content_type='application/json'
                            )
            self.assertEqual(response.status_code, 200)
    
    """
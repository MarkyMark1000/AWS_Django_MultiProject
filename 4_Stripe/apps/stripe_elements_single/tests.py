from django.test import TestCase, Client
import unittest
from unittest import mock
from django.apps import apps
from apps.stripe_elements_single.apps import StripeElementsSingleConfig
from apps.stripe_elements_single import views
from apps.stripe_elements_single.hidden_account import STRIPE_PUBLIC_KEY

class MockResponse:
    def __init__(self, id=None):
        self.id = id

class SingleElementsTest(TestCase):

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
        self.assertEqual(StripeElementsSingleConfig.name, 'stripe_elements_single')
        self.assertEqual(apps.get_app_config('stripe_elements_single').name,
                         'apps.stripe_elements_single')

    def test_checkout_status(self):
        '''
        Checkout Page
        '''
        response = self.client.get('/stripe_elements_checkout/')
        self.assertEqual(response.status_code, 200)

    def test_checkout_content(self):
        '''
        Checkout Page
        '''
        response = self.client.get('/stripe_elements_checkout/')
        self.assertContains(response, 'class="pagesection text-center')

    def test_checkout_status2(self):
        '''
        Checkout2 Page
        '''
        response = self.client.get('/stripe_elements_checkout2/')
        self.assertEqual(response.status_code, 200)

    def test_checkout_content2(self):
        '''
        Checkout2 Page
        '''
        response = self.client.get('/stripe_elements_checkout2/')
        self.assertContains(response, '<input id="example3-name"')

class SubElementsJSInterfacesTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_setup_intent_get(self):
        '''
        Setup Intent - check response from get
        '''

        # Get the data and convert it to json
        response = self.client.get('/stripe_elements_create_payment_intent/')
        self.assertEqual(response.status_code, 404)

    def test_setup_intent_post(self):
        '''
        Setup Intent - check response from post
        '''

        # Get payment intent from server
        # WARNING data IS NOT CURRENTLY USED BY THE SERVER
        response = self.client.post('/stripe_elements_create_payment_intent/',
                                    data={'id': 'photo-subscription'},
                                    content_type='application/json')

        # Should return 200 code
        self.assertEqual(response.status_code, 200)

        # Should contain publishableKey and clientSecret
        jdata = response.json()
        self.assertEqual(jdata['publishableKey'], STRIPE_PUBLIC_KEY)

    def test_setup_intent_error(self):
        '''
        Setup Intent - check response from error
        '''
        with mock.patch("apps.stripe_elements_single.views.stripe.PaymentIntent.create") as gt:
            
            gt.side_effect = Exception("An Error")

            response = self.client.post('/stripe_elements_create_payment_intent/',
                                    data={'id': 'photo-subscription'},
                                    content_type='application/json')

            self.assertEqual(response.status_code, 403)
            jdata = response.json()
            self.assertEqual(jdata['error'],'An Error')

class SubCheckoutWebhookTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_webhook_get(self):
        '''
        Webhook - check response from get
        '''

        # Get the data and convert it to json
        response = self.client.get('/stripe_elements_webhook/')
        self.assertEqual(response.status_code, 404)
    
    def test_webhook_except(self):
        '''
        Webhook - check response from get
        '''

        c = Client(HTTP_STRIPE_SIGNATURE='blah')

        with mock.patch("apps.stripe_elements_single.views.stripe.Webhook.construct_event") as ge:

            ge.side_effect = Exception("Error has occurred")
            # Get the data and convert it to json
            response = c.post(path='/stripe_elements_webhook/',
                            data={'body':'hi'},
                            content_type='application/json'
                            )
            self.assertEqual(response.status_code, 500)
            jdata = response.json()
            self.assertEqual(jdata['error'],'Error has occurred')

    def test_webhook(self):
        '''
        Webhook - check response from get
        '''

        c = Client(HTTP_STRIPE_SIGNATURE='blah')

        test_types=('payment_intent.succeeded', 'payment_intent.payment_failed')

        with mock.patch("apps.stripe_checkout_subscription.views.stripe.Webhook.construct_event") as ge:

            for t in test_types:

                # The code that this tests is taken from stripe and would need
                # modification for a production environment!!!

                # print('test_type:', t)
                ge.return_value = {'type': t, 'data': {'object': 'blah'}}

                # Get the data and convert it to json
                response = c.post(path='/stripe_elements_webhook/',
                                data={'body':'hi'},
                                content_type='application/json'
                                )
                self.assertEqual(response.status_code, 200)
                jdata = response.json()
                self.assertEqual(jdata['status'],'success')

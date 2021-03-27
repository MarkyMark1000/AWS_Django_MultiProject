from django.test import TestCase, Client
import unittest
from unittest import mock
from django.apps import apps
from apps.stripe_checkout_subscription.apps import StripeCheckoutSubscriptionConfig
from apps.stripe_checkout_subscription.hidden_account import STRIPE_PUBLIC_KEY

class MockResponse:
    def __init__(self, customer=None, url=None):
        self.customer = customer
        self.url = url


class SubCheckoutBasicViewsTest(TestCase):

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
        self.assertEqual(StripeCheckoutSubscriptionConfig.name, 'stripe_checkout_subscription')
        self.assertEqual(apps.get_app_config('stripe_checkout_subscription').name,
                         'apps.stripe_checkout_subscription')

    def test_basic_sub_status(self):
        '''
        Basic Sub Page
        '''
        response = self.client.get('/stripe_basic_sub/')
        self.assertEqual(response.status_code, 200)

    def test_basic_sub_content(self):
        '''
        Basic Sub Page
        '''
        response = self.client.get('/stripe_basic_sub/')
        self.assertContains(response, 'Choose a collaboration plan')

    def test_cancel_status(self):
        '''
        Cancel Page
        '''
        response = self.client.get('/stripe_sub_cancel/')
        self.assertEqual(response.status_code, 200)

    def test_cancel_content(self):
        '''
        Cancel Page
        '''
        response = self.client.get('/stripe_sub_cancel/')
        self.assertContains(response, 'Your subscription was cancelled.')

    def test_finished_bill_status(self):
        '''
        Finished Billing Page
        '''
        response = self.client.get('/stripe_sub_finished_billing/')
        self.assertEqual(response.status_code, 200)

    def test_finished_bill_content(self):
        '''
        Finished Billing Page
        '''
        response = self.client.get('/stripe_sub_finished_billing/')
        self.assertContains(response, 'This is the account view, after the customer')

    def test_privacy_status(self):
        '''
        Privacy Page
        '''
        response = self.client.get('/privacy/')
        self.assertEqual(response.status_code, 200)

    def test_privacy_content(self):
        '''
        Privacy Page
        '''
        response = self.client.get('/privacy/')
        self.assertContains(response, 'This is the privacy view!!!')

    def test_terms_status(self):
        '''
        Terms and Conditions Page
        '''
        response = self.client.get('/terms/')
        self.assertEqual(response.status_code, 200)

    def test_terms_content(self):
        '''
        Terms and Conditions Page
        '''
        response = self.client.get('/terms/')
        self.assertContains(response, 'This is the terms view!!!')

    def test_success_status(self):
        '''
        Success Page
        '''
        response = self.client.get('/stripe_sub_success/')
        self.assertEqual(response.status_code, 200)

    def test_success_content(self):
        '''
        Success Page
        '''
        response = self.client.get('/stripe_sub_success/')
        self.assertContains(response, 'Your subscription was successful')

class SubCheckoutJSInterfacesTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_setup_session_post(self):
        '''
        Setup Session - check response from post
        '''

        # Get the data and convert it to json
        response = self.client.post('/stripe_sub_setup/')
        self.assertEqual(response.status_code, 404)

    def test_setup_session(self):
        '''
        Setup Session
        If anything was going to change and cause a problem, changing
        the publishable key or the prices might do it, so I have them
        hard-coded here for testing purposes.
        '''

        # Get the data and convert it to json
        response = self.client.get('/stripe_sub_setup/')
        jdata = response.json()

        # Ensure the status is sensile and the size of the data is 3
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(jdata.keys()),3)

        # Check the values in the data
        self.assertEqual(jdata['publishableKey'],
                         'pk_test_51IWiboLnm61uJv5fKfrUVjLEGRLJ8QEP7GkgnOVcIzBrDNhweMpUSD4SIyJxcrW3jGXgVElPiVP5Cj0wu37H4dDr00QSJSRfa5')
        self.assertEqual(jdata['basicPrice'], 'price_1IXkXPLnm61uJv5f8369c8Wl')
        self.assertEqual(jdata['proPrice'], 'price_1IXkYoLnm61uJv5fvwF7oxzM')

    def test_checkout_session_get(self):
        '''
        Checkout Session - check response from get
        '''

        # Get the data and convert it to json
        response = self.client.get('/stripe_sub_create_checkout_session/')
        self.assertEqual(response.status_code, 404)

    def test_checkout_session_error(self):
        '''
        Checkout Session - check response from post
        '''
        with mock.patch("apps.stripe_checkout_subscription.views.stripe.checkout.Session.create") as gt:
            gt.side_effect = Exception("An Error")
            response = self.client.post('/stripe_sub_create_checkout_session/',
                                        data={'priceId': '101010'},
                                        content_type='application/json')
            self.assertEqual(response.status_code, 400)
            jdata = response.json()
            self.assertEqual(jdata['error']['message'],'An Error')

    def test_checkout_session(self):
        '''
        Checkout Session - check response from post
        '''
        with mock.patch("apps.stripe_checkout_subscription.views.stripe.checkout.Session.create") as gt:
            gt.return_value = {'id': '998877'}
            response = self.client.post('/stripe_sub_create_checkout_session/',
                                        data={'priceId': '101010'},
                                        content_type='application/json')
            self.assertEqual(response.status_code, 200)
            jdata = response.json()
            self.assertEqual(jdata['sessionId'], '998877')

class SubCheckoutSuccessJSInterfacesTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_checkout_session_post(self):
        '''
        Checkout Session - check response from post
        '''

        # Get the data and convert it to json
        response = self.client.post('/stripe_sub_checkout_session/')
        self.assertEqual(response.status_code, 404)

    def test_checkout_session(self):
        '''
        Checkout Session
        '''
        with mock.patch("apps.stripe_checkout_subscription.views.stripe.checkout.Session.retrieve") as gt:
            
            gt.return_value = {'ret': 'hi'}

            # Get the data and convert it to json
            response = self.client.get('/stripe_sub_checkout_session/12345/')

            self.assertEqual(response.status_code, 200)
            jdata  = response.json()
            self.assertEqual(jdata['ret'], 'hi')

    def test_customer_portal_get(self):
        '''
        Checkout Cust Portal - check response from get
        '''

        # Get the data and convert it to json
        response = self.client.get('/stripe_sub_customer_portal/')
        self.assertEqual(response.status_code, 404)

    def test_customer_portal(self):
        '''
        Checkout Cust Portal - check response from get
        '''

        with mock.patch("apps.stripe_checkout_subscription.views.stripe.checkout.Session.retrieve") as gt:
            
            gt.return_value = MockResponse(customer='johndoe')

            with mock.patch("apps.stripe_checkout_subscription.views.stripe.billing_portal.Session.create") as ge:

                ge.return_value = MockResponse(url="http://www.bbc.co.uk")

                # Get the data and convert it to json
                response = self.client.post('/stripe_sub_customer_portal/',
                                            data={'sessionId': '101010'},
                                            content_type='application/json')

                self.assertEqual(response.status_code, 200)
                jdata = response.json()
                self.assertEqual(jdata['url'],'http://www.bbc.co.uk')

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
        response = self.client.get('/stripe_sub_webhook/')
        self.assertEqual(response.status_code, 404)
    
    def test_webhook_except(self):
        '''
        Webhook - check response from get
        '''

        c = Client(HTTP_STRIPE_SIGNATURE='blah')

        with mock.patch("apps.stripe_checkout_subscription.views.stripe.Webhook.construct_event") as ge:

            ge.side_effect = Exception("Error has occurred")
            # Get the data and convert it to json
            response = c.post(path='/stripe_sub_webhook/',
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

        test_types=('checkout.session.completed', 'invoice.paid',
                    'invoice.payment_succeeded', 'invoice.payment_failed',
                    'customer.subscription.updated', 'customer.subscription.deleted',
                    'untested')

        with mock.patch("apps.stripe_checkout_subscription.views.stripe.Webhook.construct_event") as ge:

            for t in test_types:

                # The code that this tests is taken from stripe and would need
                # modification for a production environment!!!

                # print('test_type:', t)
                ge.return_value = {'type': t, 'data': {'object': 'blah'}}

                # Get the data and convert it to json
                response = c.post(path='/stripe_sub_webhook/',
                                data={'body':'hi'},
                                content_type='application/json'
                                )
                self.assertEqual(response.status_code, 200)
                jdata = response.json()
                self.assertEqual(jdata['status'],'success')


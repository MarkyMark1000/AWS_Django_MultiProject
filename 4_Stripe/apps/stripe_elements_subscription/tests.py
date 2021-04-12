from django.test import TestCase, Client
import unittest
from unittest import mock
from django.apps import apps
from apps.stripe_elements_subscription.apps import StripeElementsSubscriptionConfig
from apps.stripe_elements_subscription import views
import stripe
import json
from apps.stripe_elements_subscription.hidden_account import STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY, \
                           STRIPE_WEBHOOK_SECRET

class MockResponse:
    def __init__(self, id=None):
        self.id = id

class SubscriptionElementsTest(TestCase):

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
        self.assertEqual(StripeElementsSubscriptionConfig.name, 'stripe_elements_subscription')
        self.assertEqual(apps.get_app_config('stripe_elements_subscription').name,
                         'apps.stripe_elements_subscription')

    def test_subscription_status(self):
        '''
        Sub Page
        '''
        response = self.client.get('/stripe_elements_sub/')
        self.assertEqual(response.status_code, 200)

    def test_subscription_content(self):
        '''
        Sub Page
        '''
        response = self.client.get('/stripe_elements_sub/')
        self.assertContains(response, 'placeholder="Email address"')

    def test_prices_status(self):
        '''
        Prices Page
        '''
        response = self.client.get('/stripe_elements_prices/')
        self.assertEqual(response.status_code, 200)

    def test_prices_content(self):
        '''
        Prices Page
        '''
        response = self.client.get('/stripe_elements_prices/')
        self.assertContains(response, '<h3>Basic</h3>')

    def test_subscribe_status(self):
        '''
        Subscribe Page
        '''
        response = self.client.get('/stripe_elements/basic/')
        self.assertEqual(response.status_code, 200)

    def test_subscribe_content(self):
        '''
        Subscribe Page
        '''
        response = self.client.get('/stripe_elements/basic/')
        self.assertContains(response, 'id="card-element"')

    def test_account_status(self):
        '''
        Account Page
        '''
        response = self.client.get('/stripe_elements_account/')
        self.assertEqual(response.status_code, 200)

    def test_account_content(self):
        '''
        Account Page
        '''
        response = self.client.get('/stripe_elements_account/')
        self.assertContains(response, '<h3>Account</h3>')

    def test_cancel_status(self):
        '''
        Cancel Page
        '''
        response = self.client.get('/stripe_elements_cancel_subscription/fakesub_id/')
        self.assertEqual(response.status_code, 200)

    def test_cancel_content(self):
        '''
        Cancel Page
        '''
        response = self.client.get('/stripe_elements_cancel_subscription/fakesub_id/')
        self.assertContains(response, 'id="cancel-btn"')

class SubElementsJSInterfacesTest(TestCase):

    def setUp(self):
        
        # Create a customer id that can be used in the tests.   This should
        # create the customer cookie used by other routines.
        response = self.client.post('/stripe_elements_create_customer/',
                                    data={'email': 'test@test.com'},
                                    content_type='application/json')

        # IMPORTANT - INITIATE stripe WITH SECRET KEY
        stripe.api_key = STRIPE_SECRET_KEY

        # Create a paymentMethod for use in the tests
        self.payment_method = \
            stripe.PaymentMethod.create(type="card",
                                        card={
                                        "number": "4242424242424242",
                                        "exp_month": 12,
                                        "exp_year": 2050,
                                        "cvc": "123",
                                        },)

        # Create a subscription for use in the tests - ie cancel
        response = self.client.post('/stripe_elements_create_subscription/',
                                    data={'paymentMethodId': self.payment_method.id,
                                          'priceLookupKey': 'basic'},
                                    content_type='application/json')
        data = json.loads(str(response.content, encoding='utf-8'))
        self.subscription_id = data['subscription']['id']

    def tearDown(self):
        pass

    def test_create_customer_get(self):
        '''
        Create Customer - check response from get
        '''

        # Get the data and convert it to json
        response = self.client.get('/stripe_elements_create_customer/')
        self.assertEqual(response.status_code, 404)

    def test_create_customer_post(self):
        '''
        Create Customer - check response from post
        '''

        response = self.client.post('/stripe_elements_create_customer/',
                                    data={'email': 'name@test.com'},
                                    content_type='application/json')

        # Should return 200 code
        self.assertEqual(response.status_code, 200)

    def test_create_customer_error(self):
        '''
        Create Customer - check response from error
        '''
        with mock.patch("apps.stripe_elements_subscription.views.stripe.Customer.create") as gt:
            
            gt.side_effect = Exception("An Error")

            response = self.client.post('/stripe_elements_create_customer/',
                                    data={'email': 'name@test.com'},
                                    content_type='application/json')

            self.assertEqual(response.status_code, 403)
            jdata = response.json()
            self.assertEqual(jdata['error'],'An Error')

    def test_create_subscription_get(self):
        '''
        Create Subscription - check response from get
        '''

        # Get the data and convert it to json
        response = self.client.get('/stripe_elements_create_subscription/')
        self.assertEqual(response.status_code, 404)

    def test_create_subscription_basic_post(self):
        '''
        Create Subscription - check response from post
        '''

        response = self.client.post('/stripe_elements_create_subscription/',
                                    data={'paymentMethodId': self.payment_method.id,
                                          'priceLookupKey': 'basic'},
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)

    def test_create_subscription_premium_post(self):
        '''
        Create Subscription - check response from post
        '''

        response = self.client.post('/stripe_elements_create_subscription/',
                                    data={'paymentMethodId': self.payment_method.id,
                                          'priceLookupKey': 'premium'},
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)

    def test_create_subscription_error(self):
        '''
        Create Subscription - check response from error
        '''
        with mock.patch("apps.stripe_elements_subscription.views.stripe.PaymentMethod.attach") as gt:
            
            gt.side_effect = Exception("An Error")

            response = self.client.post('/stripe_elements_create_subscription/',
                                        data={'paymentMethodId': self.payment_method.id,
                                            'priceLookupKey': 'basic'},
                                        content_type='application/json')

            self.assertEqual(response.status_code, 400)
            jdata = response.json()
            self.assertEqual(jdata['error'],'An Error')

    def test_list_subscription_post(self):
        '''
        List Subscription - check response from post
        '''

        # Get the data and convert it to json
        response = self.client.post('/stripe_elements_list_subscriptions/',
                                    data={'blah': 'blah'},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_list_subscription_basic_get(self):
        '''
        List Subscription - check response from get
        '''

        response = self.client.get('/stripe_elements_list_subscriptions/')
        
        self.assertEqual(response.status_code, 200)

    def test_list_subscription_basic_error(self):
        '''
        List Customer - check response from error
        '''
        with mock.patch("apps.stripe_elements_subscription.views.stripe.Subscription.list") as gt:
            
            gt.side_effect = Exception("An Error")

            response = self.client.get('/stripe_elements_list_subscriptions/')

            self.assertEqual(response.status_code, 403)
            jdata = response.json()
            self.assertEqual(jdata['error'],'An Error')

    def test_cancel_subscription_get(self):
        '''
        Cancel Subscription - check response from get
        '''

        # Get the data and convert it to json
        response = self.client.get('/stripe_elements_cancel_subscription/')
        self.assertEqual(response.status_code, 404)

    def test_cancel_subscription_post(self):
        '''
        Cancel Subscription - check response from post
        '''

        response = self.client.post('/stripe_elements_cancel_subscription/',
                                    data={'subscriptionId': self.subscription_id},
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)

    def test_cancel_subscription_error(self):
        '''
        Cancel Subscription - check response from error
        '''
        with mock.patch("apps.stripe_elements_subscription.views.stripe.Subscription.delete") as gt:
            
            gt.side_effect = Exception("An Error")

            response = self.client.post('/stripe_elements_cancel_subscription/',
                                    data={'subscriptionId': self.subscription_id},
                                    content_type='application/json')

            self.assertEqual(response.status_code, 403)
            jdata = response.json()
            self.assertEqual(jdata['error'],'An Error')

class SubElementsWebhookTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_webhook_get(self):
        '''
        Webhook - check response from get
        '''

        # Get the data and convert it to json
        response = self.client.get('/stripe_elements_sub_webhook/')
        self.assertEqual(response.status_code, 404)
    
    def test_webhook_except(self):
        '''
        Webhook - check response from get
        '''

        c = Client(HTTP_STRIPE_SIGNATURE='blah')

        with mock.patch("apps.stripe_elements_single.views.stripe.Webhook.construct_event") as ge:

            ge.side_effect = Exception("Error has occurred")
            # Get the data and convert it to json
            response = c.post(path='/stripe_elements_sub_webhook/',
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

        test_types=('invoice.paid', 'invoice.payment_failed', 'customer.subscription.deleted')

        with mock.patch("apps.stripe_checkout_subscription.views.stripe.Webhook.construct_event") as ge:

            for t in test_types:

                # The code that this tests is taken from stripe and would need
                # modification for a production environment!!!

                # print('test_type:', t)
                ge.return_value = {'type': t, 'data': {'object': 'blah'}}

                # Get the data and convert it to json
                response = c.post(path='/stripe_elements_sub_webhook/',
                                data={'body':'hi'},
                                content_type='application/json'
                                )
                self.assertEqual(response.status_code, 200)
                jdata = response.json()
                self.assertEqual(jdata['status'],'success')

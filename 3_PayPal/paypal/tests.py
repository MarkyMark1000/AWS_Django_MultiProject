from django.test import TestCase, RequestFactory
import unittest
from unittest import mock
import paypal.extra_code_or_config.getIP as GI

class MockResponse:
    def __init__(self, text):
        self.text = text


class AWSTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_getIP(self):
        with mock.patch("paypal.extra_code_or_config.getIP.requests.get") as gt:
            lst = []
            gt.return_value = MockResponse('99.98.97.96')
            GI.appendIPToArray(lst)
            self.assertIn('99.98.97.96', lst)

    def test_getIP_adds_once(self):
        with mock.patch("paypal.extra_code_or_config.getIP.requests.get") as gt:
            lst = ['99.98.97.96']
            gt.return_value = MockResponse('99.98.97.96')
            GI.appendIPToArray(lst)
            self.assertEqual(len(lst), 1)

    def test_getFalseIP(self):
        with mock.patch("paypal.extra_code_or_config.getIP.requests.get") as gt:
            lst = []
            gt.return_value = MockResponse(False)
            self.assertEqual(GI.appendIPToArray(lst), False)

class PayPalBasicViewsTest(TestCase):

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
        Basic Sub Page
        '''
        response = self.client.get('/')
        self.assertContains(response, 'This is a description of this project')

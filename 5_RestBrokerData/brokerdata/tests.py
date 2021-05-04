from rest_framework.test import APITestCase
import unittest
from unittest import mock
import brokerdata.extra_code_or_config.getIP as GI

class MockResponse:
    def __init__(self, text):
        self.text = text

class MainTest(APITestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_getIP(self):
        with mock.patch("brokerdata.extra_code_or_config.getIP.requests.get") as gt:
            lst = []
            gt.return_value = MockResponse('99.98.97.96')
            GI.appendIPToArray(lst)
            self.assertIn('99.98.97.96', lst)

    def test_getIP_adds_once(self):
        with mock.patch("brokerdata.extra_code_or_config.getIP.requests.get") as gt:
            lst = ['99.98.97.96']
            gt.return_value = MockResponse('99.98.97.96')
            GI.appendIPToArray(lst)
            self.assertEqual(len(lst), 1)

    def test_getFalseIP(self):
        with mock.patch("brokerdata.extra_code_or_config.getIP.requests.get") as gt:
            lst = []
            gt.return_value = MockResponse(False)
            self.assertEqual(GI.appendIPToArray(lst), False)
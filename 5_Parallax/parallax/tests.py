from django.test import TestCase, RequestFactory
import unittest
from unittest import mock
import parallax.extra_code_or_config.getIP as GI

class MockResponse:
    def __init__(self, text):
        self.text = text


class AWSTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_getIP(self):
        with mock.patch("parallax.extra_code_or_config.getIP.requests.get") as gt:
            lst = []
            gt.return_value = MockResponse('99.98.97.96')
            GI.appendIPToArray(lst)
            self.assertIn('99.98.97.96', lst)

    def test_getIP_adds_once(self):
        with mock.patch("parallax.extra_code_or_config.getIP.requests.get") as gt:
            lst = ['99.98.97.96']
            gt.return_value = MockResponse('99.98.97.96')
            GI.appendIPToArray(lst)
            self.assertEqual(len(lst), 1)

    def test_getFalseIP(self):
        with mock.patch("parallax.extra_code_or_config.getIP.requests.get") as gt:
            lst = []
            gt.return_value = MockResponse(False)
            self.assertEqual(GI.appendIPToArray(lst), False)

class GetIPTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_getIP(self):
        with mock.patch("parallax.extra_code_or_config.getIP.socket.socket.connect") as gt:
            gt.side_effect = Exception("Error occurred")
            result = GI.get_ip()
            self.assertEqual('127.0.0.1', result)

class ParallaxTest(TestCase):

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
        SEARCH_TEXT = 'THIS DOES NOT WORK WHEN VIEWED ON IPHONE'
        response = self.client.get('/')
        self.assertContains(response, SEARCH_TEXT)

    def test_page2_status(self):
        '''
        Check page2 returns status 200
        '''
        response = self.client.get('/page2/')
        self.assertEqual(response.status_code, 200)

    def test_page2_content(self):
        '''
        Check page2 contains the desired text
        '''
        response = self.client.get('/page2/')
        SEARCH_TEXT = 'This is the back layer'
        self.assertContains(response, SEARCH_TEXT)
        SEARCH_TEXT = 'This is the base layer'
        self.assertContains(response, SEARCH_TEXT)

    def test_page3_status(self):
        '''
        Check page3 returns status 200
        '''
        response = self.client.get('/page3/')
        self.assertEqual(response.status_code, 200)

    def test_page3_content(self):
        '''
        Check page3 contains the desired text
        '''
        response = self.client.get('/page3/')
        SEARCH_TEXT = 'This does work on an iPhone'
        self.assertContains(response, SEARCH_TEXT)

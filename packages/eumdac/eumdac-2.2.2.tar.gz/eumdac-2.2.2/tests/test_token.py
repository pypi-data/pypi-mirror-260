import unittest
import time
from datetime import datetime

from eumdac.token import AccessToken
from .base import DataServiceTestCase, INTEGRATION_TESTING

import requests


class TestAccessToken(DataServiceTestCase):
    def setUp(self):
        super().setUp()
        self.token = AccessToken(self.credentials)

    def test_str_representation(self):
        self.assertEqual(str(self.token), self.token.access_token)

    def test_cache(self):
        token_url = self.token.urls.get("token", "token")
        # check lazy loading
        self.requests_mock.assert_call_count(token_url, 0)
        str(self.token)
        self.requests_mock.assert_call_count(token_url, 1)
        # increase the request margin to enforce re-requesting
        self.token.request_margin = 10000
        str(self.token)
        self.requests_mock.assert_call_count(token_url, 2)

    def test_properties(self):
        now = datetime.now()
        access_token = self.token.access_token
        expiration = self.token.expiration
        self.assertIsInstance(access_token, str)
        self.assertIsInstance(expiration, datetime)
        self.assertLessEqual(now, self.token.expiration)

    @unittest.skipIf(INTEGRATION_TESTING, "Check against changing value!")
    def test_auth(self):
        mock_token = "1f29ecb3-5973-35d5-a7e6-ec3348c9c49a"
        self.token._access_token = mock_token
        self.token._expiration = time.time() + 1000
        request = requests.Request("GET", "some-url")
        self.token.auth(request)
        auth_header = request.headers.get("authorization")
        self.assertEqual(auth_header, f"Bearer {mock_token}")

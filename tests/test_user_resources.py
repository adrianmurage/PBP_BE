import json
import unittest

import app


class RegularUserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.app
        self.client = self.app.test_client()
        self.regular_user = {
            "username": "test_user1",
            "password": "test_user1"
        }

    def test_regular_user_registration(self):
        resp = self.client.post(
            '/api/register',
            content_type='application/json',
            data=json.dumps(self.regular_user))
        print(resp.data)
        self.assertEqual(resp.status_code, 201)

    def test_regular_user_login(self):
        resp = self.client.post(
            '/api/login',
            content_type='application/json',
            data=json.dumps({
                "username": "test_user",
                "password": "test_user"
            })
        )
        print(resp.data)
        self.assertEqual(resp.status_code, 200)


class VendorTestCAse(unittest.TestCase):
    def setUp(self):
        self.app = app.app
        self.client = self.app.test_client()
        self.vendor = {
            "username": "test_vendor",
            "password": "test_vendor"
        }

    def test_vendor_registration(self):
        resp = self.client.post(
            '/api/vendor/register',
            content_type='application/json',
            data=json.dumps(self.vendor))
        print(resp.data)
        self.assertEqual(resp.status_code, 201)

    def test_vendor_login(self):
        resp = self.client.post(
            '/api/vendor/login',
            content_type='application/json',
            data=json.dumps({
                "username": "vendor1",
                "password": "vendor1"
            })
        )
        print(resp.data)
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()


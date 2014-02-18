import unittest

from koemei.base_client import BaseClient


class BaseClientTestCase(unittest.TestCase):

    def setUp(self):
        self.client = BaseClient()

    def tearDown(self):
        self.client = None

    def test_config(self):
        if not hasattr(self.client, "username") or self.client.username is None:
            self.fail("username not set")
        if not hasattr(self.client, "password") or self.client.password is None:
            self.fail("password not set")
        if not hasattr(self.client, "base_path") or self.client.base_path is None:
            self.fail("base path not set")

if __name__ == "__main__":
    unittest.main()
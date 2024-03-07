import unittest
from onvo import Onvo


class TestAccounts(unittest.TestCase):

    def assertShouldRaise(self, expected_exception, callable):
        if expected_exception is None:
            try:
                callable()
            except Exception as error:
                self.fail(f"Error should not have occurred: {error}")
        else:
            self.assertRaises(expected_exception, callable)

    def setup(self):
        self.onvoSDK = Onvo()

    def test_get(self):
        self.assertShouldRaise(None, self.onvoSDK.accounts.get)

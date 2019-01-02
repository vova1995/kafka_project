"""
    Module for unitests
"""
import unittest
from api.app import APP


class TestStringMethods(unittest.TestCase):
    """
    Unitests for consumer class
    """

    def test_router_offset(self):
        request, response = APP.test_client.get('/consumer_offset')
        self.assertEqual(response.status, 200)

    def test_router_rows(self):
        request, response = APP.test_client.get('/consumer_rows')
        self.assertEqual(response.status, 200)

    def test_router_not_found(self):
        request, response = APP.test_client.get('/consumer_rows_error')
        self.assertEqual(response.status, 404)

    def test_router_method_not_allowed(self):
        request, response = APP.test_client.post('/consumer_rows')
        self.assertEqual(response.status, 405)


if __name__ == '__main__':
    unittest.main()
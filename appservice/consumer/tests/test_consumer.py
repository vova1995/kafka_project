import unittest
# from common.redis import RedisDatabaseManager
# from common.zookeeper import ZookeeperDatabaseManager
import sys


class TestStringMethods(unittest.TestCase):
    #
    def test_router_offset(self):
        from consumer.api.app import APP

        request, response = APP.test_client.get('/consumer_offset')
        self.assertEqual(response.status, 200)

    def test_router_rows(self):
        from consumer.api.app import APP

        request, response = APP.test_client.get('/consumer_rows')
        self.assertEqual(response.status, 200)

import unittest
import asyncio
from api.app import APP
from common.zookeeper import ZookeeperDatabaseManager
from common.redis import RedisDatabaseManager



class TestStringMethods(unittest.TestCase):


    # def setUp(self):
    ioloop = asyncio.get_event_loop()

    # def tearDown(self):
    #     pass

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

    def test_set_value(self):
        test_value = 12

        self.ioloop.run_until_complete(RedisDatabaseManager.set('test', test_value))
        self.assertEqual(self.ioloop.run_until_complete(RedisDatabaseManager.get('test')), test_value)



if __name__ == '__main__':
    unittest.main()
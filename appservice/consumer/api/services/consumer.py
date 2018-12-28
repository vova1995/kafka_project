"""
    Module for consumer service
"""
import asyncio
import json
import time
import uuid
from datetime import datetime
from aiokafka import AIOKafkaConsumer

from common.database import PostgresDatabaseManager, CassandraDatabaseManager
from common.redis import RedisDatabaseManager
from common.zookeeper import ZookeeperDatabaseManager
from api.logger_conf import make_logger
from api.config import Configs


LOGGER = make_logger('logs/consumer_log', 'consumer_logs')
TOPIC = 'test_topic'
PARTITION = 0
GROUP = 'test_group'

loop = asyncio.get_event_loop()


class Consumer:
    """
    Consumer that reads messages from kafka
    """

    def __init__(self):
        self.consumer = AIOKafkaConsumer(TOPIC,
                                         group_id=GROUP,
                                         bootstrap_servers=f"{Configs['KAFKA_ADDRESS']}:{Configs['KAFKA_PORT']}",
                                         enable_auto_commit=False,
                                         loop=loop,
                                         value_deserializer=lambda m: json.loads(m.decode('ascii'))
                                         )
        self.counter = 0
        self._uncommitted_messages = 0
        self._last_commit_time = None
        self._commit_task: asyncio.Task = None

    async def connect(self):
        while True:
            try:
                await self.consumer.start()
                LOGGER.info("Connection with Kafka broker successfully established")
                self._commit_task = asyncio.ensure_future(self.commit_every_10_seconds())
                break
            except Exception as e:
                LOGGER.error("Couldn't connect to Kafka broker because of %s, try again in 3 seconds", e)
            await asyncio.sleep(3)

    async def listen(self):
        """
        listener that catches messages
         and either store in db or commit
        :return:
        """
        try:
            await self.connect()
            async for msg in self.consumer:
                LOGGER.info(f'topic: {msg.topic} and value that will be added to database, offset {msg.offset}, value={msg.value}')
                self._uncommitted_messages += 1
                LOGGER.info('Uncommited message = %s', self._uncommitted_messages)
                self.counter += 1
                LOGGER.info('Counter = %s', self.counter)

                if self.counter >= 10:
                    await self.consumer.commit()
                    self._uncommitted_messages = 0
                    self.counter = 0
                    LOGGER.info("Commit every 10 messages")
                await self.write_to_db(id=uuid.uuid4(), topic=str(msg.topic), message=f'key={msg.key}, value={msg.value}', offset=str(msg.offset))
        except Exception as e:
            LOGGER.error('Listener error: ', e)
            self.connect()
        finally:
            await self.consumer.stop()

    async def write_to_db(self, id, topic, message, offset):
        try:
            if Configs['DATA_STORAGE'] == 'POSTGRES':
                await PostgresDatabaseManager.insert(topic,
                                            message)
            if Configs['DATA_STORAGE'] == 'CASSANDRA':
                await CassandraDatabaseManager.insert(id,
                                                topic,
                                                message)
            if Configs['OFFSET_STORAGE'] == 'REDIS':
                await RedisDatabaseManager.set('kafka', offset)
            if Configs['OFFSET_STORAGE'] == 'ZOOKEEPER':
                await ZookeeperDatabaseManager.set('offset', offset)
        except Exception as e:
            LOGGER.error('Databases', e)

    async def commit_every_10_seconds(self):
        """
        Method that commits message very 10 seconds
        :return:
        """
        if self._last_commit_time is None:
            self._last_commit_time = time.time()
        while True:
            passed_time = time.time() - self._last_commit_time
            if passed_time < 10:
                await asyncio.sleep(10 - passed_time)
                if time.time() - self._last_commit_time < 10:
                    continue
            if self.counter > 0:
                await self.consumer.commit()
                LOGGER.info("Every 10 seconds commit")
                self.counter = 0
            self._last_commit_time = time.time()

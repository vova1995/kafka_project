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
from api.app import make_logger
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
    _consumer: AIOKafkaConsumer = None
    _counter: int = 0
    _uncommitted_messages = 0
    _last_commit_time = None
    _commit_task: asyncio.Task = None

    @classmethod
    async def _init(cls):
        cls._consumer = AIOKafkaConsumer(TOPIC,
                                         group_id=GROUP,
                                         bootstrap_servers=f"{Configs['KAFKA_ADDRESS']}:{Configs['KAFKA_PORT']}",
                                         enable_auto_commit=False,
                                         loop=loop,
                                         value_deserializer=lambda m: json.loads(m.decode('ascii')))

        while True:
            try:
                await cls._consumer.start()
                LOGGER.info("Connection with Kafka broker successfully established")
                cls._commit_task = asyncio.ensure_future(cls.commit_every_10_seconds())
                break
            except Exception as e:
                LOGGER.error("Couldn't connect to Kafka broker because of %s, try again in 3 seconds", e)
            await asyncio.sleep(3)

        cls._counter = 0

    @classmethod
    async def listen(cls):
        """
        listener that catches messages
         and either store in db or commit
        :return:
        """
        try:
            await cls._init()
            async for msg in cls._consumer:
                cls._uncommitted_messages += 1
                LOGGER.info('Uncommited message = %s', cls._uncommitted_messages)
                cls._counter += 1
                LOGGER.info('Counter = %s', cls._counter)

                if cls._counter >= 10:
                    await cls._consumer.commit()
                    cls._uncommitted_messages = 0
                    cls._counter = 0
                    LOGGER.info("Commit every 10 messages")
                await cls.write_to_db(id=uuid.uuid4(), topic=str(msg.topic),
                                      message=f'key={msg.key}, value={msg.value}', offset=str(msg.offset))
        except Exception as e:
            LOGGER.error('Listener error: %s', e)
            cls._init()
        finally:
            await cls._consumer.stop()

    @classmethod
    async def write_to_db(cls, id, topic, message, offset):
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
            LOGGER.error('Databases %s', e)

    @classmethod
    async def commit_every_10_seconds(cls):
        """
        Method that commits message very 10 seconds
        :return:
        """
        # if cls._last_commit_time is None:
        #     cls._last_commit_time = time.time()
        # while True:
        #     passed_time = time.time() - cls._last_commit_time
        #     if passed_time < 10:
        #         await asyncio.sleep(10 - passed_time)
        #         if time.time() - cls._last_commit_time < 10:
        #             continue
        #     if cls._counter > 0:
        #         await cls._consumer.commit()
        #         LOGGER.info("Every 10 seconds commit")
        #         cls._counter = 0
        #     cls._last_commit_time = time.time()
        while True:
            await asyncio.sleep(10)
            if cls._counter > 0:
                cls._consumer.commit()
                LOGGER.info("Every 10 seconds commit")
                cls._counter = 0

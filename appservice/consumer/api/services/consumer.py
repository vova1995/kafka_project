"""
    Module for consumer service
"""
import asyncio
import json
import time
import uuid
from datetime import datetime
from aiokafka import AIOKafkaConsumer
from api.app import LOGGER
from api.config import Configs

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
    _commit_task: asyncio.Task = None

    @classmethod
    async def _init(cls):
        """
        Initialise consumer
        :return:
        """
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
                cls._counter += 1
                LOGGER.info('Counter = %s', cls._counter)

                if cls._counter >= 10:
                    await cls._consumer.commit()
                    cls._counter = 0
                    LOGGER.info("Commit every 10 messages")
                await cls.write_to_db(id=uuid.uuid4(), topic=str(msg.topic),
                                      message=f'key={msg.key}, value={msg.value}', offset=str(msg.offset))
        except Exception as e:
            LOGGER.error('Listener error: %s', e)
            await cls._consumer.start()
        finally:
            await cls._consumer.stop()

    @classmethod
    async def write_to_db(cls, id, topic, message, offset):
        """
        Method writes data into different dbs
        :param id:
        :param topic:
        :param message:
        :param offset:
        :return:
        """
        try:
            from common.database import database

            await database.insert(id, topic, message)

            if Configs['OFFSET_STORAGE'] == 'REDIS':
                from common.redis import RedisDatabaseManager

                await RedisDatabaseManager.set('kafka', offset)
            else:
                from common.zookeeper import ZookeeperDatabaseManager

                await ZookeeperDatabaseManager.set('/offset', offset)
        except Exception as e:
            LOGGER.error('Databases %s', e)

    @classmethod
    async def commit_every_10_seconds(cls):
        """
        Method commits messages every 10 seconds if messages
        :return:
        """
        while True:
            await asyncio.sleep(10)
            if cls._counter > 0:
                cls._consumer.commit()
                LOGGER.info("Every 10 seconds commit")
                cls._counter = 0

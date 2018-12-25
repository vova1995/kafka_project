"""
    Module for consumer service
"""
from aiokafka import AIOKafkaConsumer, TopicPartition
from consumer.models import Messages
import json
from consumer.database import PostgresDatabaseManager, CassandraDatabaseManager, RedisDatabaseManager, \
    CassandraDatabaseManager2, ZookeeperDatabaseManager
from datetime import datetime
import asyncio
import logging
import time

TOPIC = 'test_topic'
PARTITION = 0
GROUP = 'test_group'

loop = asyncio.get_event_loop()

logging.basicConfig(filename='consumer_responses.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Consumer:
    """
    Consumer that reads messages from kafka
    """

    def __init__(self):
        self.consumer = AIOKafkaConsumer(TOPIC,
                                         group_id=GROUP,
                                         bootstrap_servers=['kafka:9092'],
                                         enable_auto_commit=False,
                                         loop=loop,
                                         value_deserializer=lambda m: json.loads(m.decode('ascii'))
                                         )
        self.counter = 0
        self._uncommitted_messages = 0
        self._last_commit_time = None

        # topic_partition = TopicPartition(TOPIC, PARTITION)
        # self.consumer.assign([topic_partition])
        while True:
            try:
                self.consumer.start()
                logging.info("Connection with Kafka broker successfully established")
                self.consumer.commit_task = asyncio.ensure_future(self.commit_every_10_seconds())
                break
            except Exception as e:
                logging.error("Couldn't connect to Kafka broker because of %s, try again in 3 seconds", e)
                asyncio.sleep(3)

    async def listener(self):
        """
        listener that catches messages
         and either store in db or commit
        :return:
        """
        try:
            await self.consumer.start()

            async for msg in self.consumer:
                logging.info(f'topic: {msg.topic} and value added to database, offset {msg.offset}, value={msg.value}')
                self._uncommitted_messages += 1
                logging.info('Uncommited message = %s', self._uncommitted_messages)
                self.counter += 1
                logging.info('Counter = %s', self.counter)

                if self.counter >= 10:
                    self.consumer.commit()
                    self._uncommitted_messages = 0
                    self.counter = 0
                    logging.info("Commit every 10 messages")

                message = Messages(topic=msg.topic,
                                   message=f'key={msg.key}, value={msg.value}')
                PostgresDatabaseManager.session_commit(message)

                CassandraDatabaseManager.cassandra_query_insert(id=str(datetime.utcnow()),
                                                                topic=msg.topic,
                                                                message=f'key={msg.key}, value={msg.value}')
                RedisDatabaseManager.redisset(msg.offset)

                CassandraDatabaseManager2.insert_data(topic=str(msg.topic),
                                                      message=f'key={msg.key}, value={msg.value}')
                ZookeeperDatabaseManager.setdata(msg.offset)
        finally:
            await self.consumer.stop()

    # async def commit_10_seconds(self):
    #     """
    #     function that commits
    #     messages every 10 sec
    #     :return:
    #     """
    #     while True:
    #         await asyncio.sleep(10)
    #         self.consumer.commit()
    #         logging.info('message was committed')

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
                logging.info("Every 10 seconds commit")
                self.counter = 0
            self._last_commit_time = time.time()

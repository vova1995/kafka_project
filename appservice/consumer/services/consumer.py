"""
    Module for consumer service
"""
from aiokafka import AIOKafkaConsumer, TopicPartition
from consumer import ZK
from consumer.models import Messages
import json
from consumer.database import PostgresDatabaseManager, CassandraDatabaseManager, RedisDatabaseManager, \
    CassandraDatabaseManager2, ZookeeperDatabaseManager
from datetime import datetime
import asyncio
import logging

TOPIC = 'test_topic'
PARTITION = 0
GROUP = 'test_group'

loop = asyncio.get_event_loop()

logging.basicConfig(filename='consumer_logs.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class Consumer:
    """
    Consumer that reads messages from kafka
    """

    def __init__(self):
        self.consumer = AIOKafkaConsumer(TOPIC,
                                         group_id=TOPIC,
                                         bootstrap_servers=['kafka:9092'],
                                         enable_auto_commit=False,
                                         loop=loop,
                                         value_deserializer=lambda m: json.loads(m.decode('ascii'))
                                         )

        self.counter = 0

        # topic_partition = TopicPartition(TOPIC, PARTITION)
        # self.consumer.assign([topic_partition])

    async def listener(self):
        """
        listener that catches messages
         and either store in db or commit
        :return:
        """
        # counter = 0
        try:
            await self.consumer.start()
            logging.critical("started")
            async for msg in self.consumer:
                logging.info("got")

                logging.info(f'topic: {msg.topic} and value added to database, offset {msg.offset}, value={msg.value}')
                self.counter += 1
                if self.counter >= 10:
                    self.consumer.commit()
                    self.counter = 0
                logging.info(self.counter)
                message = Messages(msg.topic, f'key={msg.key}, value={msg.value}')
                PostgresDatabaseManager.session_commit(message)
                await asyncio.sleep(0)
                CassandraDatabaseManager.cassandra_query_insert(str(datetime.utcnow()), msg.topic,
                                                                f'key={msg.key}, value={msg.value}')
                await asyncio.sleep(0)
                RedisDatabaseManager.redisset(msg.offset)
                await asyncio.sleep(0)
                CassandraDatabaseManager2.insert_data(topic=str(msg.topic), message=f'key={msg.key}, value={msg.value}')
                await asyncio.sleep(0)
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

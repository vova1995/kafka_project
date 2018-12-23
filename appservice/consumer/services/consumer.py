from kafka import KafkaConsumer, TopicPartition
from consumer import ZK
from consumer.models import Messages, Message
import json
from consumer.database import PostgresDatabaseManager, CassandraDatabaseManager, RedisDatabaseManager, CassandraDatabaseManager2
from datetime import datetime
import asyncio
import logging

TOPIC = 'test_topic'
PARTITION = 0

logging.basicConfig(filename='consumer_logs.txt' ,level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Consumer:
    """
    Consumer that reads messages from kafka
    """
    def __init__(self):
        self.consumer = KafkaConsumer(group_id=TOPIC,
                                 bootstrap_servers=['kafka:9092'],
                                 enable_auto_commit=False,
                                 value_deserializer=lambda m: json.loads(m.decode('ascii'))
                                 )

        self.counter = 0

        topic_partition = TopicPartition(TOPIC, PARTITION)
        self.consumer.assign([topic_partition])

    async def listener(self):
        """
        listerer that catches messages
         and either store in db or commit
        :return:
        """
        # counter = 0
        for msg in self.consumer:
            logging.info(f'topic: {msg.topic} and value added to database, offset {msg.offset}, value={msg.value}')
            self.counter += 1
            if self.counter >= 10:
                self.consumer.commit()
                self.counter = 0
            logging.info(self.counter)
            message = Messages(msg.topic, f'key={msg.key}, value={msg.value}')
            PostgresDatabaseManager.session_commit(message)
            await asyncio.sleep(0)
            CassandraDatabaseManager.cassandra_query_insert(str(datetime.utcnow()), msg.topic, f'key={msg.key}, value={msg.value}')
            await asyncio.sleep(0)
            RedisDatabaseManager.redisset(msg.offset)
            await asyncio.sleep(0)
            CassandraDatabaseManager2.insert_data(topic=str(msg.topic), message=f'key={msg.key}, value={msg.value}')
            await asyncio.sleep(0)
            ZK.start()
            ZK.ensure_path("/my/offset")
            ZK.set("/my/offset", bytes(msg.offset))
            ZK.stop()

    async def commit_10_seconds(self):
        """
        function that commits
        messages every 10 sec
        :return:
        """
        while True:
            await asyncio.sleep(10)
            self.consumer.commit()

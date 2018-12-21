from kafka import KafkaConsumer, TopicPartition
from kafka.errors import NoBrokersAvailable
from consumer import REDIS
from consumer.models import Messages
import json
from consumer.database import DatabaseManager
from datetime import datetime
import asyncio

TOPIC = 'test_topic'
PARTITION = 0


class Consumer:
    """
    Consumer that reads messages from kafka
    """
    def __init__(self):
        consumer = KafkaConsumer(group_id=TOPIC,
                                 bootstrap_servers=['kafka:9092'],
                                 enable_auto_commit=False,
                                 value_deserializer=lambda m: json.loads(m.decode('ascii'))
                                 )

        topic_partition = TopicPartition(TOPIC, PARTITION)
        consumer.assign([topic_partition])

        async def listener():
            """
            listerer that catches messages
             and either store in db or commit
            :return:
            """
            counter = 0
            for msg in consumer:
                print(f'topic: {msg.topic} and value added to database, offset {msg.offset}, value={msg.value}')
                counter += 1
                if counter >= 10:
                    consumer.commit()
                    counter = 0
                print(counter)
                message = Messages(msg.topic, f'key={msg.key}, value={msg.value}')
                DatabaseManager.session_commit(message)
                await asyncio.sleep(0)
                DatabaseManager.cassandra_query_insert(str(datetime.utcnow()), msg.topic, f'key={msg.key}, value={msg.value}')
                await asyncio.sleep(0)
                REDIS.set('kafka', msg.offset)
                await asyncio.sleep(0)

        async def commit_10_seconds():
            """
            function that commits
            messages every 10 sec
            :return:
            """
            while True:
                await asyncio.sleep(10)
                consumer.commit()

        ioloop = asyncio.get_event_loop()
        tasks = [
            ioloop.create_task(listener()),
            ioloop.create_task(commit_10_seconds())
        ]
        ioloop.run_until_complete(asyncio.wait(tasks))
        ioloop.close()

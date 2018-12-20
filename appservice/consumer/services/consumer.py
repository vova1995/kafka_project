from kafka import KafkaConsumer, TopicPartition
from consumer import REDIS
from consumer.models import Messages
import json
from consumer.database import DatabaseManager
from datetime import datetime
# import time

TOPIC = 'test_topic'
PARTITION = 0

class Consumer:
    def __init__(self):
        consumer = KafkaConsumer(group_id=TOPIC,
                                 bootstrap_servers=['localhost:9092'],
                                 consumer_timeout_ms=1000000,
                                 enable_auto_commit=False,
                                 value_deserializer=lambda m: json.loads(m.decode('ascii'))
                                 )


        counter = 0

        topic_partition = TopicPartition(TOPIC, PARTITION)
        consumer.assign([topic_partition])

        def commit_every_10_seconds():
            consumer.commit()
            self.counter = 0

        for msg in consumer:
            print(f'topic: {msg.topic} and value added to database, offset {msg.offset}, value={msg.value}')
            counter += 1
            print(counter)
            message = Messages(msg.topic, f'key={msg.key}, value={msg.value}')
            DatabaseManager.session_commit(message)
            DatabaseManager.cassandra_query_insert(str(datetime.utcnow()), msg.topic, f'key={msg.key}, value={msg.value}')
            REDIS.set('kafka', msg.offset)#more then 10 if i reload consumer
            if counter == 10:
                consumer.commit()
                counter = 0
            # while True:
            #     commit_every_10_seconds()
            #     time.sleep(10)
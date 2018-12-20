from kafka import KafkaConsumer
from consumer import REDIS
from consumer.models import Messages
import json
from consumer import SESSION

class Consumer:
    def __init__(self):
        consumer = KafkaConsumer('test_topic',
                                 bootstrap_servers=['localhost:9092'],
                                 consumer_timeout_ms=1000000,
                                 auto_commit_interval_ms=10000,
                                 value_deserializer=lambda m: json.loads(m.decode('ascii'))
                                 )

        for msg in consumer:
            print(f'topic: {msg.topic} and value added to database, offset {msg.offset}')
            session = SESSION()
            print(msg.value)
            message = Messages(msg.topic, f'key={msg.key}, value={msg.value}')
            REDIS.set('kafka', msg.offset)
            session.add(message)
            session.commit()
            session.close()

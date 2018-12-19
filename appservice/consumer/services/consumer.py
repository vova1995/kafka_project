from kafka import KafkaConsumer
from consumer import DB, REDIS
from consumer.models import Message
import json

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
            message = Message(msg.topic, f'key={msg.key}, value={msg.value}')
            REDIS.set('kafka', msg.offset)
            DB.session.add(message)
            DB.session.commit()

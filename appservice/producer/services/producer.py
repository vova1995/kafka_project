from kafka import KafkaProducer
from kafka.errors import KafkaError
import json

class Producer:
    def __init__(self):
        producer = KafkaProducer(bootstrap_servers=['kafka:9092'],
                                 value_serializer=lambda m: json.dumps(m).encode('ascii'))

        future = producer.send('json-topic', {'key': 'value'})

        try:
            record_metadata = future.get(timeout=10)
            print(record_metadata)
        except KafkaError:
            print('Application failed')
            pass

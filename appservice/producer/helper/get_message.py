from kafka.errors import KafkaError
import json

def getdata(data):
    try:
        record_metadata = data.get(timeout=10)
        print(record_metadata)
    except KafkaError:
        return json.dumps({
            'status': 'Aplication failed'
        }), 400
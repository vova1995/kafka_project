from kafka.errors import KafkaError
import json


def getdata(data):
    """
    Method that gets data from kafka
    :param data:
    :return: messages
    """
    try:
        record_metadata = data.get(timeout=10)
        print(record_metadata)
    except KafkaError:
        return json.dumps({
            'status': 'Application failed'
        }), 400

from kafka import KafkaProducer
from producer.helper import getdata
from producer import APP
from sanic.response import json
import json as j

@APP.route("/producer", methods=['POST'])
async def producer(request):
    data = request.json
    print(data)
    topic = data['topic']
    key = data['key']
    value = data['value']
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda m: j.dumps(m).encode('utf-8'))


    for _ in range(6):
        future = producer.send(topic=topic, value={key: value})

        getdata(future)

    return json({ "received": True, "message": request.json })

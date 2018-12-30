import json as j
import asyncio

from aiokafka import AIOKafkaProducer
from sanic.response import json
from api.app import APP
from api.logger_conf import make_logger
from api.config import Configs


LOGGER = make_logger('logs/producer_logs', 'producer_logs')


@APP.route("/producer", methods=['POST'])
async def producer(request):
    """
    Sanic producer that sends messages
    :param request:
    :return: json with message
    """
    data = request.json
    LOGGER.info(data)

    while True:
        try:
            producer = AIOKafkaProducer(bootstrap_servers=[f"{Configs['KAFKA_ADDRESS']}:{Configs['KAFKA_PORT']}"], loop=APP.loop,
                                        value_serializer=lambda m: j.dumps(m).encode('utf-8'))
            break
        except Exception as e:
            LOGGER.info(e)
            await asyncio.sleep(10)
    try:
        await producer.start()
        await producer.send_and_wait(topic=data['topic'], value={data['key']: data['value']})
    except Exception as e:
        LOGGER.error("Producer send error %s", e)
    finally:
        await producer.stop()
    return json({"received": True, "message": request.json})

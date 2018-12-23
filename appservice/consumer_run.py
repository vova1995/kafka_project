from consumer.services import Consumer
import asyncio

if __name__ == "__main__":
    print('Consumer started')
    consumer = Consumer()
    ioloop = asyncio.get_event_loop()
    tasks = [
        ioloop.create_task(consumer.listener()),
        ioloop.create_task(consumer.commit_10_seconds())
    ]
    ioloop.run_until_complete(asyncio.wait(tasks))
    ioloop.close()

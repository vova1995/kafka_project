import uuid
class FakeMessage:

    """Fakemessage DB"""
    id = uuid.uuid4()
    topic = 'pytest_topic'
    message = f'key=test_none, value=test_kafka'
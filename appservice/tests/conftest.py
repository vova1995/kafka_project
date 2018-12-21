import os
import tempfile

import pytest

# from producer import APP
from consumer import APP
from consumer.models import Messages
from .fake_message import FakeMessage


@pytest.fixture
def client():
    '''
    Our fake client
    :return:
    '''
    db_fd, APP.config['DATABASE'] = tempfile.mkstemp()
    APP.config['TESTING'] = True
    client = APP.test_client()

    yield client

    os.close(db_fd)
    os.unlink(APP.config['DATABASE'])


@pytest.fixture
def new_record():
    """
    Test for model Messages
    :return: user
    """
    topic = Messages(FakeMessage.topic, FakeMessage.message)
    return topic

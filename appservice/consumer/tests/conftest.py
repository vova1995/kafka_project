import os
import tempfile

import pytest

from api.app import APP
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
    from api.database import PostgresDatabaseManager

    PostgresDatabaseManager.insert(FakeMessage.id ,FakeMessage.topic, FakeMessage.message)

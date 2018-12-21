def test_new_record(new_record):
    """
    Test for model user
    :param new_user:
    :return: response in case correct user
    """
    assert new_record.topic == 'pytest_topic'

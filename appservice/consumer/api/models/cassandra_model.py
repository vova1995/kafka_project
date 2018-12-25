"""
    Module for cassandra model
"""
import uuid
from cassandra.cqlengine import columns
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model


class Message(Model):
    """
    Cassandra model message
    """
    __table_name__ = 'message'
    id = columns.UUID(primary_key=True, default=uuid.uuid4)
    topic = columns.Text(required=True)
    created_at = columns.DateTime()
    message = columns.Text(required=True)

    @classmethod
    def create_db(cls):
        sync_table(Message)

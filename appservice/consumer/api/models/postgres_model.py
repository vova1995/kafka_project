"""
    Module for postgres model
"""
import uuid

from sqlalchemy import Column, MetaData, String, Table
from sqlalchemy.dialects.postgresql import UUID


metadata = MetaData()
Messages = Table(
    "messages",
    metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('topic', String, nullable=False, unique=False),
    Column('message', String, nullable=False, unique=False)
)


models = (Messages,)

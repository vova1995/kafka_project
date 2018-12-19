from consumer import DB


class Message(DB.Model):
    __tablename__ = 'messages'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    topic = DB.Column(DB.String, unique=False, nullable=False)
    value = DB.Column(DB.String, unique=False, nullable=True)

    def __init__(self, topic, value):
        self.topic = topic
        self.value = value
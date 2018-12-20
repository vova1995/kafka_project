from sqlalchemy import create_engine, Column, String, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class Message(Base):
    __tablename__ = 'message'

    id = Column('id', INTEGER, primary_key=True, autoincrement=True)
    topic = Column('topic', String, nullable=False, unique=False)
    message = Column('message', String, nullable=False, unique=False)


engine = create_engine("postgresql://appservice:appservice@localhost:5432/appservice", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

session = Session()

message = Message()
message.topic = 'my_topic'
message.message = 'hello'
session.add(message)
session.commit()
session.close()

# import psycopg2
#
# try:
#     conn = psycopg2.connect(database = "appservice", user = "appservice", password = "appservice", host = "localhost", port = "5432")
# except:
#     print("I am unable to connect to the database")
#
# cur = conn.cursor()
# try:
#     cur.execute("CREATE TABLE messages (id serial PRIMARY KEY, topic varchar, value varchar);")
# except:
#     print("I can't drop our test database!")
#
# conn.commit() # <--- makes sure the change is shown in the database
# conn.close()
# cur.close()
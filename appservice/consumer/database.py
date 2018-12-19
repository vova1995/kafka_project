import psycopg2

try:
    conn = psycopg2.connect(database = "appservice", user = "appservice", password = "appservice", host = "localhost", port = "5432")
except:
    print("I am unable to connect to the database")

cur = conn.cursor()
try:
    cur.execute("CREATE TABLE messages (id serial PRIMARY KEY, topic varchar, value varchar);")
except:
    print("I can't drop our test database!")

conn.commit() # <--- makes sure the change is shown in the database
conn.close()
cur.close()
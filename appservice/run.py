from consumer import APP
from consumer.database import CreateTable, CreateCassandraTable

if __name__ == "__main__":
    CreateTable()
    CreateCassandraTable()
    APP.run(host="0.0.0.0", port=5000, debug=False)

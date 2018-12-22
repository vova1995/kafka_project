from consumer import APP
from consumer.database import CreateTable, CreateCassandraTable
import time

if __name__ == "__main__":
    CreateTable()
    # while True:
    #     try:
    #         CreateCassandraTable()
    #         break
    #     except Exception as e:
    #         print(e)
    #         time.sleep(10)
    CreateCassandraTable()

    APP.run(host="0.0.0.0", port=5000, debug=True)

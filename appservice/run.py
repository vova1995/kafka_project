"""
    Consumer run module
"""
import time

while True:
    try:
        from consumer import APP
        from consumer.database import CreateTable, CreateCassandraTable, CreateTableCassandra2
        if __name__ == "__main__":
            CreateTable()
            CreateCassandraTable()
            CreateTableCassandra2()
            APP.run(host="0.0.0.0", port=5001, debug=False)
            break
    except Exception:
        print('issue')
        time.sleep(10)

from consumer import APP
from consumer.database import Create_table

if __name__ == "__main__":
    Create_table()
    APP.run(host="0.0.0.0", port=5000, debug=False)

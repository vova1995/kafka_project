from consumer import APP
from consumer.database import CreateTable

if __name__ == "__main__":
    CreateTable()
    APP.run(host="0.0.0.0", port=5000, debug=False)

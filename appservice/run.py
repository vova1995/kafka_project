"""
    Consumer run module
"""

from consumer import APP

if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=5001, debug=False)

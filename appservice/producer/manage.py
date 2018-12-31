"""
    Producer run module
"""
def runserver(host='0.0.0.0', port=8000, debug=False):
    """
    Method runs consumer servie
    :param host: 0.0.0.0
    :param port: 5001
    :param debug: False
    :return:
    """
    from api.app import APP
    APP.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    runserver()
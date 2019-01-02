"""
    Producer run module
"""
import argparse
import sys

from api.app import LOGGER


def runserver(host='0.0.0.0', port=8000, debug=False):
    """
    Method runs producer service
    :param host: 0.0.0.0
    :param port: 5001
    :param debug: False
    :return:
    """
    from api.app import APP
    APP.run(host=host, port=port, debug=debug)


def override_configs(args):
    """
    Takes from a Namespace object arguments defined by user i.e. those that are not None
    and overrides Configs with them
    :param args: Namespace object
    :return: None
    """
    from api.config import Configs
    parameters = {k.upper(): v for k, v in args.__dict__.items() if k != 'command' and v is not None}
    Configs.update(parameters)


def parse_args():
    """
    Parses arguments given application on startup
    :return: Namespace object with parameters - dest's
    """
    parser = argparse.ArgumentParser(description="Sanic rest api skeleton", add_help=False)
    parser.add_argument("--help", action="help", help="show this help message and exit")
    parser.add_argument('-a', '--address', default='0.0.0.0', dest='host', type=str)
    parser.add_argument('-p', '--port', default=8000, dest='port', type=int)
    parser.add_argument('--kafka-address', dest='kafka_address', type=str)
    parser.add_argument('--kafka-port', dest='kafka_port', type=int)

    return parser.parse_args(sys.argv[1:])


def main():
    args = parse_args()
    override_configs(args)
    runserver(host=args.host, port=args.port)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        LOGGER.critical(
            "Unexpected exception occurred. Service is going to shutdown. Error message: {}".format(e),
            extra={"error_message": e},
        )
        exit(1)
    finally:
        LOGGER.info("Service stopped.")

"""
    Consumer run module
"""
import argparse
import asyncio
import sys
from api.app import LOGGER


def parse_args():

    parser = argparse.ArgumentParser(description="Sanic rest api skeleton", add_help=False)
    parser.add_argument("--help", action="help", help="show this help message and exit")

    subparser = parser.add_subparsers(dest='command')

    parser.add_argument('--postgres_user', dest='postgres_user', type=str)
    parser.add_argument('--postgres_password', dest='postgres_password', type=str)
    parser.add_argument('--postgres_database', dest='postgres_database', type=str)
    parser.add_argument('--postgres_address', dest='postgres_address', type=str)
    parser.add_argument('--kafka-address', dest='kafka_address', type=str)
    parser.add_argument('--kafka-port', dest='kafka_port', type=int)
    parser.add_argument('--offset-storage', dest='offset_storage', type=str)
    parser.add_argument('--data-storage', dest='data_storage', type=str)
    parser.add_argument('--zookeeper-host', dest='zookeeper_host', type=str)
    parser.add_argument('--zookeeper-port', dest='zookeeper_port', type=int)
    parser.add_argument('--redis-host', dest='redis_host', type=str)
    parser.add_argument('--redis-port', dest='redis_port', type=int)
    parser.add_argument('--cassandra-host', dest='cassandra-host', type=str)
    parser.add_argument('--cassandra-keyspace', dest='cassandra-keyspace', type=str)

    runserver_parser = subparser.add_parser('runserver')
    runserver_parser.add_argument('-a', '--address', default='0.0.0.0', dest='host', type=str)
    runserver_parser.add_argument('-p', '--port', default=5001, dest='port', type=int)

    subparser.add_parser('init_cassandra')
    subparser.add_parser('init_postgres')

    return parser.parse_args(sys.argv[1:])


def runserver(host='0.0.0.0', port=5001, debug=False):
    """
    Method runs consumer servie
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


def main():
    args = parse_args()

    override_configs(args)
    if args.command == 'init_postgres':
        from common.database import PostgresDatabaseManager
        loop = asyncio.get_event_loop()
        loop.run_until_complete(PostgresDatabaseManager.create())
    elif args.command == 'init_cassandra':
        from common.database import CassandraDatabaseManager
        loop = asyncio.get_event_loop()
        loop.run_until_complete(CassandraDatabaseManager.create())
    elif args.command == 'runserver':
        runserver(args.host, args.port)
    else:
        runserver()


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
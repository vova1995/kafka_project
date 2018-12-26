# Kafka_project
[![Kafka](https://img.shields.io/badge/streaming_platform-kafka-black.svg?style=flat-square)](https://kafka.apache.org)
[![Python](https://img.shields.io/badge/python-3.6+-blue.svg?style=flat-square)](https://www.python.org)

This project allows you to send and consumer messages using apache kafka and python.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You need to create repository and clone this project in it.

```
Example
git clone https://github.com/vova1995/kafka_project.git
```

### Installing

A step by step series of examples that tell you how to get a development env running

Run docker-compose and make sure that you installed docker and docker compose. Please navigate to the folder and do following
```
Sudo docker-compose up --build
```
### Usage
Please go to the postman and enter following json and use link http://0.0.0.0:8000/producer

```
{
	"topic": "test_topic",
	"key": "kafka",
	"value": "java"
}
```
In order to check amount of rows in db and current offset from REDIS, user following urls

```
http://0.0.0.0:5001/consumer_redis_offset
http://0.0.0.0:5001/consumer_zk_offset
http://0.0.0.0:5001/consumer_postgres_rows
http://0.0.0.0:5001/consumer_cassandra_rows
http://0.0.0.0:5001/consumer_cassandra2_rows

```
### Docker container usage
In order to check tables in postgres and cassandra use following
```
Postgres:
sudo docker ps -a
sudo docker exec -it <container name> psql -U appservice
SELECT * FROM messages;
Cassandra
sudo docker exec -it <container name> cqlsh
SELECT * FROM messages.messages;

```
### Testing
In order to check test please navigate to the folder tests and do following
```
pytest test_producer
```

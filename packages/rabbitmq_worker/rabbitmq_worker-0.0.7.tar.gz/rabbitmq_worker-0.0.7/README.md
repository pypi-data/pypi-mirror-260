# RabbitmqWorker - Python worker for Rabbitmq

RabbitmqWorker is a worker for rabbitmq which automatically reconnect to the broker if any disconnection occurs.

## Why?

The main library used to manage asynchronous tasks in python is Celery. Celery has its own internal message pattern that must be respected for celery to be able to interpret the messages correctly. In our architecture, we use microservices with multiple language where their task client does not follow Celery's message principle. 

The scope of this library is to make an simple library to manage every kind of message from rabbitmq.

## Installation

RabbitmqWorker is avaiable from [PyPI](https://pypi.python.org/). You can install it with pip.
```
$ pip install rabbitmq_worker
```

## Usage

Instanciate a `RabbitmqWorker` with the appropriate configuration to your needs and run it. E.g:
```python
def process_message(channel, basic_deliver, properties, body):
    print(body)
    channel.basic_ack(basic_deliver.delivery_tag)

rabbitmq_worker = RabbitmqWorker(
    amqp_url="amqp://guest:guest@localhost:5672/%2F",
    queue_name="my_queue",
    callback=process_message
)
rabbitmq_worker.run()
```

RabbitmqWorker use [pika](https://pika.readthedocs.io/en/stable/) under the hood so your amqp_url must be compliant with `URLParameters`(https://pika.readthedocs.io/en/stable/modules/parameters.html#urlparameters) object.
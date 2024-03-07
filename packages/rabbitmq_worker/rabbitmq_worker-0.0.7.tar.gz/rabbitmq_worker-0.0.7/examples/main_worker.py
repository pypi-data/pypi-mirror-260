import ssl
from rabbitmq_worker.worker import RabbitmqWorker


def my_callback(channel, basic_deliver, properties, body):
    print(body)
    channel.basic_ack(basic_deliver.delivery_tag)


if __name__ == "__main__":
    worker = RabbitmqWorker(
        amqp_url="amqps://guest:guest@localhost:5672/dev",
        queue_name="batch_stitching",
        ssl_context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2),
        callback=my_callback,
    )
    worker.run()

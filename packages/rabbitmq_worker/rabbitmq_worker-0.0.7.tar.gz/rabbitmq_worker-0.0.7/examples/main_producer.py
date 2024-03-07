import json
import ssl
from rabbitmq_worker.producer import RabbitmqProducer


if __name__ == "__main__":
    # basicConfig(level=DEBUG)
    worker = RabbitmqProducer(
        "amqps://guest:guest@localhost:5672/dev?heartbeat=10", ssl_context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    )
    with worker:
        worker.send_message(
            json.dumps({"hello": "world"}).encode("utf-8"),
            "ms_media_selector",
            "event.media_selector.selected.wow",
            {"app_id": "my_first_publisher", "content_type": "application/json"},
        )

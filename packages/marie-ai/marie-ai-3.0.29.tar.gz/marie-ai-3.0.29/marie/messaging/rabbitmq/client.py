import ssl
from typing import Any, Dict, Optional

import pika
from pika.exchange_type import ExchangeType

from marie.logging.predefined import default_logger as logger
from marie.utils.json import to_json


class BlockingPikaClient:
    def __init__(self, conf: Dict[str, str]):
        # "amazon-rabbitmq"  "rabbitmq"

        provider = conf.get("provider", "rabbitmq")
        hostname = conf.get("hostname", "localhost")
        port = int(conf.get("port", 5672))
        username = conf.get("username", "guest")
        password = conf.get("password", "guest")
        tls_enabled = conf.get("tls", False)

        # b-ff3d0999-a25b-4a5a-9775-e7ba76f8fa3d.mq.us-east-1.amazonaws.com
        if tls_enabled:
            url = f"amqps://{username}:{password}@{hostname}:{port}?connection_attempts=3&heartbeat=3600"
        else:
            url = f"amqp://{username}:{password}@{hostname}:{port}?connection_attempts=3&heartbeat=3600"

        parameters = pika.URLParameters(url)
        if provider == "amazon-rabbitmq":
            # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            ssl_context.set_ciphers("ECDHE+AESGCM:!ECDSA")
            parameters.ssl_options = pika.SSLOptions(context=ssl_context)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        # Turn on delivery confirmations
        self.channel.confirm_delivery()
        self.logger = logger

    def close(self):
        self.channel.close()
        self.connection.close()

    def declare_queue(self, queue_name: str, durable: Optional[bool] = True) -> Any:
        return self.channel.queue_declare(queue=queue_name, durable=durable)

    def exchange_declare(
        self,
        exchange,
        exchange_type=ExchangeType.direct,
        passive=False,
        durable=False,
    ) -> Any:
        """
        Declare an exchange on the RabbitMQ server
        :param exchange:
        :param exchange_type:
        :param passive:
        :param durable:
        :return:
        """
        return self.channel.exchange_declare(
            exchange=exchange,
            exchange_type=exchange_type,
            passive=passive,
            durable=durable,
        )

    def publish_message(self, exchange: str, routing_key: str, message) -> None:
        """
        Publish a message to an exchange with a routing key
        :param exchange:
        :param routing_key:
        :param message:
        """
        # channel = self.connection.channel()
        channel = self.channel
        hdrs = {"key": "val"}

        # this should be a configuration
        # we do an expiration of 24 hours https://www.rabbitmq.com/ttl.html
        hour = 60 * 60 * 1000
        mils = hour * 24

        properties = pika.BasicProperties(
            app_id="marie-service",
            content_type="application/json",
            headers=hdrs,
            delivery_mode=pika.DeliveryMode.Transient,
            expiration=str(mils),
        )
        # body = json.dumps(message, ensure_ascii=False)
        body = to_json(message)
        body = body.encode("utf-8")

        # Send a message
        try:
            channel.basic_publish(
                exchange, routing_key, body, properties, mandatory=True
            )
            self.logger.debug(
                f"Sent message. Exchange: {exchange}, Routing Key: {routing_key}"
            )
        except pika.exceptions.UnroutableError as e:
            self.logger.error(e)

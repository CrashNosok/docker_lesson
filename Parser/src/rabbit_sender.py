import pika
from config import logger
from Interfaces import MessageBroker


class RabbitSender(MessageBroker):
    def __init__(self, host, port, username, password, queue_name):

        self.rabbitmq_params = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=pika.PlainCredentials(username=username, password=password)
        )
        self.queue_name = queue_name

    def send(self, message):
        try:
            connection = pika.BlockingConnection(self.rabbitmq_params)
            channel = connection.channel()

            channel.queue_declare(queue=self.queue_name, durable=True)

            channel.basic_publish(exchange='', routing_key=self.queue_name, body=message, properties=pika.BasicProperties(
                delivery_mode=2,
            ))

            logger.info(f"Sent '{message}' to '{self.queue_name}'")

            connection.close()
        except Exception as error:
            logger.error(f"Can`t send message in queue {self.queue_name} with error {error}")

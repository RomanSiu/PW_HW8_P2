import pika

from datetime import datetime
from db_create import user_handler
import sys
import json

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='task_mock', exchange_type='direct')
channel.queue_declare(queue='phone_queue', durable=True)
channel.queue_declare(queue='email_queue', durable=True)
channel.queue_bind(exchange='task_mock', queue='phone_queue')
channel.queue_bind(exchange='task_mock', queue='email_queue')


def main(count):
    users = user_handler(count)
    for i in users:
        message = str(i["id"])
        if i.phone_number and i.email:
            publish(message, 'task_queue')
            publish(message, 'email_queue')
            continue
        elif i.phone_number:
            publish(message, 'phone_queue')
            continue
        elif i.email:
            publish(message, 'email_queue')
            continue
    connection.close()


def publish(message, routing_key):
    channel.basic_publish(
        exchange='task_mock',
        routing_key=routing_key,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))


if __name__ == '__main__':
    main(20)

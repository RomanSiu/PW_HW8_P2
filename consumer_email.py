from db_create import User
import pika
import connect
import time
import json

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_queue', durable=True)


def callback(ch, method, properties, body):
    user = User.objects(id=body.decode())
    user = user[0]
    print(f"Sending email to {user.email}")
    time.sleep(1)
    print(f"Email was send to {user.fullname}")
    user.update(check_field=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue='email_queue', on_message_callback=callback)


if __name__ == '__main__':
    channel.start_consuming()

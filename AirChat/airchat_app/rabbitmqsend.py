import pika
import json


def add_queue(email_id, body):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='email')

    payload = {'email_id': email_id, 'body': body}
    channel.basic_publish(exchange='', routing_key='email', body=json.dumps(payload))
    print("Email-", payload['email_id'],"added to queue!")
    connection.close()

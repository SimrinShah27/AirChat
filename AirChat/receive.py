import pika, sys, os
import json
from airchat import mail


def send_mail(payload):
    payload = json.loads(payload)
    mail.send_email(

            to_email=payload['email_id'],
            subject='Flight Information',
            text=json.dumps(payload['body']),
        )
    print("Sending email to:", payload['email_id'])
    print("Email sent successfully to: ",payload['email_id'],"!")

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='email')

    def callback(ch, method, properties, payload):
        send_mail(payload)

    channel.basic_consume(queue='email', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting to receive email..')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

''' This is an implementation of the rabbitmq (MQTT) request '''

import pika

node = '192.168.1.193'
port = 5672
username = "meche"
password = "meche"

# Connect to a remote AMQP server with a username/password
credentials = pika.PlainCredentials(username, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(node,
        port, '/', credentials))                                    
channel = connection.channel()

# Create a queue if it doesn't already exist
channel.queue_declare(queue='Rasp_1', durable=True)

# Define the properties and publish a message
props = pika.BasicProperties(
    headers= {
        'status': 'Good Quality',
        "alarm":"HI"
        },
    type ="Pi Sensor")

channel.basic_publish(
    exchange = '',
    routing_key = 'Rasp_1',
    body = '{"temp": 22, "pressure": 10, "level": 100 }',
    properties = props)

connection.close()
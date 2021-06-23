from logging import debug
from flask import Flask, render_template
from flask import json
from flask.json import jsonify
from flask_socketio import SocketIO, emit, disconnect, send
import pika
from flask_cors import CORS

from random import random
from time import sleep
from threading import Thread, Event

app = Flask(__name__, template_folder='template_folder')
app.config['SECRET_KEY'] = 'tellmewhoyouare!@$%'
app.config['DEBUG'] = True
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins='*')

#Random Number Generator Thread

thread = Thread()
thread_stop_event = Event()

@app.route("/")
def index():
    return render_template("index.html")

# def randomNumberGenerator():
#     """
#     Generate a random number every 1 second and emit to a socketio instance (broadcast)
#     Ideally to be run in a separate thread?
#     """
#     #infinite loop of magical random numbers
#     print("Making random numbers")
#     while not thread_stop_event.isSet():
#         number = round(random()*10, 3)
#         # print(number)
#         socketio.emit('newnumber', {'number': number}, namespace='/device')
#         socketio.sleep(3)

@socketio.on('connect', namespace='/device')
def connection():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    # Start the rabbitmq consumer thread only if the thread has not been started before.
    if not thread.isAlive():
        print("Starting Thread")
        thread = socketio.start_background_task(rabbit_consumer)

def rabbit_callback(ch, method, properties, body):
    while not thread_stop_event.isSet():
        result = body.decode()
        result = result
        print(result)
        socketio.emit('device_process_value', {'data': result}, namespace='/device')
        socketio.sleep(3)
        try:
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except: 
            pass
       
def rabbit_consumer():
    creds = pika.PlainCredentials(
        username="meche",
        password="meche")

    params = pika.ConnectionParameters(
        host="localhost",
        credentials=creds,
        virtual_host="/")

    connection = pika.BlockingConnection(params)

    # This is one channel inside the connection
    channel = connection.channel()
    channel.queue_declare(queue='Raps_1', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='Rasp_1', on_message_callback=rabbit_callback)
    channel.start_consuming()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
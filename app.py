from logging import debug
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, disconnect, send
import pika
from flask_cors import CORS

app = Flask(__name__, template_folder='template_folder')
app.config['SECRET_KEY'] = 'tellmewhoyouare!@$%'
app.config['DEBUG'] = True
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins='*')

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + msg)
	send(msg, broadcast=True)

# def rabbit_callback(ch, method, properties, body):
#     socketio.emit('connect', {'data': 'yes'})
#     print("body: ", body)

# @socketio.on("connect")
# def connect():
#     creds = pika.PlainCredentials(
#         username="guest",
#         password="guest")

#     params = pika.ConnectionParameters(
#         host="localhost",
#         credentials=creds,
#         virtual_host="/")

#     connection = pika.BlockingConnection(params)

#     # This is one channel inside the connection
#     channel = connection.channel()

#     # Declare the exchange we're going to use
#     exchange_name = ''
#     channel.exchange_declare(exchange=exchange_name, type='topic')
#     channel.queue_declare(queue='Rasp_1')
#     channel.queue_bind(exchange='', queue='Rasp_1', routing_key='Rasp_1')

#     channel.basic_consume(rabbit_callback, queue='Rasp_1', no_ack=True)
#     channel.start_consuming()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
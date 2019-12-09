from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
socketServer = SocketIO(app)

messagesList = []

@socketServer.on('connect')
def onConnection():
  emit('socketID', request.sid)
  socketServer.emit('messages', messagesList)

@socketServer.on('newMessage')
def handle_event(message):
  messagesList.append({ 'body': message['body'], 'socketId': message['socketId'] })
  socketServer.emit('messages', messagesList, broadcast=True)

@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  socketServer.run(app)
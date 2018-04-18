from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, join_room, leave_room
from Tetris import Tetris
import threading

app = Flask(__name__)
socketio = SocketIO(app)

games = { }

@socketio.on('connect')
def on_connect():
    # print('connected: ' + str(json))
    sid = request.sid
    def worker():
        tetris = Tetris(socketio, sid)
        games[sid] = tetris
        tetris.begin()
    t = threading.Thread(target=worker)
    t.start()

@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    games[sid].end()

@socketio.on('action')
def on_action(json):
    print('action: ' + str(json))

@socketio.on('end_action')
def on_end_action(json):
    print('action end: ' + str(json))

if __name__ == '__main__':
    socketio.run(app)

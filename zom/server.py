from flask import Flask, send_from_directory
from flask_socketio import SocketIO, emit
import eventlet
import os

eventlet.monkey_patch()

app = Flask(__name__, static_folder=".")
app.config["SECRET_KEY"] = "render-secret"

socketio = SocketIO(app, cors_allowed_origins="*")

participants = {}

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@socketio.on("join")
def join(username):
    sid = socketio.server.eio_sid
    participants[sid] = username
    emit("participants", participants, broadcast=True)

@socketio.on("signal")
def signal(data):
    emit(
        "signal",
        {"from": socketio.server.eio_sid, "signal": data["signal"]},
        to=data["to"]
    )

@socketio.on("message")
def message(text):
    emit(
        "message",
        {"from": participants.get(socketio.server.eio_sid, "User"), "text": text},
        broadcast=True
    )

@socketio.on("disconnect")
def disconnect():
    participants.pop(socketio.server.eio_sid, None)
    emit("participants", participants, broadcast=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    socketio.run(app, host="0.0.0.0", port=port)

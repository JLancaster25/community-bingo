from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit, join_room
from room_manager import Room
from ai_caller import call_phrase
from auth import authenticate, register


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


rooms = {}


@app.route("/register", methods=["POST"])
def api_register():
register(request.form["username"], request.form["password"])
return {"status":"ok"}


@app.route("/login", methods=["POST"])
def api_login():
ok = authenticate(request.form["username"], request.form["password"])
return {"success": ok}


@socketio.on("create_room")
def create_room(data):
code = data["code"]
rooms[code] = Room(code, data.get("password"))
join_room(code)
emit("room_created", {"code": code})


@socketio.on("join_room")
def join(data):
room = rooms[data["code"]]
card = room.add_player(request.sid)
join_room(data["code"])
emit("card", card.card)


@socketio.on("draw_number")
def draw(data):
room = rooms[data["code"]]
call = room.game.draw()
if not call: return
number = int(call[1:])
for card in room.players.values(): card.mark(number)
emit("number", {"call": call_phrase(call)}, room=data["code"])
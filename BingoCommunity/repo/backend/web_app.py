from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room
from room_manager import Room
from ai_caller import call_phrase
from auth import authenticate, register

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}

# -------------------------
# AUTH ROUTES
# -------------------------

@app.route("/register", methods=["POST"])
def api_register():
    register(
        request.form["username"],
        request.form["password"]
    )
    return {"status": "ok"}


@app.route("/login", methods=["POST"])
def api_login():
    ok = authenticate(
        request.form["username"],
        request.form["password"]
    )
    return {"success": ok}

@socketio.on("create_room")
def handle_create_room(data):
    code = data["code"]
    password = data.get("password")
    rooms[code] = Room(code, password)
    join_room(code)
    emit("room_created", {"code": code})


@socketio.on("join_room")
def handle_join_room(data):
    code = data["code"]
    room = rooms.get(code)
    if not room:
        emit("error", {"message": "Room not found"})
        return
    card = room.add_player(request.sid)
    join_room(code)
    emit("card", card.card)


@socketio.on("draw_number")
def handle_draw_number(data):
    code = data["code"]
    room = rooms.get(code)
    if not room:
        return
    call = room.game.draw()
    if not call:
        return
    number = int(call[1:])
    for card in room.players.values():
        card.mark(number)
    emit(
        "number",
        {"call": call_phrase(call)},
        room=code
    )



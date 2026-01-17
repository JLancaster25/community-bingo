from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, join_room, emit
from auth import register, login
from stats import leaderboard
from admin import is_admin
import os, random, secrets, string

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

BINGO = ["B","I","N","G","O"]
RANGES = {
    "B": range(1,16), "I": range(16,31),
    "N": range(31,46), "G": range(46,61),
    "O": range(61,76)
}

rooms = {}  # room_code -> state


# ---------- HELPERS ----------

def room_code():
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))

def bingo_card():
    card = {l: random.sample(RANGES[l], 5) for l in BINGO}
    card["N"][2] = "X"
    return card

def check_win(card, pattern):
    if pattern == "row":
        return any(all(card[l][i]=="X" for l in BINGO) for i in range(5))
    if pattern == "column":
        return any(all(v=="X" for v in card[l]) for l in BINGO)
    if pattern == "diagonal":
        return (
            all(card[BINGO[i]][i]=="X" for i in range(5)) or
            all(card[BINGO[i]][4-i]=="X" for i in range(5))
        )
    if pattern == "x":
        return (
            all(card[BINGO[i]][i]=="X" for i in range(5)) and
            all(card[BINGO[i]][4-i]=="X" for i in range(5))
        )
    if pattern == "corners":
        return card["B"][0]==card["B"][4]==card["O"][0]==card["O"][4]=="X"
    if pattern == "blackout":
        return all(card[l][i]=="X" for l in BINGO for i in range(5))
    return False


# ---------- ROUTES ----------

@app.route("/")
def index():
    return render_template("index.html")


# ---------- SOCKET EVENTS ----------

@socketio.on("create_room")
def create_room(data):
    name = data["name"]
    password = data["password"]

    code = room_code()
    rooms[code] = {
        "host": name,
        "password": password,
        "players": {name: bingo_card()},
        "pattern": "row",
        "pool": [],
        "drawn": []
    }

    session["name"] = name
    session["room"] = code
    join_room(code)

    emit("room_joined", {
        "room": code,
        "host": name,
        "players": [name]
    })


@socketio.on("join_room")
def join_room_evt(data):
    name, code, pw = data["name"], data["code"], data["password"]

    if code not in rooms:
        emit("error", "Room not found"); return
    room = rooms[code]

    if room["password"] != pw:
        emit("error", "Wrong password"); return
    if len(room["players"]) >= 30:
        emit("error", "Room full"); return

    session["name"] = name
    session["room"] = code

    if name not in room["players"]:
        room["players"][name] = bingo_card()

    join_room(code)

    emit("room_joined", {
        "room": code,
        "host": room["host"],
        "players": list(room["players"].keys())
    }, room=code)

    emit("card", room["players"][name])


@socketio.on("start_game")
def start_game(data):
    code = session.get("room")
    name = session.get("name")
    room = rooms.get(code)

    if not room or name != room["host"]:
        return

    room["pattern"] = data["pattern"]
    room["pool"] = list(range(1,76))
    random.shuffle(room["pool"])
    room["drawn"].clear()

    emit("game_started", room["pattern"], room=code)

@socketio.on("draw_number")
def draw_number():
    code = session.get("room")
    name = session.get("name")
    room = rooms.get(code)

    if not room or name != room["host"] or not room["pool"]:
        return

    number = room["pool"].pop()
    winners = []

    for player, card in room["players"].items():
        for l in BINGO:
            if number in card[l]:
                card[l][card[l].index(number)] = "X"
        if check_win(card, room["pattern"]):
            winners.append(player)

    emit("number", {
        "number": number,
        "winners": winners
    }, room=code)


@socketio.on("get_card")
def get_card():
    code = session.get("room")
    name = session.get("name")
    room = rooms.get(code)

    if room and name in room["players"]:
        emit("card", room["players"][name])


if __name__ == "__main__":
    socketio.run(app)



@app.route("/", methods=["GET","POST"])
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def r():
    register(request.form["username"], request.form["password"])
    return redirect("/")

@app.route("/login", methods=["POST"])
def l():
    uid = login(request.form["username"], request.form["password"])
    if uid:
        session["uid"]=str(uid)
        return redirect("/")
    return "Login failed",401

@app.route("/leaderboard")
def lb():
    return render_template("leaderboard.html", board=leaderboard())

@app.route("/admin")
def admin():
    if not is_admin(session.get("uid")):
        return "Forbidden",403
    return render_template("admin.html")

if __name__ == "__main__":
    socketio.run(app)


from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.secret_key = "super-secret"
socketio = SocketIO(app, cors_allowed_origins="*")

BINGO = ["B","I","N","G","O"]
RANGES = {
    "B": range(1,16), "I": range(16,31),
    "N": range(31,46), "G": range(46,61),
    "O": range(61,76)
}

players = {}
host = None
pattern = "row"
number_pool = []
drawn = []


def generate_card():
    card = {l: random.sample(RANGES[l], 5) for l in BINGO}
    card["N"][2] = "X"
    return card


def check_pattern(card):
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


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("join")
def join(name):
    global host
    session["name"] = name
    players[name] = generate_card()
    if not host:
        host = name
    emit("lobby", {
        "players": list(players.keys()),
        "host": host
    }, broadcast=True)


@socketio.on("start")
def start(selected):
    global number_pool, drawn, pattern
    if session.get("name") != host:
        return
    pattern = selected
    number_pool = list(range(1,76))
    random.shuffle(number_pool)
    drawn.clear()
    emit("started", pattern, broadcast=True)


@socketio.on("draw")
def draw():
    if session.get("name") != host or not number_pool:
        return
    number = number_pool.pop()
    drawn.append(number)

    winners = []
    for name, card in players.items():
        for l in BINGO:
            if number in card[l]:
                card[l][card[l].index(number)] = "X"
        if check_pattern(card):
            winners.append(name)

    emit("number", {
        "number": number,
        "winners": winners
    }, broadcast=True)


@socketio.on("get_card")
def get_card():
    emit("card", players.get(session.get("name")))


@socketio.on("chat")
def chat(msg):
    emit("chat", {
        "user": session.get("name"),
        "msg": msg
    }, broadcast=True)


@socketio.on("reset")
def reset():
    global players, host
    if session.get("name") != host:
        return
    players.clear()
    host = None
    emit("reset", broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)

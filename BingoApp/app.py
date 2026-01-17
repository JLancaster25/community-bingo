from flask import Flask, render_template, request, session, redirect
from flask_socketio import SocketIO, join_room, emit
from auth import register, login
from stats import leaderboard
from admin import is_admin
import os, random

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

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

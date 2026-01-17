from passlib.hash import bcrypt
from db import get_db

def register(username, password):
    db = get_db(); cur = db.cursor()
    cur.execute(
        "insert into users (username, password_hash) values (%s,%s)",
        (username, bcrypt.hash(password))
    )
    db.commit(); cur.close(); db.close()

def login(username, password):
    db = get_db(); cur = db.cursor()
    cur.execute("select id, password_hash from users where username=%s", (username,))
    u = cur.fetchone()
    cur.close(); db.close()
    return u["id"] if u and bcrypt.verify(password, u["password_hash"]) else None

from passlib.hash import bcrypt
from db import get_db

def register_user(username, password):
    pw_hash = bcrypt.hash(password)
    db = get_db()
    cur = db.cursor()

    cur.execute(
        "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
        (username, pw_hash)
    )

    db.commit()
    cur.close()
    db.close()

def authenticate_user(username, password):
    db = get_db()
    cur = db.cursor()

    cur.execute(
        "SELECT id, password_hash FROM users WHERE username=%s",
        (username,)
    )

    user = cur.fetchone()
    cur.close()
    db.close()

    if not user:
        return None

    if bcrypt.verify(password, user["password_hash"]):
        return user["id"]

    return None

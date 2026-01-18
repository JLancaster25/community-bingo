import bcrypt

# In-memory user store (Supabase-ready placeholder)
users = {}


def register(username, password):
    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )
    users[username] = hashed


def authenticate(username, password):
    stored = users.get(username)

    if not stored:
        return False

    return bcrypt.checkpw(
        password.encode("utf-8"),
        stored
    )

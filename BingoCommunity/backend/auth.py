import bcrypt


users = {}


def register(username, password):
users[username] = bcrypt.hashpw(password.encode(), bcrypt.gensalt())




def authenticate(username, password):
return bcrypt.checkpw(password.encode(), users.get(username, b""))
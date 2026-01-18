import redis, json

r = redis.Redis(host="REDIS_HOST", port=6379, decode_responses=True)

def save_room(code, room_data):
    r.set(f"room:{code}", json.dumps(room_data))

def load_room(code):
    data = r.get(f"room:{code}")
    return json.loads(data) if data else None

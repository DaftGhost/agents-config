import redis

r = redis.Redis()


def user_key(user_id):
    return f"user:{user_id}"


def get_user(user_id):
    return r.get(user_key(user_id))


def set_user(user_id, blob):
    r.set(user_key(user_id), blob, ex=86400)

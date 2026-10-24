import json


def load_users(path="data/users.json"):
    with open(path) as f:
        return json.load(f)


def display_name(user):
    return user["name"]

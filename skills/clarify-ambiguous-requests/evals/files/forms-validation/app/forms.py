import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def signup(data):
    if not EMAIL_RE.match(data.get("email", "")):
        raise ValueError("invalid email")
    if len(data.get("password", "")) < 8:
        raise ValueError("password too short")
    return {"email": data["email"]}


def login(data):
    if not EMAIL_RE.match(data.get("email", "")):
        raise ValueError("invalid email")
    return {"email": data["email"]}

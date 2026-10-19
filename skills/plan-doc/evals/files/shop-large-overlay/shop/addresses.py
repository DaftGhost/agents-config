BOOK = {}


def save(user_id, address):
    BOOK[user_id] = address


def get(user_id):
    return BOOK.get(user_id)

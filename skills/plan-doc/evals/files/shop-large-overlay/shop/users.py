def get_user(db, user_id):
    return {"id": user_id}


def display_name(user):
    return f"user-{user['id']}"

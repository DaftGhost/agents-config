def serialize_user(user):
    return {
        "id": user.id,
        "user_name": user.name,
        "email": user.email,
    }

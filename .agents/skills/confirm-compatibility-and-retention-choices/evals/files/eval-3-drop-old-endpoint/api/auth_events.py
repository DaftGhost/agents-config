from db import query


def get_auth_events(user_id):  # GET /v2/auth-events
    return query("SELECT * FROM auth_events WHERE user_id = ?", user_id)

from db import query


def get_login_history(user_id):  # GET /v1/login-history
    return query("SELECT * FROM login_history WHERE user_id = ?", user_id)

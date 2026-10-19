POINTS = {}


def award(user_id, cents):
    POINTS[user_id] = POINTS.get(user_id, 0) + cents // 100

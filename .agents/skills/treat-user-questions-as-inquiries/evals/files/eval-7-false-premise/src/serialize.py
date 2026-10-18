def serialize(payload):
    return {"id": payload["user_id"], "name": payload.get("name", "")}

def parse(payload):
    if payload is None:
        raise ValueError("payload is required")
    if "user_id" not in payload:
        raise ValueError("user_id is required")
    return {"user_id": payload["user_id"], "name": payload.get("name", "")}

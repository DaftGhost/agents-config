def serialize_order(o):
    return {"id": o.id, "status_code": o.status, "total": o.total}

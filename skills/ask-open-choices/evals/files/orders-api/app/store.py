ORDERS = [
    {"id": i, "customer": f"c{i % 7}", "total": i * 10, "status": "open"}
    for i in range(1, 501)
]

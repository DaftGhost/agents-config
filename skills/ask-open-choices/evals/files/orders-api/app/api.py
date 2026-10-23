from flask import Flask, jsonify, abort

from app.store import ORDERS

app = Flask(__name__)


@app.get("/orders")
def list_orders():
    return jsonify(ORDERS)


@app.get("/orders/<int:order_id>")
def get_order(order_id):
    for order in ORDERS:
        if order["id"] == order_id:
            return jsonify(order)
    abort(404)


@app.patch("/orders/<int:order_id>/cancel")
def cancel_order(order_id):
    for order in ORDERS:
        if order["id"] == order_id:
            order["status"] = "cancelled"
            return jsonify(order)
    abort(404)

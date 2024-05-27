from flask import request, jsonify
from schemas.orderSchema import order_schema, orders_schema
from marshmallow import ValidationError
from services import orderService

def save():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    order = orderService.save(order_data)

    if order is None:
        return jsonify({"error": "Order already exists"}), 400
    else:
        return order_schema.jsonify(order), 201
    
def find_all():
    orders = orderService.find_all()
    return orders_schema.jsonify(orders), 200
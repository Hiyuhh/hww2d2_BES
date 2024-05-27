from flask import request, jsonify
from schemas.customerSchema import customers_schema, customer_schema
from services import customerService
from marshmallow import ValidationError
from caching import cache

def save():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    customer = customerService.save(customer_data)

    if customer is None:
        return jsonify({"error": "Customer already exists"}), 400
    else:
        return customer_schema.jsonify(customer), 201

@cache.cached(timeout=60)
def find_all():
    customers = customerService.find_all()
    return customers_schema.jsonify(customers), 200

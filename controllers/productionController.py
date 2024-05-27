from flask import request, jsonify
from schemas.productSchema import product_schema, products_schema
from services import productService
from marshmallow import ValidationError

def save():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    product = productService.save(product_data)

    if product is None:
        return jsonify({"error": "Product already exists"}), 400
    else:
        return product_schema.jsonify(product), 201
    
def find_all():
    production = productService.find_all()
    return products_schema.jsonify(production), 200
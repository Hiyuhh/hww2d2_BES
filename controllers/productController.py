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
    args = request.args
    page = args.get('page', 1, type=int)
    per_page = args.get('per_page', 10, type=int)
    search_term = args.get('search')
    products = productService.find_all(page, per_page, search_term)
    return products_schema.jsonify(products)

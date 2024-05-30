from flask import request, jsonify
from schemas.userSchema import user_input_schema, user_output_schema, users_schema, user_login_schema
from services import userService
from marshmallow import ValidationError
from caching import cache

def save():
    try:
        user_data = user_input_schema.load(request.json)
        customer = userService.save(user_data)
        return user_output_schema.jsonify(customer), 201
    except ValidationError as e:
        return jsonify(e.messages), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@cache.cached(timeout=60)
def find_all():
    users = userService.find_all()
    return users_schema.jsonify(users), 200

def get_token():
    try:
        user_data = user_login_schema.load(request.json)
        token = userService.get_token(user_data['username'], user_data['password'])
        return jsonify(token), 200
    except ValidationError as e:
        return jsonify(e.messages), 400
    
def login():
    try:
        user_data = user_login_schema.load(request.json)
        user_token = userService.login(user_data['username'], user_data['password'])
        response = {"token": user_token, "message": "Success!"}
        return jsonify(response), 200
    except ValidationError as e:
        return jsonify(e.messages), 400
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except KeyError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400



    

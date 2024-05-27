from flask import request, jsonify
from schemas.employeeSchema import employee_schema, employees_schema
from services import employeeService
from marshmallow import ValidationError
from caching import cache

def save():
    try:
        employee_data = employee_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    employee = employeeService.save(employee_data)

    if employee is None:
        return jsonify({"error": "Employee already exists"}), 400
    else:
        return employee_schema.jsonify(employee), 201
    
@cache.cached(timeout=60)
def find_all():
    employees = employeeService.find_all()
    return employees_schema.jsonify(employees), 200


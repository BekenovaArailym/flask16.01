import json
from flask import jsonify

def get_profiles_from_file():
    with open("data.json", "r") as f:
        return json.load(f)
    
def set_profiles_to_file(data):
    with open("data.json", "w") as f:
        json.dump(data, f)

def jsonify_custom_response(obj, message="There is a profile with ID"):
    return {
        "message": message,
        "result": obj
    }

def jsonify_response(success, data=None, message=None, status_code=200):
    response = {
        'success': success,
        'data': data,
        'message': message
    }
    return jsonify(response), status_code

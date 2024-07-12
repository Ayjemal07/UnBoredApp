"""
Helpers file will essentially create an extra function 
to check tokens for rightful access to data, 
and create an encoder for our JSON content. 
"""

from functools import wraps
import secrets
from flask import request, jsonify, json
import decimal

from app.models import User

def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            #token = request.headers['x-access-token'].split(' ')[1]
            token = request.headers['x-access-token']
            print(token)
            
        if not token:
            return jsonify({'message': 'Token is missing. {}'.format(dict(request.headers))}), 401

        try:
            current_user_token = User.query.filter_by(token = token).first()
            print(token)
            print(current_user_token)
            print("end of try, no exception")
        except:
            print("exception caught")
            owner=User.query.filter_by(token=token).first()

            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated


# class JSONEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, decimal.Decimal):
#             return str(obj)
#         return super(JSONEncoder,self).default(obj)
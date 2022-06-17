from apps.models.user import User
from bson import json_util
from flask import request, Response, jsonify
from functools import wraps
import jwt
import os

secret_key = os.environ.get("SECRET_KEY")

if secret_key == None:
    secret_key = b'9Jx#\xdd\x0f1\xf4\xa6\x8f\t\x97\x14\x1dh\xe6'

# Funcion que verifica si el token es correcto para poder acceder a los servicios del sistema
def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()
        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]
            data = jwt.decode(token, secret_key)
            user = User()
            user = User.get_by_email(user, email=data['sub'])
            if user == None:
                #raise RuntimeError('User not found')
                message = {
                    'error': 'User not found'
                }
                response = json_util.dumps(message)
                return Response(response, mimetype='application/json', status=400)
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            response = json_util.dumps(expired_msg)
            return Response(response, mimetype='application/json', status=401)
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            response = json_util.dumps(invalid_msg)
            return Response(response, mimetype='application/json', status=401)

    return _verify
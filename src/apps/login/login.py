from flask import request, Response, Blueprint
from apps.models.users import signup, login as login_user, logout
from bson import json_util
from datetime import datetime, timedelta
import jwt
import os

login = Blueprint('login', __name__)

secret_key = os.environ.get("SECRET_KEY")

if secret_key == None:
    secret_key = b'9Jx#\xdd\x0f1\xf4\xa6\x8f\t\x97\x14\x1dh\xe6'

# Para registrarse en el sistema
@login.route('/signup', methods=['POST'])
def signup_service():
    username = request.json.get('username', None)
    type = request.json.get('type', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = {
        'username': username,
        'type': type,
        'email': email,
        'password': password
    }
    user_out, result = signup(user)
    if(result == 200):
        token = jwt.encode({
            'sub': user_out['email'],
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=3)},
            secret_key)
        user_out['token'] = token.decode('UTF-8')
        response = json_util.dumps(user_out)
        return Response(response, mimetype='application/json')
    elif(result == 4001):
        message = {"error": "Email address already in use"}
        response = json_util.dumps(message)
        return Response(response, mimetype='application/json', status=400)
    else:
        message = {"error": "Signup failed"}
        response = json_util.dumps(message)
        return Response(response, mimetype='application/json', status=400)

# Para cerrar sesion
@login.route('/logout')
def logout_service():
    logout()
    message = {"result": "Logged out"}
    response = json_util.dumps(message)
    return Response(response, mimetype='application/json')

# Para autenticarse en el sistema
@login.route('/login', methods=['POST'])
def log_in():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = {
        'email': email,
        'password': password
    }
    user_out, result = login_user(user)
    if(result == 200):
        token = jwt.encode({
            'sub': user_out['email'],
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=3)},
            secret_key)
        user_out['token'] = token.decode('UTF-8')
        response = json_util.dumps(user_out)
        return Response(response, mimetype='application/json')
    else:
        message = {"error": "Invalid login credentials"}
        response = json_util.dumps(message)
        return Response(response, mimetype='application/json', status=401)

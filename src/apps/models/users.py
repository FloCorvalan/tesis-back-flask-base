from flask import request, jsonify, Response, Blueprint
from flask import session
from passlib.hash import pbkdf2_sha256
from bson import json_util
from bson.objectid import ObjectId
from database.database import mongo

users = Blueprint('users', __name__)

#####################################################################
########################  SERVICIOS  ################################
#####################################################################

# Para crear un usuario
@users.route('/users', methods=['POST'])
def create_user():
    username = request.json.get('username', None)
    type = request.json.get('type', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if username and type and email and password:
        id = mongo.db.get_collection('users').insert_one(
            {
                'username': username,
                'type': type, 
                'email': email, 
                'password': password
            }
        )
        response = {
            'id': str(id),
            'username': username,
            'type': type,
            'email': email
        }
        return response
    else:
        return not_found()    

#####################################################################
#####################################################################
#####################################################################


#####################################################################
######################  CRUD NORMAL  ################################
#####################################################################

# Para obtener a todos los usuarios del sistema
@users.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.get_collection('users').find()
    response = json_util.dumps(users)
    return Response(response, mimetype='application/json')

# Para obtener un usuario segun su id
@users.route('/users/<id>', methods=['GET'])
def get_user(id):
    # find_one --> el primer dato que coincida
    user = mongo.db.get_collection('users').find_one({'_id': ObjectId(id)})
    response = json_util.dumps(user)
    return Response(response, mimetype='application/json')

# Para eliminar un usuario segun su id
@users.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = mongo.db.get_collection('users').delete_one({'_id': ObjectId(id)})
    response = jsonify({'message':'User' + id + ' was deleted successfully'})
    return response

# Para actualizar un usuario
@users.route('/users/<id>', methods=['PUT'])
def update_user(id):
    username = request.json.get('username', None)
    type = request.json.get('type', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if username and type and email and password:
        mongo.db.get_collection('users').update_one({'_id': ObjectId(id)}, {'$set': {
            'username': username,
            'type': type, 
            'email': email, 
            'password': password
        }})
        response = jsonify({'message':'User' + id + ' was updated successfully'})
        return response

# Para manejar errores 404
@users.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message':'Resouce Not Found: ' + request.url, 
        'status': 404
    })
    response.status_code = 404
    return response

#####################################################################
#####################################################################
#####################################################################


#####################################################################
######################  MANEJO DE SESIÓN  ###########################
#####################################################################

# Al iniciar la sesion se borra la contraseña y se agrega el id del usuario de respuesta al login
def start_session(user):
    del user['password']
    user['_id'] = str(user['_id'])
    return user

# Para registrarse
def signup(user):
    # Se revisa si el email esta registrado
    if mongo.db.get_collection('users').find_one({ "email": user['email'] }):
        return None, 4001 
    # Se encripta la contraseña
    user['password'] = pbkdf2_sha256.encrypt(user['password'])
    if mongo.db.get_collection('users').insert_one(user):
        user_out = start_session(user)
        return user_out, 200
    return None, 4002

# Para cerrar la sesion
def logout():
    session.clear()
    return 0

# Para iniciar sesion
def login(user):
    user_db = mongo.db.get_collection('users').find_one({
    "email": user['email']
    })

    if user_db and pbkdf2_sha256.verify(user['password'], user_db['password']):
        user_out = start_session(user_db)
        return user_out, 200
    
    return None, 401 

# Para obtener al usuario segun su email
def get_by_email(email):
    user_db = mongo.db.get_collection('users').find_one({
    "email": email
    })
    return user_db
    
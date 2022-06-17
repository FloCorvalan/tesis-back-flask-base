from flask import session
from passlib.hash import pbkdf2_sha256
from database.database import mongo

# Clase que maneja al usuario en la sesion
class User:

    # Al iniciar la sesion se borra la contraseña y se agrega el id del usuario de respuesta al login
    def start_session(self, user):
        del user['password']
        user['_id'] = str(user['_id'])
        return user

    # Para registrarse
    def signup(self, user):
        # Se revisa si el email esta registrado
        if mongo.db.get_collection('users').find_one({ "email": user['email'] }):
            return None, 4001 
        # Se encripta la contraseña
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        if mongo.db.get_collection('users').insert_one(user):
            user_out = self.start_session(user)
            return user_out, 200
        return None, 4002 
    
    # Para cerrar la sesion
    def logout(self):
        session.clear()
        return 0
  
    # Para iniciar sesion
    def login(self, user):
        user_db = mongo.db.get_collection('users').find_one({
        "email": user['email']
        })

        if user_db and pbkdf2_sha256.verify(user['password'], user_db['password']):
            user_out = self.start_session(user_db)
            return user_out, 200
        
        return None, 401 

    # Para obtener al usuario segun su email
    def get_by_email(self, email):
        user_db = mongo.db.get_collection('users').find_one({
        "email": email
        })
        return user_db
        
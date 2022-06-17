from json import loads
from bson import ObjectId

def test_login(test_client):
    '''HU11 - Escenario 1'
    'Dado que el líder de proyectos está registrado en el sistema'
    'Cuando ingresa correctamente su correo electrónico y contraseña'
    'E inicia sesión'
    'Entonces ingresa al sistema'''

    client, mongo = test_client

    response = client.post('/login', json={
        'email': 'hola@gmail.com',
        'password': '123456'
    })

    assert response.status_code == 200

    data_str = response.data.decode('utf8')

    data = loads(data_str)

    assert '_id' in data.keys()
    assert 'type' in data.keys()
    assert 'username' in data.keys()
    assert 'email' in data.keys()

    assert data['_id'] == '62831feddda8b46093c931f6'
    assert data['type'] == 'leader'
    assert data['username'] == 'Florencia'
    assert data['email'] == 'hola@gmail.com'
    assert b'token' in response.data


def test_singup(test_client):
    '''HU11 - Escenario 2'
    'Dado que el líder de proyectos no está registrado en el sistema'
    'Cuando ingresa un nombre de usuario, correo electrónico válido y una contraseña válida'
    'Y crea una cuenta'
    'Entonces es registrado en el sistema'
    'E ingresa a este'''


    client, mongo = test_client

    response = client.post('/signup', json={
        'username': 'Prueba',
        'type': 'leader',
        'email': 'hola1@gmail.com',
        'password': '1234567'
    })

    assert response.status_code == 200

    data_str = response.data.decode('utf8')

    data = loads(data_str)

    print(data)

    assert 'type' in data.keys()
    assert 'username' in data.keys()
    assert 'email' in data.keys()

    assert data['type'] == 'leader'
    assert data['username'] == 'Prueba'
    assert data['email'] == 'hola1@gmail.com'
    assert b'token' in response.data

    # Se borra el usuario creado
    mongo.db.get_collection('users').delete_one({'_id': ObjectId(data['_id'])})

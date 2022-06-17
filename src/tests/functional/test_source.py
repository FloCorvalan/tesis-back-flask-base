from ..conftest import create_auth_token
from bson import ObjectId
from json import loads


def test_source_create_and_delete(test_client):

    '''HU2 - Escenario 1'
    'Dado que no existe fuente de información de Jira asignada al equipo de desarrollo'
    'Cuando el líder de proyectos ingresa la información perteneciente a un proyecto de Jira'
    'Entonces el sistema asigna al equipo la fuente de información de Jira con la información ingresada'''


    client, mongo = test_client
    token = create_auth_token()
    response_team = client.post('/team/', json={
        'name': 'pruebados',
        'leader': '123456789'
    },
        headers={
        'Authorization': 'Bearer: {}'.format(token.decode('UTF-8'))
    })

    assert response_team.status_code == 200

    data_str_team = response_team.data.decode('utf8')

    data_team = loads(data_str_team)

    response = client.post('/source/', json={
        'type': 'jira',
        'user': 'usuariodeprueba',
        'token': 'tokendeprueba',
        'team_id': data_team['id'],
        'name': 'proyectodeprueba',
        'ip_port': 'urldeprueba'
    },
        headers={
        'Authorization': 'Bearer: {}'.format(token.decode('UTF-8'))
    })
    
    assert response.status_code == 200

    assert b"jira" in response.data
    assert b"usuariodeprueba" in response.data
    assert b"tokendeprueba" in response.data
    assert str.encode(data_team['id']) in response.data
    assert b"proyectodeprueba" in response.data
    assert b"urldeprueba" in response.data

    team = mongo.db.get_collection('team').find_one({'_id': ObjectId(data_team['id'])})

    data_str = response.data.decode('utf8')

    data = loads(data_str)

    assert team != None
    assert team['jira_source'] == data['id'] # Se valida que se asocio al equipo el source de jira creado

    response_del = client.delete('/source/' + data['id'])

    assert response_del.status_code == 200

    response_del_team = client.delete('/team/' + data_team['id'])

    assert response_del_team.status_code == 200


def test_check_jira_info(test_client):
    client, mongo = test_client

    '''HU4 - Escenario 1'
    'Dado que existe fuente de información de Jira registrada'
    'Cuando el líder de proyectos ingresa a la información registrada de un equipo de desarrollo'
    'Entonces el sistema entrega el email del dueño del proyecto de Jira, la key del proyecto de Jira y la URL del dueño del proyecto de Jira registrados'''

    # Se define el id de un equipo de desarrollo existente que posee una fuente de informacion
    # de Jira registrada
    team_id = '629f6ff71785c7fd81349a17'

    token = create_auth_token()
    response = client.get('/source/get-jira/' + team_id,
        headers={
        'Authorization': 'Bearer: {}'.format(token.decode('UTF-8'))
    })

    assert response.status_code == 200

    assert b"https://florencia-corvalan-lillo.atlassian.net" in response.data
    assert b"PTU" in response.data
    assert b"florencia.corvalan@usach.cl" in response.data


def test_check_project_info(test_client):
    client, mongo = test_client

    '''HU4 - Escenario 2'
    'Dado que existen proyectos asociados al equipo de desarrollo'
    'Cuando el líder de proyectos ingresa a la información registrada de un equipo de desarrollo'
    'Y selecciona un proyecto asociado al equipo de desarrollo'
    'Entonces el sistema entrega el nombre de usuario, el nombre del pipeline y la ip'
    'y el puerto de la fuente de información de Jenkins registrada; el nombre de usuario'
    'del dueño del repositorio y el nombre del repositorio de la fuente de información de' 
    'GitHub registrada; y el TAG registrado para la asociación de Jira'''


    # Se define el id de un proyecto de desarrollo existente que posee una fuente de informacion
    # de Jira registrada
    team_project_id = '629f70971785c7fd81349a19'
    # Se define el id del equipo dueño del proyecto
    team_id = '629f6ff71785c7fd81349a17'

    token = create_auth_token()
    response = client.get('/source/by-team-project/' + team_project_id,
        headers={
        'Authorization': 'Bearer: {}'.format(token.decode('UTF-8'))
    })

    assert response.status_code == 200

    data_str = response.data.decode('utf8')

    data = loads(data_str)

    assert 'jenkins' in data.keys()

    assert 'ip_port' in data['jenkins'].keys()
    assert 'name' in data['jenkins'].keys()
    assert 'user' in data['jenkins'].keys()

    assert 'github' in data.keys()

    assert 'name' in data['github'].keys()
    assert 'user' in data['github'].keys()

    assert data['jenkins']['ip_port'] == "188.166.118.192:8080"
    assert data['jenkins']['name'] == "prueba-tesis-uno"
    assert data['jenkins']['user'] == "admin"
    assert data['github']['name'] == "prueba-tesis-uno"
    assert data['github']['user'] == "FloCorvalan"

    response_tag = client.get('/team-project/by-team/' + team_id,
        headers={
        'Authorization': 'Bearer: {}'.format(token.decode('UTF-8'))
    })

    assert response_tag.status_code == 200

    data_str_tag = response_tag.data.decode('utf8')

    data_tag = loads(data_str_tag)

    assert '_id' in data_tag[0].keys()
    assert '$oid' in data_tag[0]['_id'].keys()
    assert data_tag[0]['_id']['$oid'] == team_project_id 

    assert 'tag' in data_tag[0].keys()
    assert data_tag[0]['tag'] == 'BACK'

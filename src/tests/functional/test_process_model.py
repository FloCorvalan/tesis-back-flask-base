from ..conftest import create_auth_token
from json import loads
from bson import ObjectId
import os

def test_get_activities_count(test_client):
    '''HU7 - Escenario 1'
    'Dado que se ha generado un dashboard asociado a un equipo de desarrollo'
    'Cuando el líder de proyectos selecciona un proyecto'
    'Entonces se muestra la cantidad de veces que fueron realizadas las actividades del proceso de desarrollo'''

    #team_id = '629f6ff71785c7fd81349a17'
    team_project_id = '629f70971785c7fd81349a19'

    client, mongo = test_client
    token = create_auth_token()
    response = client.post('/process-model/get-activities-count', json={
        'team_project_id': team_project_id
    },
        headers={
        'Authorization': 'Bearer: {}'.format(token.decode('UTF-8'))
    })

    data_str = response.data.decode('utf8')

    data = loads(data_str)

    assert b'SEGUIMIENTO_In Progress' in response.data
    assert b'PLANIFICACION' in response.data
    assert b'IMPLEMENTACION_test' in response.data
    assert b'IMPLEMENTACION_code' in response.data
    assert b'EJECUCION_PIPELINE' in response.data
    assert b'PRUEBAS' in response.data
    assert b'DESPLIEGUE' in response.data
    assert b'CONSTRUIR_IMAGEN' in response.data 
    assert b'CONSTRUIR' in response.data
    assert b'ANALISIS' in response.data

    assert 'jira' in data.keys()
    assert 'activities' in data['jira'].keys()
    assert 'count' in data['jira'].keys()
    
    assert 'github' in data.keys()
    assert 'activities' in data['github'].keys()
    assert 'count' in data['github'].keys()

    assert 'jenkins' in data.keys()
    assert 'activities' in data['jenkins'].keys()
    assert 'count' in data['jenkins'].keys()

    assert len(data['jira']['activities']) == len(data['jira']['count'])
    assert len(data['jenkins']['activities']) == len(data['jenkins']['count'])
    assert len(data['github']['activities']) == len(data['github']['count'])


def test_get_fitness(test_client):
    '''HU13 - Escenario 1'
    'Dado que se ha generado un dashboard asociado a un equipo de desarrollo y existe un modelo de proceso ideal'
    'Cuando el líder de proyectos selecciona un proyecto'
    'Entonces el sistema entrega la medida en que el proceso efectuado por los desarrolladores se ajusta a un modelo de proceso ideal'''


    #team_id = '629f6ff71785c7fd81349a17'
    team_project_id = '629f70971785c7fd81349a19'
    leader_id = '62831feddda8b46093c931f6'

    client, mongo = test_client
    token = create_auth_token()
    response = client.post('/process-model/get-fitness', json={
        'team_project_id': team_project_id, 
        'leader_id': leader_id
    },
        headers={
        'Authorization': 'Bearer: {}'.format(token.decode('UTF-8'))
    })

    assert response.status_code == 200

    data_str = response.data.decode('utf8')

    data = loads(data_str)

    assert 'avg' in data.keys()
    assert 'result' in data.keys()
    assert 'status' in data.keys()

    assert data['avg'] == 100
    assert len(data['result']) == 7
    assert data['status'] == True

def test_get_save_ideal_model(test_client):
    '''HU14 - Escenario 1'
    'Dado que se ha generado un dashboard asociado a un equipo de desarrollo'
    'Cuando el líder de proyectos selecciona un proyecto'
    'Y se ha generado un modelo de proceso en notación BPMN a partir de los datos extraídos desde las fuentes de información asociadas al proyecto'
    'Entonces el sistema permite seleccionar ese modelo de proceso como modelo de proceso ideal asociado al líder de proyectos'''

    #team_id = '629f6ff71785c7fd81349a17'
    team_project_id = '629f70971785c7fd81349a19'
    leader_id = '62831feddda8b46093c931f6'

    client, mongo = test_client
    token = create_auth_token()

    ideal_model = mongo.db.get_collection('users').find_one({'_id': ObjectId(leader_id), 'ideal_model_path': {'$exists': True}})
    if ideal_model != None:
        ideal_model_pnml = ideal_model['ideal_model_path']
        ideal_model_svg = ideal_model['ideal_model_path_svg']

    response = client.post('/process-model/save-ideal-model', json={
        'team_project_id': team_project_id, 
        'leader_id': leader_id
    },
        headers={
        'Authorization': 'Bearer: {}'.format(token.decode('UTF-8'))
    })

    assert response.status_code == 200

    data_str = response.data.decode('utf8')

    data = loads(data_str)

    exists_pnml = mongo.db.get_collection('users').find_one({'_id': ObjectId(leader_id), 'ideal_model_path': {'$exists': True}})
    exists_svg = mongo.db.get_collection('users').find_one({'_id': ObjectId(leader_id), 'ideal_model_path_svg': {'$exists': True}})

    pwd = os.getcwd()

    assert exists_pnml != None
    assert exists_svg != None
    assert exists_pnml['ideal_model_path'] == pwd + '/src/static/img/ideal_62831feddda8b46093c931f6.pnml'
    assert exists_svg['ideal_model_path_svg'] == pwd + '/src/static/img/ideal_62831feddda8b46093c931f6.svg'

    # Se restauran los valores
    if ideal_model != None:
        mongo.db.get_collection('users').update_one({'_id': ObjectId(leader_id)}, {'$set': {
            'ideal_model_path': ideal_model_pnml,
            'ideal_model_path_svg': ideal_model_svg
        }})

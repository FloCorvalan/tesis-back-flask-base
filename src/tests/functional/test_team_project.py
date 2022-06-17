from ..conftest import create_auth_token
from bson import ObjectId
from json import loads


def test_team_project_create_and_delete(test_client):

    '''HU3 - Escenario 1'
    'Dado que existe un proyecto asociado al equipo de desarrollo no ha sido registrado'
    'Cuando el líder de proyectos crea un proyecto'
    'E ingresa la información de un pipeline de Jenkins y un repositorio de GitHub'
    'Entonces el sistema crea el proyecto asociado al equipo'
    'Y se le asignan las fuentes de información de Jenkins y de GitHub'''

    client, mongo = test_client
    token = create_auth_token()

    # Se crea un equipo de desarrollo para hacer la prueba
    response_team = client.post('/team/', json={
        'name': 'pruebados',
        'leader': '123456789'
    },
        headers={
        'Authorization': 'Bearer: {}'.format(token.decode('UTF-8'))
    })

    data_str_team = response_team.data.decode('utf8')

    data_team = loads(data_str_team)

    # Se crea un proyecto asociado al equipo de desarrollo
    response = client.post('/team-project/add', json={
        'name': 'nombreproyecto',
        'tag': 'tagdeprueba',
        'jenkins_user': 'usuariojenkins',
        'jenkins_name': 'nombrejenkins',
        'jenkins_token': 'tokenjenkins',
        'jenkins_ip_port': 'ipportjenkins',
        'github_name': 'nombregithub',
        'github_user': 'usuariogithub',
        'github_token': 'tokengithub',
        'team_id': data_team['id'],
    },
        headers={
        'Authorization': 'Bearer: {}'.format(token.decode('UTF-8'))
    })

    # Se valida que se entregan los datos correctos como respuesta y el status de la respuesta
    assert response.status_code == 200
    assert b"nombreproyecto" in response.data
    assert b"tagdeprueba" in response.data


    data_str = response.data.decode('utf8')

    data = loads(data_str)

    assert 'sources' in data.keys()
    assert 'jenkins' in data['sources'].keys()
    assert 'github' in data['sources'].keys()

    jenkins_id = data['sources']['jenkins']
    github_id = data['sources']['github']

    # Se valida que se crearon los sources de jenkins y github
    jenkins = mongo.db.get_collection('source').find_one({'_id': ObjectId(jenkins_id)})
    github = mongo.db.get_collection('source').find_one({'_id': ObjectId(github_id)})

    assert jenkins != None
    assert github != None

    # Se busca el equipo para validar que se asocio el proyecto creado al equipo
    team = mongo.db.get_collection('team').find_one({'_id': ObjectId(data_team['id'])})

    assert team != None
    assert 'projects' in team.keys()
    assert 'id' in data.keys()
    assert data['id'] in team['projects'] # Se valida que se asocio al equipo el proyecto creado al equipo

    # Se borra todo lo que se creo
    response_del = client.delete('/team-project/' + data['id'])

    assert response_del.status_code == 200

    response_del_jenkins = client.delete('/source/' + jenkins_id)

    assert response_del_jenkins.status_code == 200

    response_del_github = client.delete('/source/' + github_id)

    assert response_del_github.status_code == 200

    response_del_team = client.delete('/team/' + data_team['id'])

    assert response_del_team.status_code == 200
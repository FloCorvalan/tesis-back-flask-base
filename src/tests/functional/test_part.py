from ..conftest import create_auth_token
from json import loads

def test_get_projects(test_client):
    '''HU5 - Escenario 1 parte 1'
    'Dado que existe al menos un proyecto asociado al equipo de desarrollo y está registrada la fuente de información de Jira'
    'Cuando el líder de proyectos accede al dashboard del equipo de desarrollo'
    'Entonces se genera el dashboard a partir de los datos extraídos de las fuentes de información registradas'''

    team_id = '629f6ff71785c7fd81349a17'

    client, mongo = test_client
    token = create_auth_token()
    response = client.post('/participation/get-projects', json={
        'team_id': team_id
    },
        headers={
        'Authorization': 'Bearer: {}'.format(token.decode('UTF-8'))
    })

    data_str = response.data.decode('utf8')

    data = loads(data_str)

    assert 'id' in data[0].keys()
    assert 'name' in data[0].keys()
    assert 'jenkins' in data[0].keys()
    assert 'github' in data[0].keys()

    assert len(data) == 1
    assert data[0]['id'] == '629f70971785c7fd81349a19'
    assert data[0]['name'] == 'backend'
    assert data[0]['jenkins'] == '629f70971785c7fd81349a1a'
    assert data[0]['github'] == '629f70971785c7fd81349a1b'

from ..conftest import create_auth_token
from json import loads

def test_team_create_and_delete(test_client):

    '''HU1 - Escenario 1'
    'Dado que el líder de proyectos está autenticado en el sistema'
    'Cuando crea un equipo de desarrollo'
    'Entonces el sistema crea un equipo de desarrollo asociado al líder de proyectos'''


    client, mongo = test_client
    token = create_auth_token()
    response = client.post('/team/', json={
        'name': 'prueba',
        'leader': '123456789'
    },
        headers={
        'Authorization': 'Bearer: {}'.format(token.decode('UTF-8'))
    })
    assert response.status_code == 200
    assert b"prueba" in response.data
    assert b"123456789" in response.data

    data_str = response.data.decode('utf8')

    data = loads(data_str)

    response_del = client.delete('/team/' + data['id'])

    assert response_del.status_code == 200

from flask import request, Response, Blueprint
from .methods import *
import requests
import os
from ..token.token import token_required
from json import loads

prod = Blueprint('prod', __name__)

# Hace el llamado al modulo de GitHub para obtener la productividad individual
@prod.route('/github', methods=['POST'])
@token_required
def get_github_prod():
    team_id = request.json['team_id']
    team_project_id = request.json['team_project_id']

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    base_url_github = os.environ.get("BASE_URL_GITHUB")

    url = base_url_github + '/github/prod' #'http://localhost:5003/github/prod'
    response = requests.request(
        "POST",
        url,
        headers=headers,
        json={
            "team_id": team_id, 
            "team_project_id": team_project_id
        }
    )

    return Response(response.content, mimetype='application/json')


# Hace el llamado al modulo de Jira para obtener la productividad grupal
@prod.route('/jira', methods=['POST'])
@token_required
def get_jira_prod():
    team_id = request.json['team_id']

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    base_url_jira = os.environ.get("BASE_URL_JIRA")

    url = base_url_jira + '/jira/prod' #'http://localhost:5001/jira/prod'
    response = requests.request(
        "POST",
        url,
        headers=headers,
        json={
            "team_id": team_id
        }
    )
    return Response(response.content, mimetype='application/json')


# Hace el llamado al modulo de GitHub para obtener los nombres de los desarrolladores que han
# participado en GitHub (generado codigo)
@prod.route('/part-names', methods=['POST'])
@token_required
def get_github_part_names():
    team_id = request.json['team_id']

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    base_url_jira = os.environ.get("BASE_URL_JIRA")

    url = base_url_jira + '/jira/get-sprint-timestamps'
    response = requests.request(
        "POST",
        url,
        headers=headers,
        json={
            "team_id": team_id
        }
    )

    data_str = response.content.decode('utf8')

    data = loads(data_str)

    base_url_github = os.environ.get("BASE_URL_GITHUB")

    url = base_url_github + '/github/part-names' 
    response_timestamps = requests.request(
        "POST",
        url,
        headers=headers,
        json={
            "team_id": team_id,
            'start_timestamp': data['start_timestamp'],
            'end_timestamp': data['end_timestamp']
        }
    )

    return Response(response_timestamps.content, mimetype='application/json')
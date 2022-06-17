from flask import Blueprint, Response, request
from .methods import *
from bson import json_util
import requests
import os
from ..token.token import token_required

participation = Blueprint('participation', __name__)

# Para obtener la informacion de los proyectos de un equipo de desarrollo
@participation.route('/get-projects', methods=['POST'])
@token_required
def get_team_projects_service():
    team_id = request.json['team_id']
    projects = get_team_projects(team_id)
    response = json_util.dumps(projects)
    return Response(response, 'application/json')


# Para hacer el llamado al modulo de Jenkins para obtener la participacion en Jenkins
@participation.route('/jenkins', methods=['POST'])
@token_required
def get_jenkins_part():
    team_project_id = request.json['team_project_id']
    source_id = request.json['source_id']

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    base_url_jenkins = os.environ.get("BASE_URL_JENKINS")

    url = base_url_jenkins + '/jenkins/participation' #'http://localhost:5001/jenkins/participation'
    response = requests.request(
        "POST",
        url,
        headers=headers,
        json={
            'team_project_id': team_project_id, 
            'source_id': source_id
        }
    )
    return Response(response.content, mimetype='application/json')


# Para hacer el llamado al modulo de Jira para obtener la participacion en Jira
@participation.route('/jira', methods=['POST'])
@token_required
def get_jira_part():
    team_id = request.json['team_id']

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    base_url_jira = os.environ.get("BASE_URL_JIRA")

    url =  base_url_jira + '/jira/participation' #'http://localhost:5001/jira/participation'
    response = requests.request(
        "POST",
        url,
        headers=headers,
        json={
            'team_id': team_id, 
        }
    )
    print(response.content)
    return Response(response.content, mimetype='application/json')


# Para hacer el llamado al modulo de GitHub para obtener la participacion en GitHub
@participation.route('/github', methods=['POST'])
@token_required
def get_github_part():
    team_project_id = request.json['team_project_id']
    source_id = request.json['source_id']

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    base_url_github = os.environ.get("BASE_URL_GITHUB")

    url = base_url_github + '/github/participation' #'http://localhost:5003/github/participation'
    response = requests.request(
        "POST",
        url,
        headers=headers,
        json={
            'team_project_id': team_project_id, 
            'source_id': source_id
        }
    )
    return Response(response.content, mimetype='application/json')

# Para hacer el llamado al modulo de Jenkins para obtener los stages de las ejecuciones del pipeline
# de un proyecto 
@participation.route('/jenkins/stages', methods=['POST'])
@token_required
def get_jenkins_stages():
    team_project_id = request.json['team_project_id']
    source_id = request.json['source_id']

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    base_url_jenkins = os.environ.get("BASE_URL_JENKINS")

    url = base_url_jenkins + '/jenkins/stages' 
    response = requests.request(
        "POST",
        url,
        headers=headers,
        json={
            'team_project_id': team_project_id, 
            'source_id': source_id
        }
    )
    return Response(response.content, mimetype='application/json')

from flask import Blueprint, Response, request, jsonify
from .methods import *
import os
import requests
from ..token.token import token_required
from ..pm.methods import process_data, get_fitness

process_model = Blueprint('process_model', __name__)

# Para obtener la cantidad de veces que se realizaron las actividades en el modelo de proceso generado
@process_model.route('/get-activities-count', methods=['POST'])
@token_required
def get_activities_cont_service():
    team_project_id = request.json['team_project_id']
    response = get_activities_cont(team_project_id)
    return Response(response, 'application/json')


# Obtiene los registros para Process Mining de todas las herramientas
# (llama a los modulos de Jira, Jenkins y GitHub)
@process_model.route('/get-model', methods=['POST'])
@token_required
def get_registers():
    team_id = request.json['team_id']
    team_project_id = request.json['team_project_id']
    source_id_jenkins = request.json['source_id_jenkins']
    source_id_github = request.json['source_id_github']
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    # Para Jenkins
    base_url_jenkins = os.environ.get("BASE_URL_JENKINS")
    url_jenkins = base_url_jenkins + '/jenkins' #'http://localhost:5001/jenkins'
    requests.request(
        "POST",
        url_jenkins,
        headers=headers,
        json={
            "team_id": team_id, 
            "team_project_id": team_project_id,
            "source_id": source_id_jenkins
        }
    )

    # Para Jira
    base_url_jira = os.environ.get("BASE_URL_JIRA")
    url_jira = base_url_jira + '/jira' #'http://localhost:5001/jira'
    requests.request(
        "POST",
        url_jira,
        headers=headers,
        json={
            "team_id": team_id
        }
    )

    # Para GitHub
    base_url_github = os.environ.get("BASE_URL_GITHUB")
    url_github = base_url_github + '/github' #'http://localhost:5003/github'
    requests.request(
        "POST",
        url_github,
        headers=headers,
        json={
            "team_project_id": team_project_id,
            "source_id": source_id_github
        }
    )

    print("VOY A ENTRAR A PROCESS DATA")

    # Para generar el modelo de proceso
    process_data(team_project_id)

    print("SALI DE PROCESS DATA")

    # Para obtener el modelo de proceso
    bpmn_str = get_last_bpmn(team_project_id)
    return Response(bpmn_str, mimetype='image/svg+xml')


# Obtiene en nivel de cumplimineto del proceso efectuado realmente respecto a un modelo de proceso ideal
@process_model.route('/get-fitness', methods=['POST'])
@token_required
def get_fitness_service():
    team_project_id = request.json['team_project_id']
    leader_id = request.json['leader_id']
    response = get_fitness(team_project_id, leader_id)
    return jsonify(response)


# Obtiene el modelo de proceso ideal asociado a un lider de proyectos
@process_model.route('/get-ideal-model', methods=['POST'])
@token_required
def get_ideal_bpmn_service():
    leader_id = request.json['leader_id']
     # Para obtener el modelo de proceso
    bpmn_str = get_ideal_bpmn(leader_id)
    return Response(bpmn_str, mimetype='image/svg+xml')


# Para seleccionar/guardar un modelo de proceso generado por el sistema como modelo de proceso ideal
# para un lider de proyectos
@process_model.route('/save-ideal-model', methods=['POST'])
@token_required
def save_ideal_bpmn_service():
    team_project_id = request.json['team_project_id']
    leader_id = request.json['leader_id']
    save_ideal_bpmn_path(team_project_id, leader_id)
    return jsonify({'message': 'saved'})
    
if __package__ is None or __package__ == '':
    # uses current directory visibility
    from ...database.database import mongo
else:
    # uses current package visibility
    from database.database import mongo
    #print(__package__)
from .db_methods import *
from bson import json_util
import shutil
import os

# Posibles actividades en los registros
ACT_JIRA = ['PLANIFICACION', 'SEGUIMIENTO_In Progress']
ACT_GITHUB = ['IMPLEMENTACION_code', 'IMPLEMENTACION_test']
ACT_JENKINS = ['PRUEBAS', 'ANALISIS', 'CONSTRUIR', 'CONSTRUIR_IMAGEN', 'DESPLIEGUE', 'EJECUCION_PIPELINE']
#########################################


# Obtiene el ultimo bpmn generado para ese id de proyecto
def get_last_bpmn(team_project_id):
    filepath = get_last_bpmn_db(team_project_id)
    with open(filepath, 'r') as file:
        data = file.read()
        file.close()
    return data


# Obtiene el modelo de proceso ideal
def get_ideal_bpmn(leader_id):
    filepath = get_ideal_bpmn_db(leader_id)
    with open(filepath, 'r') as file:
        data = file.read()
        file.close()
    return data

# Guarda el modelo de proceso generado para ese proyecto como modelo de proceso ideal para ese lider
# de proyectos
def save_ideal_bpmn_path(team_project_id, leader_id):
    filepath = get_last_bpmn_db(team_project_id)
    bpmn_file_path = filepath.split('.')
    bpmn_file_path_pnml = bpmn_file_path[0] + '.pnml'
    pwd = os.getcwd()
    dest_path = pwd + '/src/static/img/ideal_' + leader_id + '.pnml'
    dest_path_svg = pwd + '/src/static/img/ideal_' + leader_id + '.svg'
    # Se generan nuevos archivos para que no se reemplacen cuando se generen nuevos modelos para
    # el proyecto desde donde salio ese modelo 
    shutil.copy2(bpmn_file_path_pnml, dest_path)
    shutil.copy2(filepath, dest_path_svg)
    save_ideal_bpmn_path_db(leader_id, dest_path, dest_path_svg)


# Obtiene la cantidad de veces que se realizaron las actividades en el modelo de proceso
def get_activities_cont(team_project_id):
    result = get_activities_cont_db(team_project_id)
    activities_jira = []
    count_jira = []
    activities_github = []
    count_github = []
    activities_jenkins = []
    count_jenkins = []
    for res in result:
        if res['_id'] == 'jira':
            for act in res['activities']:
                activities_jira.append(act['activity'])
                count_jira.append(act['count'])
            for act in ACT_JIRA:
                if act not in activities_jira:
                    activities_jira.append(act)
                    count_jira.append(0)
        if res['_id'] == 'github':
            for act in res['activities']:
                activities_github.append(act['activity'])
                count_github.append(act['count'])
            for act in ACT_GITHUB:
                if act not in activities_github:
                    activities_github.append(act)
                    count_github.append(0)
        if res['_id'] == 'jenkins':
            for act in res['activities']:
                activities_jenkins.append(act['activity'])
                count_jenkins.append(act['count'])
            for act in ACT_JENKINS:
                if act not in activities_jenkins:
                    activities_jenkins.append(act)
                    count_jenkins.append(0)
    result = {
        'jira': {
            'activities': activities_jira, 
            'count': count_jira
        }, 
        'github': {
            'activities': activities_github,
            'count': count_github
        },
        'jenkins': {
            'activities': activities_jenkins, 
            'count': count_jenkins
        }
    }
    response = json_util.dumps(result)
    return response
    
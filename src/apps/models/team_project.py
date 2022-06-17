from flask import request, jsonify, Response, Blueprint
from bson import json_util
from bson.objectid import ObjectId
from database.database import mongo
from ..token.token import token_required

team_project = Blueprint('team_project', __name__)

# Para manejar errores 404
@team_project.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message':'Resouce Not Found: ' + request.url, 
        'status': 404
    })
    response.status_code = 404
    return response

#####################################################################
########################  SERVICIOS  ################################
#####################################################################

# Para crear un proyecto con sus fuentes de informacion de Jenkins y GitHub, el TAG de Jira
# y asociarlo al equipo de desarrollo
@team_project.route('/add', methods=['POST'])
@token_required
def create_team_project_sources():
    name = request.json.get('name', None)
    tag = request.json.get('tag', None)
    jenkins_user = request.json.get('jenkins_user', None)
    jenkins_name = request.json.get('jenkins_name', None)
    jenkins_token = request.json.get('jenkins_token', None)
    jenkins_ip_port = request.json.get('jenkins_ip_port', None)
    github_name = request.json.get('github_name', None)
    github_user = request.json.get('github_user', None)
    github_token = request.json.get('github_token', None)
    team_id = request.json.get('team_id', None)
    

    if name and tag and jenkins_user and jenkins_name and jenkins_token and jenkins_ip_port and github_name and github_user and github_token and team_id:
        # Se crea el proyecto
        team_project = mongo.db.get_collection('team_project').insert_one(
            {
                'name': name,
                'tag': tag,
                'case_id': 0
            }
        )

        team_project_id = str(team_project.inserted_id)

        # Se crean los sources 
        jenkins = mongo.db.get_collection('source').insert_one(
            {
                'type': 'jenkins',
                'user': jenkins_user, 
                'token': jenkins_token, 
                'name': jenkins_name,
                'ip_port': jenkins_ip_port,
                'team_project_id': team_project_id, 
                'team_id': team_id
            }
        )

        jenkins_id = str(jenkins.inserted_id)

        github = mongo.db.get_collection('source').insert_one(
            {
                'type': 'github',
                'user': github_user, 
                'token': github_token, 
                'name': github_name,
                'team_project_id': team_project_id, 
                'team_id': team_id
            }
        )

        github_id = str(github.inserted_id)

        # Se agregan los ids de los sources al team_project
        mongo.db.get_collection('team_project').update_one({'_id': ObjectId(team_project_id)}, {'$set': {
            'sources': {
                'jenkins': jenkins_id,
                'github': github_id
            }
        }})

        # Se asocia el team_proyect al team
        team_project_exists = mongo.db.get_collection('team').find_one({'_id': ObjectId(team_id), 'projects': {'$exists': True}})
        projects = []
        if(team_project_exists != None):
            for p in team_project_exists['projects']:
                projects.append(p)
        projects.append(team_project_id)
        mongo.db.get_collection('team').update_one({'_id': ObjectId(team_id)}, {'$set': {
            'projects': projects
        }})

        response = {
            'id': team_project_id,
            'name': name, 
            'sources': {
                'jenkins': jenkins_id,
                'github': github_id
            },
            'tag': tag
        }
        return response
    else:
        return not_found()

# Para obtener todos los proyectos de un equipo de desarrollo segun su id
@team_project.route('/by-team/<id>', methods=['GET'])
@token_required
def get_team_project_by_team_id(id):
    team = mongo.db.get_collection('team').find_one({'_id': ObjectId(id)})
    projects_exists = mongo.db.get_collection('team').find_one({'_id': ObjectId(id), 'projects': {'$exists': True}})
    team_projects = []
    if(team != None and projects_exists != None):
        team_projects_id = team['projects']
        for project_id in team_projects_id:
            project = mongo.db.get_collection('team_project').find_one({'_id': ObjectId(project_id)})
            team_projects.append(project)
    response = json_util.dumps(team_projects)
    return Response(response, mimetype='application/json')

#####################################################################
#####################################################################
#####################################################################


#####################################################################
######################  CRUD NORMAL  ################################
#####################################################################

# Para crear un proyecto
@team_project.route('/', methods=['POST'])
def create_team_project():
    name = request.json.get('name', None)
    jenkins = request.json.get('jenkins', None)
    github = request.json.get('github', None)
    tag = request.json.get('tag', None)

    if name and jenkins and github and tag:
        id = mongo.db.get_collection('team_project').insert_one(
            {
                'name': name, 
                'sources': {
                    'jenkins': jenkins,
                    'github': github
                },
                'tag': tag,
                'case_id': 0
            }
        )
        response = {
            'id': id,
            'name': name, 
            'sources': {
                'jenkins': jenkins,
                'github': github
            },
            'tag': tag
        }
        return response
    else:
        return not_found()

# Para obtener todos los proyectos
@team_project.route('/', methods=['GET'])
def get_team_projects():
    team_project = mongo.db.get_collection('team_project').find()
    response = json_util.dumps(team_project)
    return Response(response, mimetype='application/json')

# Para obtener un proyecto segun su id
@team_project.route('/<id>', methods=['GET'])
def get_team_project_by_id(id):
    # find_one --> el primer dato que coincida
    team_project = mongo.db.get_collection('team_project').find_one({'_id': ObjectId(id)})
    response = json_util.dumps(team_project)
    return Response(response, mimetype='application/json')

# Para borrar un proyecto segun su id
@team_project.route('/<id>', methods=['DELETE'])
def delete_team_project(id):
    team_project = mongo.db.get_collection('team_project').delete_one({'_id': ObjectId(id)})
    response = jsonify({'message':'team_project' + id + ' was deleted successfully'})
    return response

# Para actualizar un proyecto segun su id
@team_project.route('/<id>', methods=['PUT'])
def update_team_project(id):
    name = request.json.get('name', None)
    jenkins = request.json.get('jenkins', None)
    github = request.json.get('github', None)
    tag = request.json.get('tag', None)

    has_changed = 0

    if name:
        has_changed = 1
        mongo.db.get_collection('team_project').update_one({'_id': ObjectId(id)}, {'$set': {
            'name': name
        }})
    if github:
        has_changed = 1
        team_project = mongo.db.get_collection('team_project').find_one({'_id': ObjectId(id)})
        dic = {}
        for k in team_project['sources'].keys():
            dic[k] = team_project['sources'][k]
        dic['github'] = github
        mongo.db.get_collection('team_project').update_one({'_id': ObjectId(id)}, {'$set': {
           'sources': dic
        }})
    if jenkins:
        has_changed = 1
        team_project = mongo.db.get_collection('team_project').find_one({'_id': ObjectId(id)})
        dic = {}
        for k in team_project['sources'].keys():
            dic[k] = team_project['sources'][k]
        dic['jenkins'] = jenkins
        mongo.db.get_collection('team_project').update_one({'_id': ObjectId(id)}, {'$set': {
           'sources': dic
        }})
    if tag:
        has_changed = 1
        mongo.db.get_collection('team_project').update_one({'_id': ObjectId(id)}, {'$set': {
            'tag': tag
        }})
    if has_changed == 1:
        response = jsonify({'message':'team_project' + id + ' was updated successfully'})
    else: 
        response = jsonify({'message':'No change'})
    return response

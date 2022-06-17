from flask import request, jsonify, Response, Blueprint
from bson import json_util
from bson.objectid import ObjectId
from database.database import mongo
from ..token.token import token_required

source = Blueprint('source', __name__)

# Para manejar errores 404
@source.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resouce Not Found: ' + request.url,
        'status': 404
    })
    response.status_code = 404
    return response

#####################################################################
########################  SERVICIOS  ################################
#####################################################################

# Para crear un source o fuente de informacion de Jira, Jenkins o GitHub
@source.route('/', methods=['POST'])
@token_required
def create_source():
    type = request.json.get('type', None)
    user = request.json.get('user', None)
    token = request.json.get('token', None)
    team_project_id = request.json.get('team_project_id', None)
    team_id = request.json.get('team_id', None)
    name = request.json.get('name', None)
    ip_port = request.json.get('ip_port', None)

    if type == 'github':
        if user and token and team_id and name:
            id = mongo.db.get_collection('source').insert_one(
                {
                    'type': type,
                    'user': user,
                    'token': token,
                    'team_project_id': team_project_id,
                    'team_id': team_id,
                    'name': name
                }
            )
        response = {
            'type': type,
            'user': user,
            'token': token,
            'team_project_id': team_project_id,
            'team_id': team_id,
            'name': name
        }
        team_project_sources = mongo.db.get_collection('team_project').find_one({'_id': ObjectId(team_project_id), 'sources': {'$exists': True}})
        if(team_project_sources != None):
            sources = {}
            for k in team_project_sources.keys():
                sources[k] = team_project_sources[k]
            sources['github'] = str(id.inserted_id)
        else:
            sources = {
                'github': str(id.inserted_id)
            }
        mongo.db.get_collection('team_project').update_one({'_id': ObjectId(team_project_id)}, {'$set': {
            'sources': sources
        }})
        return response
    if type == 'jenkins':
        if user and token and team_id and name and ip_port:
            id = mongo.db.get_collection('source').insert_one(
                {
                    'type': type,
                    'user': user,
                    'token': token,
                    'team_project_id': team_project_id,
                    'team_id': team_id,
                    'name': name,
                    'ip_port': ip_port
                }
            )
        response = {
            'type': type,
            'user': user,
            'token': token,
            'team_project_id': team_project_id,
            'team_id': team_id,
            'name': name,
            'ip_port': ip_port
        }
        team_project_sources = mongo.db.get_collection('team_project').find_one({'_id': ObjectId(team_project_id), 'sources': {'$exists': True}})
        if(team_project_sources != None):
            sources = {}
            for k in team_project_sources.keys():
                sources[k] = team_project_sources[k]
            sources['jenkins'] = str(id.inserted_id)
        else:
            sources = {
                'jenkins': str(id.inserted_id)
            }
        mongo.db.get_collection('team_project').update_one({'_id': ObjectId(team_project_id)}, {'$set': {
            'sources': sources
        }})
        return response
    elif type == 'jira':
        if user and token and team_id and name and ip_port:
            id = mongo.db.get_collection('source').insert_one(
                {
                    'type': type,
                    'user': user,
                    'token': token,
                    'team_id': team_id,
                    'name': name,
                    'ip_port': ip_port
                }
            )
        response = {
            'id': str(id.inserted_id),
            'type': type,
            'user': user,
            'token': token,
            'team_id': team_id,
            'name': name,
            'ip_port': ip_port
        }
        mongo.db.get_collection('team').update_one({'_id': ObjectId(team_id)}, {'$set': {
            'jira_source': str(id.inserted_id)
        }})
        return response
    else:
        return not_found()

# Para obtener los sources por proyecto segun su id
@source.route('/by-team-project/<id>', methods=['GET'])
@token_required
def get_source_by_team_project_id(id):
    team_project = mongo.db.get_collection('team_project').find_one({'_id': ObjectId(id)})
    sources = {}
    if(team_project != None):
        sources_id = team_project['sources']
        jenkins_id = sources_id['jenkins']
        github_id = sources_id['github']
        jenkins = mongo.db.get_collection('source').find_one({'_id': ObjectId(jenkins_id)})
        if(jenkins != None):
            sources['jenkins'] = jenkins
        github = mongo.db.get_collection('source').find_one({'_id': ObjectId(github_id)})
        if(github != None):
            sources['github'] = github
    response = json_util.dumps(sources)
    return Response(response, mimetype='application/json')

# Para obtener el source de Jira de un equipo de desarrollo segun su id
@source.route('/get-jira/<id>', methods=['GET'])
@token_required
def get_source_jira(id):
    team = mongo.db.get_collection('team').find_one({'_id': ObjectId(id)})
    jira = None
    jira_source_exists = mongo.db.get_collection('team').find_one({'_id': ObjectId(id), 'jira_source': {'$exists': True}})
    if(team != None and jira_source_exists != None):
        jira_id = team['jira_source']
        jira = mongo.db.get_collection('source').find_one({'_id': ObjectId(jira_id)})
    response = json_util.dumps(jira)
    return Response(response, mimetype='application/json')

#####################################################################
#####################################################################
#####################################################################


#####################################################################
######################  CRUD NORMAL  ################################
#####################################################################

# Para obtener todos los sources
@source.route('/', methods=['GET'])
def get_sources():
    source = mongo.db.get_collection('source').find()
    response = json_util.dumps(source)
    return Response(response, mimetype='application/json')

# Para obtener un source por id
@source.route('/<id>', methods=['GET'])
def get_source_by_id(id):
    # find_one --> el primer dato que coincida
    source = mongo.db.get_collection('source').find_one({'_id': ObjectId(id)})
    response = json_util.dumps(source)
    return Response(response, mimetype='application/json')

# Para eliminar un source 
@source.route('/<id>', methods=['DELETE'])
def delete_source(id):
    source = mongo.db.get_collection('source').delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'source' + id +
                        ' was deleted successfully'})
    return response

# Para actualizar un source
@source.route('/<id>', methods=['PUT'])
def update_source(id):
    type = request.json.get('type', None)
    user = request.json.get('user', None)
    token = request.json.get('token', None)
    source_id = request.json.get('source_id', None)
    team_id = request.json.get('team_id', None)
    name = request.json.get('name', None)
    ip_port = request.json.get('ip_port', None)

    has_changed = 0

    if name:
        has_changed = 1
        mongo.db.get_collection('source').update_one({'_id': ObjectId(id)}, {'$set': {
            'name': name
        }})
    if type:
        has_changed = 1
        mongo.db.get_collection('source').update_one({'_id': ObjectId(id)}, {'$set': {
            'type': type
        }})
    if user:
        has_changed = 1
        mongo.db.get_collection('source').update_one({'_id': ObjectId(id)}, {'$set': {
            'user': user
        }})
    if token:
        has_changed = 1
        mongo.db.get_collection('source').update_one({'_id': ObjectId(id)}, {'$set': {
            'token': token
        }})
    if source_id:
        has_changed = 1
        mongo.db.get_collection('source').update_one({'_id': ObjectId(id)}, {'$set': {
            'source_id': source_id
        }})
    if team_id:
        has_changed = 1
        mongo.db.get_collection('source').update_one({'_id': ObjectId(id)}, {'$set': {
            'team_id': team_id
        }})
    if ip_port:
        has_changed = 1
        mongo.db.get_collection('source').update_one({'_id': ObjectId(id)}, {'$set': {
            'ip_port': ip_port
        }})
    if has_changed == 1:
        response = jsonify({'message': 'source ' + id +
                            ' was updated successfully'})
    else:
        response = jsonify({'message': 'No change'})
    return response

from flask import request, jsonify, Response, Blueprint
from bson import json_util
from bson.objectid import ObjectId
from database.database import mongo
from ..token.token import token_required

team = Blueprint('team', __name__)

# Para manejar errores 404
@team.errorhandler(404)
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

# Para crear un equipo de desarrollo
@team.route('/', methods=['POST'])
@token_required
def create_team():
    name = request.json.get('name', None)
    leader = request.json.get('leader', None)
    if name and leader:
        id = mongo.db.get_collection('team').insert_one(
            {
                'name': name, 
                'leader': leader, 
                'last_case_id': 0
            }
        )
        response = {
            'id': str(id.inserted_id),
            'name': name, 
            'leader': leader,
        }
        return response
    else:
        return not_found()

# Para obtener los equipos de desarrollo asociados a un lider de proyectos segun su id
@team.route('/by-leader', methods=['POST'])
@token_required
def get_team_by_leader_id():
    leader_id = request.json['leader_id']
    teams = mongo.db.get_collection('team').find({'leader': leader_id})
    response = json_util.dumps(teams)
    return Response(response, mimetype='application/json')

#####################################################################
#####################################################################
#####################################################################


#####################################################################
######################  CRUD NORMAL  ################################
#####################################################################

# Para obtener todos los equipos de desarrollo
@team.route('/', methods=['GET'])
def get_teams():
    team = mongo.db.get_collection('team').find()
    response = json_util.dumps(team)
    return Response(response, mimetype='application/json')

# Para obtener un equipo de desarrollo segun su id
@team.route('/<id>', methods=['GET'])
def get_team_by_id(id):
    # find_one --> el primer dato que coincida
    team = mongo.db.get_collection('team').find_one({'_id': ObjectId(id)})
    response = json_util.dumps(team)
    return Response(response, mimetype='application/json')

# Para eliminar un equipo de desarrollo
@team.route('/<id>', methods=['DELETE'])
def delete_team(id):
    team = mongo.db.get_collection('team').delete_one({'_id': ObjectId(id)})
    response = jsonify({'message':'Team' + id + ' was deleted successfully'})
    return response

# Para actualizar un equipo de desarrollo
@team.route('/<id>', methods=['PUT'])
def update_team(id):
    name = request.json.get('name', None)
    leader = request.json.get('leader', None)
    jira_source = request.json.get('jira_source', None)
    developers = request.json.get('developers', None)
    projects = request.json.get('projects', None)

    has_changed = 0

    if name:
        has_changed = 1
        mongo.db.get_collection('team').update_one({'_id': ObjectId(id)}, {'$set': {
            'name': name
        }})
    if leader:
        has_changed = 1
        mongo.db.get_collection('team').update_one({'_id': ObjectId(id)}, {'$set': {
            'leader': leader
        }})
    if jira_source:
        has_changed = 1
        mongo.db.get_collection('team').update_one({'_id': ObjectId(id)}, {'$set': {
            'jira_source': jira_source
        }})
    if developers:
        has_changed = 1
        developers_exists = mongo.db.get_collection('team').find_one({'_id': ObjectId(id), 'developers': {'$exists': True}})
        if developers_exists != None:
            team = mongo.db.get_collection('team').find_one({'_id': ObjectId(id)})
            developers_db = team['developers']
            for dev in developers:
                developers_db.append(dev)
            mongo.db.get_collection('team').update_one({'_id': ObjectId(id)}, {'$set': {
                'developers': developers_db
            }})
        else:
            mongo.db.get_collection('team').update_one({'_id': ObjectId(id)}, {'$set': {
                'developers': developers
            }})
    if projects:
        has_changed = 1
        projects_exists = mongo.db.get_collection('team').find_one({'_id': ObjectId(id), 'projects': {'$exists': True}})
        if projects_exists != None:
            team = mongo.db.get_collection('team').find_one({'_id': ObjectId(id)})
            projects_db = team['projects']
            for project in projects:
                projects_db.append(project)
            mongo.db.get_collection('team').update_one({'_id': ObjectId(id)}, {'$set': {
                'projects': projects_db
            }})
        else:
            mongo.db.get_collection('team').update_one({'_id': ObjectId(id)}, {'$set': {
                'projects': projects
            }})
    if has_changed == 1:
        response = jsonify({'message':'Team ' + id + ' was updated successfully'})
    else: 
        response = jsonify({'message':'No change'})
    return response

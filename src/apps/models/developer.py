from unicodedata import name
from flask import request, jsonify, Response, Blueprint, session
from functools import wraps
from bson import json_util
from bson.objectid import ObjectId
from database.database import mongo
from ..token.token import token_required

developer = Blueprint('developer', __name__)

'''# Decorators
def token_required(f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if 'logged_in' in session:
      return f(*args, **kwargs)
    else:
      return jsonify({'error': 'Authentication required'})
  
  return wrap'''

@developer.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message':'Resouce Not Found: ' + request.url, 
        'status': 404
    })
    response.status_code = 404
    return response

@developer.route('/', methods=['POST'])
@token_required
def create_developer():
    name = request.json.get('name', None)
    email = request.json.get('email', None)
    github = request.json.get('github', None)
    jenkins = request.json.get('jenkins', None)
    jira = request.json.get('jira', None)
    team_id = request.json.get('team_id', None) # Al menos 1 para crear el equipo, tiene que venir como lista

    if name and email and github and jenkins and jira:
        id = mongo.db.get_collection('developer').insert_one(
            {
                'name': name, 
                'email': email, 
                'github': github,
                'jenkins': jenkins,
                'jira': jira,
                'team_id': [team_id]
            }
        )
        response = {
            'name': name, 
            'email': email, 
            'github': github,
            'jenkins': jenkins,
            'jira': jira,
            'team_id': [team_id]
        }

        team = mongo.db.get_collection('team').find_one({'_id': ObjectId(team_id), 'developers': {'$exists': True}})
        developers = []
        if(team != None):
            developers_db = team['developers']
            for dev in developers_db:
                developers.append(dev)
        developers.append(str(id.inserted_id))
        print(developers)
        mongo.db.get_collection('team').update_one({'_id': ObjectId(team_id)}, {'$set': {
            'developers': developers
        }})
        return response
    else:
        print('faltan datos')
        return not_found()

@developer.route('/', methods=['GET'])
@token_required
def get_developers():
    developer = mongo.db.get_collection('developer').find()
    response = json_util.dumps(developer)
    return Response(response, mimetype='application/json')

@developer.route('/<id>', methods=['GET'])
def get_developer_by_id(id):
    # find_one --> el primer dato que coincida
    developer = mongo.db.get_collection('developer').find_one({'_id': ObjectId(id)})
    response = json_util.dumps(developer)
    return Response(response, mimetype='application/json')

@developer.route('/by-team/<id>', methods=['GET'])
@token_required
def get_developer_by_team_id(id):
    team = mongo.db.get_collection('team').find_one({'_id': ObjectId(id)})
    developers = []
    developers_exists = mongo.db.get_collection('team').find_one({'_id': ObjectId(id), 'developers': {'$exists': True}})
    if(team != None and developers_exists != None):
        developers_id = team['developers']
        for dev_id in developers_id:
            dev = mongo.db.get_collection('developer').find_one({'_id': ObjectId(dev_id)})
            developers.append(dev)
    response = json_util.dumps(developers)
    return Response(response, mimetype='application/json')

@developer.route('/<id>', methods=['DELETE'])
def delete_developer(id):
    developer = mongo.db.get_collection('developer').delete_one({'_id': ObjectId(id)})
    response = jsonify({'message':'developer' + id + ' was deleted successfully'})
    return response

@developer.route('/<id>', methods=['PUT'])
def update_developer(id):
    name = request.json.get('name', None)
    email = request.json.get('email', None)
    github = request.json.get('github', None)
    jenkins = request.json.get('jenkins', None)
    jira = request.json.get('jira', None)
    team_id = request.json.get('team_id', None)

    has_changed = 0

    if name:
        has_changed = 1
        mongo.db.get_collection('developer').update_one({'_id': ObjectId(id)}, {'$set': {
            'name': name
        }})
    if email:
        has_changed = 1
        mongo.db.get_collection('developer').update_one({'_id': ObjectId(id)}, {'$set': {
            'email': email
        }})
    if github:
        has_changed = 1
        mongo.db.get_collection('developer').update_one({'_id': ObjectId(id)}, {'$set': {
            'github': github
        }})
    if jenkins:
        has_changed = 1
        mongo.db.get_collection('developer').update_one({'_id': ObjectId(id)}, {'$set': {
            'jenkins': jenkins
        }})
    if jira:
        has_changed = 1
        mongo.db.get_collection('developer').update_one({'_id': ObjectId(id)}, {'$set': {
            'jira': jira
        }})
    if team_id:
        has_changed = 1
        team_id_exists = mongo.db.get_collection('developer').find_one({'_id': ObjectId(id), 'team_id': {'$exists': True}})
        if team_id_exists != None:
            developer = mongo.db.get_collection('developer').find_one({'_id': ObjectId(id)})
            team_id_db = developer['team_id']
            for t in team_id:
                team_id_db.append(t)
            mongo.db.get_collection('developer').update_one({'_id': ObjectId(id)}, {'$set': {
                'team_id': team_id_db
            }})
        else:
            mongo.db.get_collection('developer').update_one({'_id': ObjectId(id)}, {'$set': {
                'team_id': team_id
            }})
    if has_changed == 1:
        response = jsonify({'message':'developer' + id + ' was updated successfully'})
    else: 
        response = jsonify({'message':'No change'})
    return response
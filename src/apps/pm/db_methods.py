if __package__ is None or __package__ == '':
    # uses current directory visibility
    from ...database.database import mongo
else:
    # uses current package visibility
    from database.database import mongo
import pymongo
from bson.objectid import ObjectId

# Se obtienen los registros de un proyecto
def get_registers(team_project_id):
    registers = mongo.db.get_collection('registers').find({'team_project_id': team_project_id}).sort('timestamp', pymongo.ASCENDING)
    return registers


# Se actualiza el path del ultimo modelo de proceso generado para ese proyecto
def update_last_model_path(team_project_id, file_path_bpmn):
    mongo.db.get_collection('team_project').update_one({'_id': ObjectId(team_project_id)}, {'$set': {
        'last_model_path': file_path_bpmn
    }})


# Se obtiene el path del ultimo modelo de proceso generado para ese proyecto
def get_last_team_model_db(team_project_id):
    team = mongo.db.get_collection('team_project').find_one({'_id': ObjectId(team_project_id)})
    path = team['last_model_path']
    return path


# Se obtiene el path del modelo de proceso ideal registrado para el id de un lider de proyectos
def get_ideal(leader_id):
    path_exists = mongo.db.get_collection('users').find_one({'_id': ObjectId(leader_id), 'ideal_model_path': {'$exists': True}})
    if path_exists != None:
        return path_exists['ideal_model_path']
    return None

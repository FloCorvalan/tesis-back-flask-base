if __package__ is None or __package__ == '':
    # uses current directory visibility
    from ...database.database import mongo
else:
    # uses current package visibility
    from database.database import mongo
    #print(__package__)
from bson.objectid import ObjectId


# Obtiene el ultimo bpmn generado para ese id de proyecto
def get_last_bpmn_db(team_project_id):
    res = mongo.db.get_collection('team_project').find_one({'_id': ObjectId(team_project_id)})
    if res != None:
        return res['last_model_path']


# Guarda el modelo de proceso generado para ese proyecto como modelo de proceso ideal para ese lider
# de proyectos
def save_ideal_bpmn_path_db(leader_id, ideal_model_path, filepath):
    path_exists = mongo.db.get_collection('users').update_one({'_id': ObjectId(leader_id)}, {'$set': {
        'ideal_model_path': ideal_model_path, 'ideal_model_path_svg': filepath
    }})


# Obtiene el modelo de proceso ideal
def get_ideal_bpmn_db(leader_id):
    res = mongo.db.get_collection('users').find_one({'_id': ObjectId(leader_id)})
    if res != None:
        return res['ideal_model_path_svg']


# Obtiene la cantidad de veces que se realizaron las actividades en el modelo de proceso
def get_activities_cont_db(team_project_id):
    cont = mongo.db.get_collection('registers').aggregate([
        {
            '$match': {
                'team_project_id': team_project_id,
            }
        },
        {
            '$group': {
                '_id': {
                    'tool': '$tool',
                    'activity': '$activity'
                },
                'count': {'$sum':1}
            }
        },
        {
            '$group': {
                '_id': '$_id.tool',
                'activities': {
                    '$push': {
                        'activity': '$_id.activity',
                        'count': '$count'
                    }
                }
            }
        }
    ])
    return cont

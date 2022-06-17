if __package__ is None or __package__ == '':
    # uses current directory visibility
    from ...database.database import mongo
else:
    # uses current package visibility
    from database.database import mongo
from bson.objectid import ObjectId

# Para obtener la informacion de los proyectos de un equipo de desarrollo
def get_projects_info(team_id):
    info = []
    team = mongo.db.get_collection('team').find_one({'_id': ObjectId(team_id)})
    projects = team['projects']
    dic = {}
    for project in projects:
        team_project = mongo.db.get_collection('team_project').find_one({'_id': ObjectId(project)})
        dic = {
                'id': project,
                'name': team_project['name']
            }
        for source in team_project['sources'].keys():
            dic[source] = team_project['sources'][source]
        info.append(dic)
        dic = {}
    return info
    
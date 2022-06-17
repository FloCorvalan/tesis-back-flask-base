from flask import Blueprint
from .methods import *

pm = Blueprint('pm', __name__)

# Procesa los registros obtenidos desde las distintas herramientas mediante Process Mining
# y genera el modelo de proceso de un equipo de desarrollo
@pm.route('/pm/generate-model/<team_project_id>', methods=['GET'])
def generate_model(team_project_id):
    file_path = process_data(team_project_id)
    return {
        'message': 'Successfully processed data',
        'file_path': file_path
    }

# Obtiene el filepath ultimo modelo de proceso de ese equipo de desarrollo
@pm.route('/pm/get-last-model/<team_project_id>', methods=['GET'])
def get_last_model(team_project_id):
    file_path = get_last_team_model(team_project_id)
    return file_path

from .db_methods import *

# Para obtener la informacion de los proyectos de un equipo de desarrollo
def get_team_projects(team_id):
    projects = get_projects_info(team_id)
    return projects
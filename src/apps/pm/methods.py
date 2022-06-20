from pandas import DataFrame
import pm4py
from pm4py.objects.conversion.log import converter
from pm4py.objects.conversion.process_tree import converter as converter2
import time
import pymongo
from .db_methods import *
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.bpmn import visualizer
import os
from pm4py.algo.conformance.alignments.petri_net import algorithm as alignments

# Procesa los registros para generar un modelo de proceso
def process_data(team_project_id):
    print("ENTRE A PROCESS DATA")
    # Se obtienen los registros y se formatean para poder procesarlos con el algoritmo de pm4py
    registers = get_registers(team_project_id)
    print(registers)
    log = DataFrame(list(registers))
    print(log)
    log.rename(columns={'timestamp': 'time:timestamp', 
    'case_id': 'case:concept:name', 'activity': 'concept:name', 'resource': 'org:resource'}, inplace=True)
    
    # Se genera una red de petri con inductive miner
    net, initial_marking, final_marking = inductive_miner.apply(log, variant=inductive_miner.Variants.IM)
    
    # Se genera un arbol con inductive miner
    process_tree = inductive_miner.apply_tree(log, variant=inductive_miner.Variants.IM)

    # Se convierte a bpmn
    bpmn_graph = converter.apply(process_tree, variant=converter2.Variants.TO_BPMN)
    
    timestr = time.strftime("%Y%m%d")
    pwd = os.getcwd()
    
    # Se definen los nombres de los archivos que se van a guardar
    file_path_svg = pwd + '/static/img/prueba_' + timestr + '_' + team_project_id + '.svg'
    file_path_petri = pwd + '/static/img/prueba_' + timestr + '_' + team_project_id + '.pnml'

    # Se generan y guardan los archivos
    parameters = {visualizer.Variants.CLASSIC.value.Parameters.FORMAT: 'svg'}
    gviz = visualizer.apply(bpmn_graph, parameters=parameters)
    visualizer.save(gviz, file_path_svg)
    pm4py.write_pnml(net, initial_marking, final_marking, file_path_petri)

    # Se guarda el path del ultimo modelo generado
    update_last_model_path(team_project_id, file_path_svg)
    print("VOY A SALIR DE PROCESS DATA")
    return file_path_svg


# Para obtener el nivel de cumplimiento del proceso efectuado realmente respecto a un modelo
# de proceso ideal
def get_fitness(team_project_id, leader_id):
    registers = get_registers(team_project_id)
    log = DataFrame(list(registers))
    log.rename(columns={'timestamp': 'time:timestamp', 
    'case_id': 'case:concept:name', 'activity': 'concept:name', 'resource': 'org:resource'}, inplace=True)

    response = {
        'avg': 0,
        'status': False,
        'result': {}
    }

    result = {}

    file_path_petri = get_ideal(leader_id)
    # Si existe modelo de proceso ideal registrado
    if file_path_petri != None:
        response['status'] = True
        # Se genera una red de petri a partir del archivo pnml con el modelo ideal
        net, initial_marking, final_marking = pm4py.read_pnml(file_path_petri)
        # Se realiza la comparacion de los logs con la red de petri del modelo ideal
        # Se obtiene una lista de instancias del proceso cada una con su nivel de cumplimiento
        replayed_traces = alignments.apply(log, net, initial_marking, final_marking)
        # Se calcula el promedio de nivel de cumplimiento de las instancias del proceso
        i = 0
        while i < len(replayed_traces):
            trace = replayed_traces[i]
            result[str(i)] = int(trace['fitness'] * 100)
            i += 1
        sum = 0
        for key in result.keys():
            sum += result[key]
        avg = int(sum/len(result.keys()))
        response['result'] = result
        response['avg'] = avg
    return response


##############################################################################
##############################################################################
##############################################################################

# Para obtener el ultimo modelo de proceso de un proyecto
def get_last_team_model(team_project_id):
    path = get_last_team_model_db(team_project_id)
    return path

from dyn_rm.mca.base.graph.module.graph_object import MCAGraphObjectModule
from dyn_rm.mca.base.system.module.psets.pset import MCAPSetModule
from dyn_rm.mca.base.system.module.psets.proc import MCAProcModule
from dyn_rm.mca.base.system.module.topology.node import MCANodeModule
from dyn_rm.mca.system.modules.psets.pset_models.amdahl import AmdahlPsetModel
from dyn_rm.mca.mca import MCA
import math
import sys
import time


def get_placeholder(name, gid, cores, executable, status):
    return {"name": str(name), "gid": str(gid), "cores": cores, "exec": executable, "status": status}

def get_delta_add_pset_for_nodes(nodes, task, mapping):
    procs = []
    # fill node
    id = 0
    executable = task.run_service("GET", "TASK_EXECUTABLE")
    status = MCAProcModule.PROC_STATUS_LAUNCH_REQUESTED
    for index in range(len(nodes)):
        cores = nodes[index].run_service("GET", "CORES")
        if mapping == 'dense':
            for core in cores:
                procs.append(get_placeholder(str(id), str(id), [core], executable, status))
                id += 1
                #proc = MCAProcModule(str(index), task.run_service("GET", "TASK_EXECUTABLE"))
                #proc.run_service("SET", "CORE_ACCESS", [core])
                #proc.run_service("SET", "PROC_STATUS", MCAProcModule.PROC_STATUS_LAUNCH_REQUESTED)
                #procs.append(proc)
        elif mapping == 'sparse':
            procs.append(get_placeholder(str(id), str(id), cores, executable, status))
            id += 1
            #proc = MCAProcModule(str(index), task.run_service("GET", "TASK_EXECUTABLE"))
            #proc.run_service("SET", "CORE_ACCESS", cores)
        else:
            procs.append(get_placeholder(str(id), str(id), cores, executable, status))
            id += 1
            #proc = MCAProcModule(str(index), task.run_service("GET", "TASK_EXECUTABLE"))
            #proc.run_service("SET", "CORE_ACCESS", cores)
        
    if len(procs) == 0:
        return None, []
    
    delta_pset = MCAPSetModule("delta_add", procs)
    delta_pset.run_service("SET", "TASK", task)
    return delta_pset, procs

def get_delta_sub_pset_for_nodes(nodes, task, pset):
    delta_procs = []
    proc_node_mapping = dict()
    procs = pset.run_service("GET", "PROCS")
    for proc in procs:
        if proc.run_service("GET", "STATUS") != MCAGraphObjectModule.STATUS_VALID:
            continue
        cores = proc.run_service("GET", "CORE_ACCESS")
        if len(cores) > 0:
            node = cores[0].run_service("GET", "NODE")
            if node not in proc_node_mapping:
                proc_node_mapping[node] = []
            proc_node_mapping[node].append(proc)
    
    executable = task.run_service("GET", "TASK_EXECUTABLE")
    status = MCAProcModule.PROC_STATUS_TERMINATION_REQUESTED
    for node in nodes:
        if node in proc_node_mapping.keys():
            for old_proc in proc_node_mapping[node]:
                id = old_proc.run_service("GET", "GID")
                delta_procs.append(get_placeholder(str(id), str(id), cores, executable, status))
                #delta_proc = MCAProcModule("", "")
                #delta_proc = old_proc.run_service("GET", "COPY", delta_proc)
                #delta_proc.run_service("SET", "PROC_STATUS", MCAProcModule.PROC_STATUS_TERMINATION_REQUESTED)
                #delta_procs.append(delta_proc)
    
    if len(delta_procs) == 0:
        return None, []
    
    delta_pset = MCAPSetModule("delta_sub", delta_procs)
    delta_pset.run_service("SET", "TASK", task)
    return delta_pset, delta_procs

def get_grow_pset(input, delta_add, task, model, params):
    procs = input.run_service("GET", "PROCS") + delta_add.run_service("GET", "PROCS")
    if len(procs) == 0:
        return None, []

    if model == None:
        pset_model = input.run_service("GET", "PSET_MODEL", "USER_MODEL")
    else:
        pset_model = model()
    
    pset_model.run_service("SET", "MODEL_PARAMS", params)
    
    grow_pset = MCAPSetModule("replace_pset", procs)
    grow_pset.run_service("ADD", "PSET_MODEL", "USER_MODEL", pset_model)
    grow_pset.run_service("SET", "TASK", task)
    return grow_pset, procs

def get_replace_pset(input, delta_add, delta_sub, task, model, params):
    sub_proc_ids = [proc["gid"] for proc in delta_sub.run_service("GET", "PROCS")]
    procs = [proc for proc in input.run_service("GET", "PROCS") if proc.run_service("GET", "GID") not in sub_proc_ids] + delta_add.run_service("GET", "PROCS")
    if len(procs) == 0:
        return None, []

    if model == None:
        replace_model = input.run_service("GET", "PSET_MODEL", "USER_MODEL")
    else:
        replace_model = model()
    
    replace_model.run_service("SET", "MODEL_PARAMS", params)
    
    replace_pset = MCAPSetModule("replace_pset", procs)
    replace_pset.run_service("ADD", "PSET_MODEL", "USER_MODEL", replace_model)
    replace_pset.run_service("SET", "TASK", task)
    return replace_pset, procs



def output_space_generator_launch(setop, 
                                  input, 
                                  graphs, 
                                  task = None, 
                                  model = AmdahlPsetModel, 
                                  model_params = {'t_s' : 0, 't_p' : 1}, 
                                  num_delta = -1, 
                                  multiple_of_two = False, 
                                  mapping = 'dense'):

    topology_graph_sub = graphs["TOPOLOGY_GRAPH_SUB"]
    if len(topology_graph_sub.run_service("GET", "TOPOLOGY_OBJECTS", MCANodeModule)) > 0:
        return [], []

    topology_graph = graphs["TOPOLOGY_GRAPH_ADD"]
    nodes = topology_graph.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCANodeModule))

    delta_pset_add, procs = get_delta_add_pset_for_nodes(nodes, task, mapping)

    # Fixed number of procs to start with
    if num_delta > - 1 and len(procs) != num_delta:
        #print("===> Fixed number of procs constraint not satisfied ", num_delta, " vs. ", len(procs))
        return [], []
    
    # multiple of 2 constraint
    if multiple_of_two:
        if (len(procs) & (len(procs) - 1)) != 0:
            #print("===> Multiple of 2 constraint not satisfied: "+str(len(nodes)))
            return [], []


    pset_model = model()
    pset_model.run_service("SET", "MODEL_PARAMS", model_params)
    delta_pset_add.run_service("ADD", "PSET_MODEL", "USER_MODEL", pset_model)

    #print("LAUNCH OUPUT SPACE GENERATED for task " + task.run_service("GET", "NAME"))

    # Note: Lists of Lists => For each possibility return: output_lists and lists_of_adapted_objects 
    return [[delta_pset_add]], [[delta_pset_add] + procs]



def output_space_generator_replace(setop, 
                                   input, 
                                   graphs, 
                                   task=None, 
                                   model=None, 
                                   model_params = dict(), 
                                   num_delta_add=-1, 
                                   num_delta_sub=-1,
                                   num_max = sys.maxsize,
                                   num_min = 1,
                                   multiple_of_two=False, 
                                   factor=-1,
                                   mapping='dense'):

    pset_graph = graphs["PSET_GRAPH"]
    topology_graph_add = graphs["TOPOLOGY_GRAPH_ADD"]
    topology_graph_sub = graphs["TOPOLOGY_GRAPH_SUB"]
    
    nodes_add = topology_graph_add.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCANodeModule))
    nodes_sub = topology_graph_sub.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCANodeModule))

    # Get the associated task
    if task == None:
        task = input[0].run_service("GET", "TASK")

    # do an early check for num_delta_add && num_delta_sub
    num_procs_add = len(nodes_add) if mapping == 'sparse' else sum([n.run_service("GET", "NUM_CORES") for n in nodes_add])
    num_procs_sub = len(nodes_sub) if mapping == 'sparse' else sum([n.run_service("GET", "NUM_CORES") for n in nodes_sub])

    cur_size = input[0].run_service("GET", "NUM_PROCS")

    new_size = cur_size + num_procs_add - num_procs_sub


    if num_delta_add == "DOUBLE":
        num_delta_add = cur_size
    elif num_delta_add == "DOUBLE_REVERSE":
        num_delta_add = min (num_max/2, (num_max - cur_size + num_min)/2)

    if num_delta_sub == "HALF":
        num_delta_sub = cur_size / 2
    elif num_delta_sub == "HALF_REVERSE":
        num_delta_sub = num_max - (cur_size - num_min)

    # min constraint
    if new_size < num_min:
        return [], []

    # max constraint
    if new_size > num_max:
        return [], []

    # fixed delta constraints
    if num_delta_add > -1 and num_procs_add != num_delta_add:
        #print("===> Fixed nodes constraint not satisfied for add")
        return [], []

    if num_delta_sub > -1 and num_procs_sub != num_delta_sub:
        #print("===> Fixed nodes constraint not satisfied for sub")
        return [], []

    # multiple of constraint
    if multiple_of_two:
        if (new_size & (new_size - 1)) != 0:
            #print("===> Multiple of 2 constraint not satisfied: "+str(len(replace_procs)))
            return [], []

    if factor > - 1:
        if cur_size * factor != new_size:
            return [], []



    delta_pset_add, delta_add_procs = get_delta_add_pset_for_nodes(nodes_add, task, mapping)
    if None == delta_pset_add:
        delta_pset_add = pset_graph


    delta_pset_sub, delta_sub_procs = get_delta_sub_pset_for_nodes(nodes_sub, task, input[0])
    if None == delta_pset_sub:
        delta_pset_sub = pset_graph

    replace_pset, replace_procs = get_replace_pset(input[0], delta_pset_add, delta_pset_sub, task, model, model_params)
    if None == replace_pset:
        replace_pset = pset_graph


    if replace_pset == pset_graph or (delta_pset_sub == pset_graph and delta_pset_add == pset_graph):
        return [], []  


    #print("REPLACE OUPUT SPACE GENERATED for task " + task.run_service("GET", "NAME"))

    # Note: Lists of Lists => For each possibility return: output_lists and lists_of_adapted_objects 
    return [[delta_pset_sub, delta_pset_add, replace_pset]], [[delta_pset_add, delta_pset_sub, replace_pset] + delta_add_procs+ delta_sub_procs]



def output_space_generator_grow(setop, 
                                   input, 
                                   graphs, 
                                   task=None, 
                                   model=None, 
                                   model_params = dict(), 
                                   num_delta_add=-1, 
                                   num_delta_sub=-1,
                                   num_max = sys.maxsize,
                                   num_min = 1,
                                   multiple_of_two=False, 
                                   factor=-1,
                                   mapping='dense'):

    pset_graph = graphs["PSET_GRAPH"]
    topology_graph_add = graphs["TOPOLOGY_GRAPH_ADD"]
    topology_graph_sub = graphs["TOPOLOGY_GRAPH_SUB"]
    
    nodes_add = topology_graph_add.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCANodeModule))
    nodes_sub = topology_graph_sub.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCANodeModule))

    # Get the associated task
    if task == None:
        task = input[0].run_service("GET", "TASK")

    # do an early check for num_delta_add && num_delta_sub
    num_procs_add = len(nodes_add) if mapping == 'sparse' else sum([n.run_service("GET", "NUM_CORES") for n in nodes_add])

    cur_size = input[0].run_service("GET", "NUM_PROCS")

    new_size = cur_size + num_procs_add


    if num_delta_add == "DOUBLE":
        num_delta_add = cur_size
    elif num_delta_add == "DOUBLE_REVERSE":
        num_delta_add = min (num_max/2, (num_max - cur_size + num_min)/2)


    # min constraint
    if new_size < num_min:
        return [], []

    # max constraint
    if new_size > num_max:
        return [], []

    # fixed delta constraints
    if num_delta_add > -1 and num_procs_add != num_delta_add:
        #print("===> Fixed nodes constraint not satisfied for add")
        return [], []

    # multiple of constraint
    if multiple_of_two:
        if (new_size & (new_size - 1)) != 0:
            #print("===> Multiple of 2 constraint not satisfied: "+str(len(replace_procs)))
            return [], []

    if factor > - 1:
        if cur_size * factor != new_size:
            return [], []


    delta_pset_add, delta_add_procs = get_delta_add_pset_for_nodes(nodes_add, task, mapping)
    if None == delta_pset_add:
        delta_pset_add = pset_graph

    grow_pset, grow_procs = get_grow_pset(input[0], delta_pset_add, task, model, model_params)
    if None == grow_pset:
        grow_pset = pset_graph


    if grow_pset == pset_graph or delta_pset_add == pset_graph:
        return [], []  
    
    return [[delta_pset_add, grow_pset]], [[delta_pset_add, grow_pset] + delta_add_procs]


def output_space_generator_sub(setop, 
                                   input, 
                                   graphs, 
                                   task=None, 
                                   model=None, 
                                   model_params = dict(), 
                                   num_delta_add=-1, 
                                   num_delta_sub=-1,
                                   multiple_of_two=False, 
                                   factor=-1,
                                   mapping='dense'):

    pset_graph = graphs["PSET_GRAPH"]
    topology_graph_add = graphs["TOPOLOGY_GRAPH_ADD"]
    topology_graph_sub = graphs["TOPOLOGY_GRAPH_SUB"]
    
    nodes_add = topology_graph_add.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCANodeModule))
    nodes_sub = topology_graph_sub.run_service("GET", "GRAPH_VERTICES_BY_FILTER", lambda x: isinstance(x, MCANodeModule))

    if nodes_add > 0:
        return [], []
    
    cur_nodes = input[0].run_service("GET", "ACCESSED_NODES")

    if set([n.run_service("GET", "GID") for n in cur_nodes]) != set([n.run_service("GET", "GID") for n in nodes_sub]):
        return [],[]
       
    return [[pset_graph]], [[]]
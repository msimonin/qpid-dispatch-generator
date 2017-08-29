from itertools import groupby
import networkx as nx
import json
import os

SIZE = 5
MACHINES = 1
GEN_PATH = 'generated'

# logical graph of qdrouterd
# TODO: specify it through the cli
#graph = nx.complete_graph(SIZE)
graph = nx.nx.tutte_graph()

# physqical machine
# TODO: specify it through the cli
machines = ["machine%s" % m for m in range(MACHINES)]

# one dummy way of mapping qdrouterd to machines
# Round Robin for now
def distribute(graph, machines):
    ## RR fashion
    nodes_to_machines = {}
    machines_to_nodes = {}
    i = 0
    for node in graph.nodes():
        nodes_to_machines.update({node: machines[i]})
        machines_to_nodes.setdefault(machines[i], [])
        machines_to_nodes[machines[i]].append(node)
        i = (i + 1) % len(machines)
    return nodes_to_machines, machines_to_nodes

# distribute router to machines
ntm, mtn = distribute(graph, machines)

# Build the main configuration parameter of each qdrouterd
# It takes into account
#  - the logical graph to generate the listener/connectors
#  - the mapping to physical ressources to avoid port conflicts
confs = {}
router_idx = 0
for node, nbrdict in graph.adjacency_iter():
    confs.setdefault(node, {})
    machine = ntm[node]
    idx = mtn[machine].index(node)
    router_id = "router%s" % router_idx
    confs[node].update({
        'machine': machine,
        'router_id': router_id})
    confs[node].update({
            'listeners': [{'host': '0.0.0.0',
			    'port': 6000 + idx,
			    'role': 'inter-router'},
			  {
			    'host': '0.0.0.0',
			    'port': 5000 + idx,
			    'role': 'normal',
                            # use an extra field for the remaining options
			    'authenticatePeer': 'no',
			    'saslMechanisms': 'ANONYMOUS'}]})
    # outgoing links
    connectors = []
    for out in nbrdict.keys():
        out_machine = ntm[out]
        out_idx = mtn[out_machine].index(out)
        connectors.append({
            'host': out_machine,
            'port': 6000 + out_idx, # same rule as above
            'role': 'inter-router'
        })
    confs[node].update({'connectors': connectors})
    router_idx = router_idx + 1

# Dumping all the confs
basename = "complete_%s_%s" % (SIZE, MACHINES)
directory = os.path.join(GEN_PATH, basename)
if not os.path.isdir(directory):
    os.makedirs(directory)
filename = os.path.join(directory, "confs.json")
with open(filename, 'w') as f:
    f.write(json.dumps({'confs': confs.values()}))

from qpid_generator import networkx as qnx
from qpid_generator.distribute import round_robin
from qpid_generator.configurations import get_conf

import json
import os

GEN_PATH = 'generated'

# inputs
graph_type = 'complete_graph'
args = [5]
machines = 2

# machinery
graph = qnx.call(graph_type, *args)
machines = ["machine%s" % m for m in range(machines)]
confs = get_conf(graph, machines, round_robin)

print(confs)
# output
params = "-".join([str(x) for x in args])
basename = "%s_%s_on_%s" % (graph_type, params, len(machines))
directory = os.path.join(GEN_PATH, basename)
if not os.path.isdir(directory):
    os.makedirs(directory)
filename = os.path.join(directory, "confs.json")
with open(filename, 'w') as f:
    f.write(json.dumps({'confs': confs.values()}))

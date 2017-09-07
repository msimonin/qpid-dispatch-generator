from qpid_generator import networkx as qnx
from qpid_generator.distribute import round_robin
from qpid_generator.configurations import get_conf

import json
import os

from qpid_generator.parser import Config

GEN_PATH = 'generated'

config = Config()
config.parse_args()
config.parse_inventory()

# inputs
graph_type = 'complete_graph'
args = [config.routers]
machines = config.machines

# machinery
graph = qnx.call(graph_type, *args)
machines = ["machine%s" % m for m in range(machines)]
confs = get_conf(graph, machines, round_robin)

# output
params = "-".join([str(x) for x in args])
basename = "%s_%s_on_%s" % (graph_type, params, len(machines))
directory = os.path.join(GEN_PATH, basename)
if not os.path.isdir(directory):
    os.makedirs(directory)
filename = os.path.join(directory, "confs.json")
with open(filename, 'w') as f:
    f.write(json.dumps({'confs': confs.values()}))

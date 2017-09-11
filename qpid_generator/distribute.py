#!/usr/bin/env python
# -*- coding: utf-8 -*-


# one dummy way of mapping qdrouterd to machines
# Round Robin for now
def round_robin(graph, machines):
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



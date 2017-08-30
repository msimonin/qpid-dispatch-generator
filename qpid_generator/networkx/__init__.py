import networkx as nx

def call(func_name, *args):
    return getattr(nx, func_name)(*args)

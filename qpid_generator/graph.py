# -*- coding: utf-8 -*-

import networkx as nx

def generate(func_name, *args):
    return getattr(nx, func_name)(*args)

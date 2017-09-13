#!/usr/bin/env python
# -*- coding: utf-8 -*-


import networkx as nx

def call(func_name, *args):
    return getattr(nx, func_name)(*args)
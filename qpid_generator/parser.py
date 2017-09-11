#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import re
import yaml


class Config:
    def __init__(self):
        self.path_inventory = '~/inventory'
        self.machines = 2
        self.routers = 1
        self.brokers = 1
        self.router_names = []
        self.broker_names = []


    def parse_args(self):
        # parse arguments
        parser = argparse.ArgumentParser(description='Qpid-dispatch facts generator.')
        required = parser.add_argument_group('required arguments')
        required.add_argument('-c', '--config-file', action="store", dest="config_file", help='Path to config file',
                              required=True)

        results = parser.parse_args()

        with open(results.config_file, 'r') as stream:
            try:
                config = yaml.load(stream)
                self.path_inventory = config['hostfile']
            except yaml.YAMLError as exc:
                print(exc)

    def parse_inventory(self):
        group = 'none'
        with open(self.path_inventory, 'r') as f:
            try:
                read_data = f.read()
            except IOError as exc:
                print(exc)

        f.closed

        for line in read_data.splitlines():
            if re.match('\[routers\].*', line) != None:
                group = 'routers'
            elif re.match('\[brokers\].*', line):
                group = 'brokers'
            elif re.match('^\s*$', line):
                group = 'none'

            val = re.match('(\S+) .*', line)

            if group is 'routers' and val:
                self.router_names.append(val.group(1))
            elif group is 'brokers' and val:
                self.broker_names.append(val.group(1))

        self.routers = len(self.router_names)
        self.brokers = len(self.broker_names)

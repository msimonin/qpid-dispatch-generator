# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""

from setuptools import setup
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session='hack')

# reqs is a list of requirement
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name='qpid_generator',
    version='0.1.1',
    packages=['qpid_generator'],
    entry_points={
        "console_scripts": ['qpid_generator = qpid_generator.qpid_generator:main']
    },
    license='Apache 2.0',
    description='',
    long_description=open('README.md').read(),
    install_requires=reqs,
    url='https://github.com/rh-messaging-qe/qpid_generator',
    author='Dominik Lenoch <dlenoch@redhat.com>, Jakub Stejskal <jstejska@redhat.com>'
)

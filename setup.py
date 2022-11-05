#!/usr/bin/env python3

'''Ejemplo de API REST para ADI'''

from setuptools import setup

setup(
    name='restdir',
    version='0.1',
    description=__doc__,
    packages=['restdir', 'restdir_scripts'],
    entry_points={
        'console_scripts': [
            'restdir_server=restdir_scripts.server:main',
            'restdir_client=restdir_scripts.client:main'
        ]
    }
)
#!/usr/bin/env python

"""Setup script for Chess."""

import setuptools

from chess import __project__, __version__

import os
if os.path.exists('README.rst'):
    README = open('README.rst').read()
else:
    README = ""  # a placeholder, readme is generated on release
CHANGES = open('CHANGES.md').read()


setuptools.setup(
    name=__project__,
    version=__version__,

    description="Chess is a Python 2 and 3 package template.",
    url='https://github.com/theovoss/chess',
    author='Theo Voss',
    author_email='theo.voss973@gmail.com',

    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['chess/*', 'chess/chess_game.json']},

    entry_points={'console_scripts': []},

    long_description=(README + '\n' + CHANGES),
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=[]
)

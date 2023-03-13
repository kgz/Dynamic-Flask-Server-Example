import importlib
import os
import pathlib
from importlib import import_module
from inspect import getmembers, isfunction
from os import listdir
from os.path import isfile, join

from flask import jsonify

path = pathlib.Path(__file__).parent.resolve()
ogpath = os.getcwd()
path = pathlib.Path(__file__).parent.resolve()
os.chdir(path)

files = [f for f in listdir(path) if isfile(join(path, f))]
files = [f for f in files if not f.startswith("__")]

from .wrapper import api_list

for x in files:
    import_module("Api." + x[:-3])

os.chdir(ogpath)
#!/usr/bin/python3
"""
Script to setup env and run a development server for app
Does the following:
- setup sys path to libraries included
- change dir to src
- execvpe sys.argv[1] with parameters passed and default environ
"""
import os
from os.path import join, dirname, abspath
import sys
import site
paths = []

base_path = abspath(join(dirname(__file__), ".."))
src_path = join(base_path, "src")
lib_path = join(base_path, "lib")
paths.append(src_path)
sys.path.extend(paths)
site.addsitedir(lib_path)
os.chdir(src_path)
environ = {}
environ['PYTHONPATH'] = ":".join(sys.path)
environ.update(os.environ)
os.execvpe("python3", sys.argv[0:], environ)

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
import importlib
module = importlib.import_module('%s.application'% sys.argv[1])
sys.argv = sys.argv[1:]
module.main()
#os.execvp("python3", sys.argv[0:])#, os.environ)

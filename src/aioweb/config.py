import os
from os.path import dirname, join
import logging
import configparser
config = None


def set_config(basepath, configfile='development'):
    global config
    default_config_path = join(dirname(__file__), "conf", "default.ini")
    config = configparser.ConfigParser()
    configpath = join(basepath, 'conf', "%s.ini" % configfile)
    logging.debug("Reading config from: %s" % configpath)
    config.read(default_config_path)
    config.read(configpath)
    return config
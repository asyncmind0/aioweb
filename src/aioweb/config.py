import os
from os.path import dirname, join
import logging
import logging.config
import configparser
import json
from .util import deep_update
config = None
configpath = None
default_config_path = join(dirname(__file__), "conf", "default.ini")
default_logging_config_path = join(dirname(__file__), "conf", "logging.json")
logger = logging.getLogger("config")


def set_config(basepath, configfile='development'):
    global config
    global configpath
    config = configparser.ConfigParser()
    configpath = join(basepath, 'conf', "%s.ini" % configfile)
    logger.debug("Reading config from: %s" % configpath)
    config.read(default_config_path)
    config.read(configpath)
    return config


def configure_logging(basepath, configfile="logging"):
    """Load logging config from json string textfile.
    """
    logging_config_path = join(basepath, 'conf', "%s.json" % configfile)
    appconfig = {}
    with open(default_logging_config_path, 'r') as config:
        defaultconfig = json.loads(config.read())
    try:
        with open(logging_config_path, 'r') as config:
            appconfig = json.loads(config.read())
    except Exception as e:
        logging.info("Falling back to default logging config.")
    deep_update(appconfig, defaultconfig)
    print(appconfig)
    logging.config.dictConfig(appconfig)
    return appconfig

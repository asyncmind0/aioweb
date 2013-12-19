import os
import logging
import configparser
config = None


def set_config(configfile='development'):
    global config
    config = configparser.ConfigParser()
    configpath = os.path.join('conf', "%s.ini" % configfile)
    logging.debug("Reading config from: %s" % configpath)
    config.read(configpath)
    return config
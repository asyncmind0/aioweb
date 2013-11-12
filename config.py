import os
import logging
import configparser
config = configparser.ConfigParser()
configpath = os.path.join( 'conf', 'development.ini')
logging.debug("Reading config from: %s" % configpath)
config.read(configpath)
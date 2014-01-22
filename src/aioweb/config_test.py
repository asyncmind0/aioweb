import json
from os.path import join, dirname
from .config import configure_logging

default_test_config_path = join(dirname(__file__), "conf", "logging_test.json")


def test_configure_logging():
    configdict = {
        'version': 1,
        'disable_existing_loggers': False,
        'incremental': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'loggers': {
            'config': {
                'handlers': ['console'],
                'level': 'WARN',
                'propagate': False
            },
            'CouchDBAdapter': {
                'handlers': ['console'],
                'level': 'WARN',
                'propagate': False
            },
        }
    }
    with open(default_test_config_path, 'w+') as config:
        config.write(json.dumps(configdict, indent=4))
    c = configure_logging(dirname(__file__), configfile="logging_test")
    print(c)

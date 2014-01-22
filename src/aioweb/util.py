import logging
from IPython.core import ultratb
import collections


class AioWebLogFormatter(logging.Formatter):
    """ Pretty formatter for logging
    http://nbviewer.ipython.org/gist/minrk/8330041
    """
    def __init__(self, *args, **kwargs):
        super(AioWebLogFormatter, self).__init__(*args, **kwargs)
        self.ftb = ultratb.FormattedTB()

    def formatException(self, exc_info):
        etype, evalue, etb = exc_info
        tblist = self.ftb.structured_traceback(etype, evalue, etb)
        return '\n'.join(tblist)


def deep_update(d, u):
    """http://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
    """
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            r = deep_update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d
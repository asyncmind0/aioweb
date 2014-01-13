import logging
import sys
from IPython.core import ultratb


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

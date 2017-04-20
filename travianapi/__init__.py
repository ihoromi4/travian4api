import os
import logging

logger = logging.getLogger(__name__)

__tuple_version__ = (0, 1, 0)
__version__ = '.'.join((str(i) for i in __tuple_version__))

logger.debug('Travian Legends API version: ' + __version__)

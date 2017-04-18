import os
import logging

__tuple_version__ = (0, 1, 0)
__version__ = '.'.join((str(i) for i in __tuple_version__))

if not os.path.isdir('log'):
    os.makedirs('log')

logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG),
                    #filename='log/log.log')

logging.debug('Travian Legends API version: ' + __version__)

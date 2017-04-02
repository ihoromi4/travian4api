import os
import logging


if not os.path.isdir('log'):
    os.makedirs('log')

logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG),
                    #filename='log/log.log')

logging.debug('Start logging')

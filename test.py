import logging

logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

import travian4api
from travian4api import account

url = travian4api.servers.TS6_RU
username = 'broo'
password = '1234qwer'

acc = account.Account(url, username, password)

v = acc.villages[0]
print(v.outer.buildings)

mp = v.get_building_by_repr('marketplace')
print(mp.get_exchange_page())

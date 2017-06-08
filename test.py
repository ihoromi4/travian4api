import logging

logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG)

import travian4api

url = travian4api.servers.TS6_RU
username = 'broo'
password = '1234qwer'

account = travian4api.Account(url, username, password)

print(account.alliance)

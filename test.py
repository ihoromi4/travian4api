from travianapi import account

url = 'http://ts5.travian.ru/'
username = 'broo'
password = 'wA4iN_tYR'

acc = account.Account(url, username, password)

v = acc.villages[0]
print(v.outer.buildings)

mp = v.get_building_by_repr('marketplace')
print(mp.get_exchange_page())

import os
import sys

import unittest

os.chdir('..')
newwd = os.getcwd()
sys.path.append(newwd)

from travlib import login
# from travlib import account


class TestLogin(unittest.TestCase):
    def test_1(self):
        server_url = 'http://ts5.travian.ru'
        name = 'broo'
        password = '1994igor'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0'}
        login_ = login.Login(server_url, name, password, headers)

        self.assertEqual(login_.server_url, server_url)
        self.assertEqual(login_.name, name)
        self.assertEqual(login_.password, password)
        self.assertEqual(login_.headers, headers)

unittest.main()

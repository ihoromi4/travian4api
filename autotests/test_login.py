import os
import sys

import unittest

from travianapi import login


class TestLogin(unittest.TestCase):
    def __init__(self, data):
        unittest.TestCase.__init__(self)

        self.data = data

    def runTest(self):
        url = self.data['url']
        name = self.data['username']
        password = self.data['password']

        login_ = login.Login(url, name, password)

        login_.login()

        self.assertEqual(login_.url, url)
        self.assertEqual(login_.name, name)
        self.assertEqual(login_.password, password)

if __name__ == '__main__':
    unittest.main()

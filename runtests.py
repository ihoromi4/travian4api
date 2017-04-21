import unittest

from autotests import test_login

data = {
    'url': 'http://ts4.travian.com/',
    'username': 'bro',
    'password': '1994igor'
}

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(test_login.TestLogin(data))

    runner = unittest.TextTestRunner()
    runner.run(suite)

    #unittest.main()

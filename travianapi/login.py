import logging
import time

import requests
import bs4

from .exceptions import LoginError
from . import language
from .travparse import dorf1


class Login:
    def __init__(self, url, name, password, headers={}, lang_dir='data/language/'):
        self.url = url
        self.name = name
        self.password = password
        self.__headers = headers

        self.session = None
        self.new_session()

        self.timeout = 5.0
        self.relogin_delay = 0.33
        self.reconnections = 3
        self.html_obsolescence_time = 1.0
        self.loggedin = False
        self.ajax_token = None
        self.html_sources = dict()

        self.__server_language = None
        self.__game_version = None
        self.language = language.Language("{}{}.json".format(lang_dir, self.server_language))

    def new_session(self):
        if self.session:
            self.session.close()
        self.session = requests.Session()
        self.session.headers = self.__headers

    def get_headers(self):
        return self.__headers

    def set_headers(self, headers):
        self.__headers = headers
        self.session.headers = headers
    headers = property(get_headers, set_headers)

    def get(self, url, data={}, params={}):
        MAXTRIES = 2
        response = None
        for attempt in range(1, MAXTRIES + 1):
            try:
                logging.debug('Send get request to url: {}'.format(url))
                response = self.session.get(url, params=params, timeout=self.timeout)
                break
            except requests.exceptions.ConnectionError:
                print('Attempt %s of %s' % (attempt, MAXTRIES))
                self.new_session()
                self.login()
            except requests.exceptions.ReadTimeout:
                print('Attempt %s of %s' % (attempt, MAXTRIES))
                self.new_session()
                self.login()
            except:
                raise
        if response:
            status_code = response.status_code
            if hasattr(response, 'is_redirect'):
                is_redirect = response.is_redirect
            else:
                is_redirect = None
            logging.debug('Response: status_code: {}, is_redirect {}'.format(status_code, is_redirect))
        else:
            raise ValueError('response must be not None')
        return response

    def post(self, url, data={}, params={}):
        MAXTRIES = 2
        response = None
        for attempt in range(1, MAXTRIES + 1):
            try:
                logging.debug('Send post request to url: {}'.format(url))
                response = self.session.post(url, params=params, data=data, timeout=self.timeout)
                break
            except requests.exceptions.ConnectionError:
                print('Attempt %s of %s' % (attempt, MAXTRIES))
                self.new_session()
                self.login()
            except requests.exceptions.ReadTimeout:
                print('Attempt %s of %s' % (attempt, MAXTRIES))
                self.new_session()
                self.login()
            except:
                logging.error('Net problem, cant fetch the URL {}'.format(url))
                raise
        if response:
            status_code = response.status_code
            if hasattr(response, 'is_redirect'):
                is_redirect = response.is_redirect
            else:
                is_redirect = None
            logging.debug('Response: status_code: {}, is_redirect {}'.format(status_code, is_redirect))
        else:
            raise ValueError('response must be not None')
        return response

    def send_request(self, url, data={}, params={}):
        if not len(data):
            response = self.get(url, data=data, params=params)
        else:
            response = self.post(url, data=data, params=params)
        return response

    def server_get(self, url, data={}, params={}):
        return self.get(self.url + url, data, params).text

    def server_post(self, url, data={}, params={}):
        return self.post(self.url + url, data, params).text

    def server_get_request(self, url, data={}, params={}, *args, **kwargs):
        return self.get(self.url + url, data, params, *args, **kwargs)

    def server_post_request(self, url, data={}, params={}, *args, **kwargs):
        return self.post(self.url + url, data, params, *args, **kwargs)

    def login(self):
        logging.debug('Start Login')
        response = self.session.get(self.url)
        if response.status_code != 200:
            return False
        html = response.text
        # start parse
        parser = bs4.BeautifulSoup(html, 'html5lib')
        s1 = parser.find('button', {'name': 's1'})['value'].encode('utf-8')
        login = parser.find('input', {'name': 'login'})['value']
        # start login
        data = {
            'name': self.name,
            'password': self.password,
            's1': s1,
            'w': '1366:768',
            'login': login
            }
        response = self.session.post(self.url + 'dorf1.php', data=data)
        if response.status_code != 200:
            return False
        html = response.text
        if 'playerName' in html:
            self.loggedin = True
            self.ajax_token = dorf1.parse_ajax_token(html)
            logging.debug('Login succeed')
            return True
        self.loggedin = False
        logging.debug('Login fail')
        return False

    def load_html(self, url, params={}, data={}):
        if not self.loggedin:
            if not self.login():
                logging.debug('Can\'t login. Something is wrong.')
                raise LoginError('Can\'t login. Something is wrong.')
        html = self.send_request(url, data=data, params=params).text
        if 'playerName' not in html:
            self.loggedin = False
            logging.debug('Suddenly logged off')
            for i in range(self.reconnections):
                if self.login():
                    html = self.send_request(url, data=data, params=params).text
                    return html
                else:
                    logging.debug('Could not relogin %d time' % (self.reconnections-i))
                    time.sleep(self.relogin_delay)
        return html

    def get_ajax(self, params: dict={}, data: dict={}) -> str:
        """ Выполняет ajax запрос и возвращает результат """
        last_url = 'ajax.php'  # Адрес для ajax запросов постоянный
        url = self.url + last_url
        data['ajaxToken'] = self.ajax_token  # В данных должен быть ajax_token, добавляем.
        response = self.post(url, data=data, params=params)  # Нужен именно post запрос
        html = response.text
        return html

    def get_html(self, last_url, params={}, data={}):
        url = self.url + last_url
        key = (url, hash(tuple(sorted(params.items()))))
        if key in self.html_sources:
            html, load_time = self.html_sources[key]
            if time.time() - load_time < self.html_obsolescence_time:
                print("{} : no obsolescence html".format(url))
                return html
        load_time = time.time()
        html = self.load_html(url, params=params, data=data)
        self.html_sources[key] = (html, load_time)
        return html

    def load_dorf1(self, village_id):
        return self.get_html('dorf1.php?newdid={}&'.format(village_id))

    def load_dorf2(self, village_id):
        return self.get_html('dorf2.php?newdid={}&'.format(village_id))

    def get_game_version(self):
        if not self.__game_version:
            html = self.get_html('dorf1.php')
            game_version = dorf1.parse_game_version(html)
            self.__game_version = game_version
        return self.__game_version
    game_version = property(get_game_version)

    def get_server_language(self):
        if not self.__server_language:
            html = self.get_html('dorf1.php')
            self.__server_language = dorf1.parse_server_language(html)
        return self.__server_language
    server_language = property(get_server_language)

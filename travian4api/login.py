import logging
import time
from urllib import parse

import requests
import bs4

from .exceptions import LoginError
from . import language
from .travparse import dorf1

logger = logging.getLogger(__name__)

BASE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

REQUEST_MAX_TRIES = 2


class Login:
    """ Класс реализует подключение к серверу и вход в аккаунт """

    def __init__(self, url, name, password, headers=None):
        self.url = self.verify_url(url)
        self.name = name
        self.password = password

        if not headers:
            headers = BASE_HEADERS

        self.__headers = headers

        self.session = self.new_session()

        self.timeout = 5.0
        self.relogin_delay = 0.33
        self.reconnections = 3
        self.html_obsolescence_time = 1.0
        self.loggedin = False
        self.ajax_token = None
        self.html_sources = dict()

        self.__server_language = None
        self.__game_version = None

    def verify_url(self, url: str):
        if not type(url) is str:
            raise TypeError()

        if not url:
            raise ValueError()

        result = parse.urlparse(url)
        url = parse.urljoin('http://' + (result.netloc or result.path), '')
        result = parse.urlparse(url)

        return parse.urljoin('http://' + result.netloc, '/')

    @staticmethod
    def _get_session() -> object:
        return requests.Session()

    def new_session(self) -> object:
        if getattr(self, 'session', None):
            self.session.close()
        self.session = self._get_session()
        self.session.headers = self.__headers
        return self.session

    def get_headers(self):
        return self.__headers

    def set_headers(self, headers):
        self.__headers = headers
        self.session.headers = headers
    headers = property(get_headers, set_headers)

    def request(self, method: str, url: str, data: dict={}, params: dict={}) -> requests.Response:
        """
            Отправляет серверу get или post запрос.
            В случае нудачи повторяет REQUEST_MAX_TRIES раз.
            К адресу присоединяет слева адрес сервера.
            Возвращает объект типа requests.Response
        """

        response = None
        url = self.url + url

        for attempt in range(1, REQUEST_MAX_TRIES + 1):
            try:
                logger.debug('Send {} request to url: {}'.format(method, url))
                if method == 'get':
                    response = self.session.get(url, params=params, timeout=self.timeout)
                elif method == 'post':
                    response = self.session.post(url, params=params, data=data, timeout=self.timeout)
                break
            except requests.exceptions.ConnectionError:
                print('Attempt %s of %s' % (attempt, REQUEST_MAX_TRIES))
                self.new_session()
                self.login()
            except requests.exceptions.ReadTimeout:
                print('Attempt %s of %s' % (attempt, REQUEST_MAX_TRIES))
                self.new_session()
                self.login()
            except:
                logging.error('Net problem, cant fetch the URL {}'.format(url))
                raise

        if not response:
            raise ValueError('response must be not None')

        return response

    def get(self, url: str, data: dict={}, params: dict={}) -> requests.Response:
        """ Отправляет серверу get запрос """
        return self.request('get', url, data, params)

    def post(self, url: str, data: dict={}, params: dict={}) -> requests.Response:
        """ Отправляет серверу post запрос """
        return self.request('post', url, data, params)

    def send_request(self, url: str, data: dict={}, params: dict={}) -> requests.Response:
        """
            Отправляет серверу get запрос если нет данных (data),
            иначе отправляет post запрос.
        """
        if not len(data):
            response = self.get(url, data=data, params=params)
        else:
            response = self.post(url, data=data, params=params)
        return response

    def login(self) -> None:
        """
            Метод производит вход в аккаунт.
            После входа сессия остается открытой до отключения
            или закрытия соединения.
        """

        logger.debug('Start Login to server {}'.format(self.url))

        response = self.session.get(self.url)

        if response.status_code != 200:
            logger.debug('Login failed')
            return False

        html = response.text
        parser = bs4.BeautifulSoup(html, 'html5lib')

        # извлекаем из страницы переменные нужные для входа
        s1 = parser.find('button', {'name': 's1'})['value'].encode('utf-8')
        login = parser.find('input', {'name': 'login'})['value']

        data = {
            'name': self.name,
            'password': self.password,
            's1': s1,
            'w': '1366:768',
            'login': login
            }
        response = self.session.post(self.url + 'dorf1.php', data=data)

        if response.status_code != 200:
            logger.debug('Login failed')
            return False

        html = response.text

        # вхождение подстроки в html - маркер выполнения входа
        if 'playerName' in html:
            self.loggedin = True
            # извлекаем токен для использования ajax:
            self.ajax_token = dorf1.parse_ajax_token(html)
            logger.debug('Login to server {} succeed'.format(self.url))
            return True

        self.loggedin = False
        logger.debug('Login failed')
        return False

    def load_html(self, url: str, params: dict={}, data: dict={}) -> str:
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
        data['ajaxToken'] = self.ajax_token  # В данных должен быть ajax_token, добавляем

        response = self.post(url, data=data, params=params)  # Нужен именно post запрос

        return response.text

    def get_html(self, url: str, params: dict={}, data: dict={}) -> str:
        """ Загружает страницу и сохраняет ее в буффер """

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

    def load_dorf1(self, village_id: int) -> str:
        params = {'newdid': village_id}
        return self.get_html('dorf1.php', params=params)

    def load_dorf2(self, village_id: int) -> str:
        params = {'newdid': village_id}
        return self.get_html('dorf2.php', params=params)

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

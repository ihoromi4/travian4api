import bs4

from .travparse import dorf1
from .travparse import spieler

from . import nations
from . import login
from .event import eventmachine
from .village import village
from . import reports
from . import map


class Account(eventmachine.EventMachine):
    """ Основной класс API. Агрегирует весь функционал """

    def __init__(self, url, name, password, headers=None):
        super().__init__()

        # Агрегируем объект для взаимодействия с сервером
        self.login = login.Login(url, name, password, headers)

        self.__villages = {}  # id: village
        self._nation_id = None
        self._nation = None

        self.map = map.Map(self)  # Агрегируем объект для работы с картой
        self.reports = reports.Reports(self)  # Агрегируем обект для работы с отчетами

    def get_server_time(self) -> str:
        """ Возвращает время на сервере """
        html = self.login.get_html("dorf1.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return dorf1.parse_server_time(soup)
    server_time = property(get_server_time)

    def get_rank(self) -> int:
        """ Возвращает ранг аккаунта в игровой статистике """
        html = self.login.get_html("spieler.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return spieler.parse_rank(soup)
    rank = property(get_rank)

    def get_alliance(self) -> int:
        """ Возвращает id альянса игрока """
        html = self.login.get_html("spieler.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return spieler.parse_alliance(soup)
    alliance = property(get_alliance)

    def get_villages_amount(self) -> int:
        """ Возвращает количество деревень """
        html = self.login.get_html("spieler.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return spieler.parse_villages_amount(soup)
    villages_amount = property(get_villages_amount)

    def get_population(self) -> int:
        """ Возвращает общее количество населения """
        html = self.login.get_html("spieler.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return spieler.parse_population(soup)
    population = property(get_population)

    def get_nation_id(self):
        if self._nation_id is None:
            html = self.login.get_html("dorf1.php")
            soup = bs4.BeautifulSoup(html, 'html5lib')
            self._nation_id =  dorf1.parse_nation_id(soup)
        return self._nation
    nation_id = property(get_nation_id)

    def get_nation(self):
        if self._nation:
            self._nation = nations.NATIONS[self.nation_id - 1]
        return self._nation
    nation = property(get_nation)

    def update_villages(self):
        villages_data = self._load_villages_data()
        for vdata in villages_data:
            id = vdata['id']
            pos = vdata['coords']
            if id not in self.__villages:
                vil = village.Village(self, id, pos)
                self.__villages[id] = vil

    def get_villages(self) -> list:
        """ Возвращает список поселений игрока """
        self.update_villages()
        return list(self.__villages.values())
    villages = property(get_villages)

    def get_villages_names(self) -> list:
        """ Возвращает список названий поселений игрока """
        names = [self.__villages[id].name for id in self.__villages]
        return names
    villages_names = property(get_villages_names)

    def _load_villages_data(self):
        """ Возвращает информацию о деревнях из dorf1.php """
        html = self.login.get_html("dorf1.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return dorf1.parse_villages_data(soup)

    def read_spieler(self) -> list:
        """ Возвращает информацию о деревнях из spieler.php """
        html = self.login.get_html("spieler.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return spieler.parse_spieler(soup)

    def get_village_by_id(self, id: int) -> village.Village:
        """ Возвращает поселение игрока с указанныи идентификатором id """
        self.update_villages()
        return self.__villages[id]

    def get_village_by_name(self, name: str) -> village.Village:
        """ Возвращает поселение игрока с указанныи именем name """
        for village in self.villages:
            if village.name == name:
                return village
        return None

    def get_gold(self) -> int:
        """ Возвращает количество золота на аккаунте """
        html = self.login.get_html("dorf1.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return dorf1.parse_gold_silver(soup)['gold']
    gold = property(get_gold)

    def get_silver(self) -> int:
        """ Возвращает количество серебра на аккаунте """
        html = self.login.get_html("dorf1.php")
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return dorf1.parse_gold_silver(soup)['silver']
    silver = property(get_silver)
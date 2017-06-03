import json

import bs4

from .travparse import position_details
from .travparse.position_details import PointType


class Zoom:
    """ Класс-контейнер параметров масштаба """
    MIN = 1
    MIDDLE = 2
    MAX = 3


class Map:
    """ Реализация доступа к игровой карте """

    def __init__(self, account):
        self.account = account

    def get_pos_info(self, pos: list) -> dict:
        """
            Возвращает детальную информацию о указаной клетке
            Аргументы метода:
                pos: list  # координаты точки на карте (х, у)
            Возвращаемое значение:
                Словарь с информацией о клетке:
                {
                    'pos': list,  # положение на двумерной карте, например (-40, 17)
                    'type': int,  # тип клетки PointType
                    'nation': str,  # нация если есть, иначе пустая строка
                    'alliance-id': int,  # идентификатор альянса, для игроков без альянса равно 0
                        для других клеток равно -1
                    'alliance': str,  # название альянса
                    'player-id': int,  # идентификатор игрока, для не дервенень равно -1
                    'player': str,  # имя игрока
                    'population': int  # население дервени, для не деревень равно 0
                }
        """
        params = {'x': pos[0], 'y': pos[1]}
        response = self.account.login.get('position_details.php', params=params)
        html = response.text
        soup = bs4.BeautifulSoup(html, 'html5lib')
        info = position_details.parse_position_details(soup)
        info['pos'] = pos
        return info

    def get_area(self, pos: list, zoom: int=Zoom.MIN) -> dict:
        """
            Возвращает информацию о всех клетках вокруг указаной. Быстрый метод.
            Аргументы метода:
                pos: list  # список типа (45, -34) - координаты точки на карте (х, у)
                zoom: int  # масштабирование, влияет на размер сканируемой области
                    Zoom.MIN - минимальный масштаб, область 8х8
                    Zoom.MIDDLE - средний масштаб, область 16х16
                    Zoom.Max - большой масштаб, область 32х32
            Возвращает список, каждый элемент содержит информацию об отдельной клетке на карте.
            Структура словаря:
                {
                    'pos': list,  # положение на двумерной карте, например (-40, 17)
                    'village-id': int,  # целое число - уникальный идентификатор деревни
                        для оазиса равно -1, для свободной долины равно 0
                    'user-id': int,  # число-идентификатор игрока, для оазисов равно -1
                    'alliance-id': int  # число-идентификатор альянса, начинается с 0, для озисов равно -1
                }
        """
        params = {'cmd': 'mapPositionData'}
        data = {
            'cmd': 'mapPositionData',
            'data[x]': pos[0],
            'data[y]': pos[1],
            'data[zoomLevel]': zoom
        }
        html = self.account.login.get_ajax(params=params, data=data)  # используем ajax запрос
        json_data = json.loads(html)['response']
        if json_data['error']:  # проверяем была ли ошибка
            # сервер сообщил об ошибке, посылаем исключение
            raise ValueError(json_data['errorMsg'])
        # Анализируем данные:
        data = json_data['data']['tiles']
        info = []
        for elem in data:
            v = dict()
            v['pos'] = (int(elem['x']), int(elem['y']))
            v['village-id'] = int(elem.get('d', 0))  # dorf id, -1 for oasis, 0 for valley
            v['user-id'] = int(elem.get('u', -1))  # user id, nothing for oasis (now -1)
            v['alliance-id'] = int(elem.get('a', -1))  # alliance id, nothing for oasis (now -1)
            info.append(v)
        return info

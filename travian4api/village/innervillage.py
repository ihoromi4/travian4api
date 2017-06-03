import logging
import re
import bs4

from . import buildings
from .buildings import building

from ..travparse import dorf2


class InnerVillage:
    """ Внутренняя часть деревни """

    def __init__(self, village):
        self.village = village
        self.login = village.login
        self.id = village.id
        self.__buildings = {}
        # ---
        self.__create_buildings()

    def get_html(self, params={}):      # obs
        raise TypeError('Устаревший метод!')
        # return self.village.get_html("build.php", params=params)

    def get_building_html(self, params={}) -> str:
        """ Скачивает страницу GET http://<server>/build.php """
        return self.village.get_html("build.php", params=params)

    def __create_buildings(self):
        """
        Метод для внутреннего использования
        Создает постройки
        """
        buildings_list = self._parse_dorf2_village_map()
        for building_info in buildings_list:
            name = building_info['name']
            id = building_info['id']
            level = building_info['level']
            repr = building_info['repr']
            building_type = buildings.get_building_type(repr)
            building = building_type(self, name, id, level)
            building.inner_repr = repr
            self.__buildings[id] = building

    def _update_buildings(self):
        """
        Метод для внутреннего использования
        Обновляет информацию о постройках:
            level
            is_build
            is_top_level
            resources_to_build
        """
        buildings_list = self._parse_dorf2_village_map()
        for info in buildings_list:
            building = self.__buildings[info['id']]
            if building.inner_repr == info['repr']:
                building.level = info['level']
                building.is_build = info['is_build']
                building.is_top_level = info['is_top_level']
                building.cost_for_upgrading = info['resources_to_build']
            else:
                name = info['name']
                id = info['id']
                level = info['level']
                repr = info['repr']
                logging.debug('Change building type from {} to {}'.format(building.inner_repr, repr))
                building_type = buildings.get_building_type(repr)
                building = building_type(self, name, id, level)
                building.inner_repr = repr
                self.__buildings[id] = building

    def _parse_dorf2_village_map(self):
        html = self.login.load_dorf2(self.id)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return dorf2.parse_village_map(soup)

    def get_buildings(self) -> list:
        """ Возвращает список построек """
        self._update_buildings()
        return list(self.__buildings.values())
    buildings = property(get_buildings)

    def get_building(self, inner_repr: str):
        """ Принимает строку - название постройки. Возвращает постройку """
        for building in self.buildings:
            if building.inner_repr == inner_repr:
                return building
        return None

    def get_building_by_id(self, id: int):
        """ Принимает идентификатор места постройки. Возвращает постройку """
        for build in self.buildings:
            if build.id == id:
                return build
        return None

    def start_build(self, building_id: int, c: int):
        """
        Метод для внутреннего использования
        Принимает идентификатор места постройки и внутриигровую константу
        Начинает постройку
        """
        self.village.get_html('dorf2.php', {'a': building_id, 'c': c})

    def downgrade(self, build):
        """ Начинает понижение уровня здания """
        if type(build) is int:
            id = build
        elif type(build) is building:
            name = build.name
            id = build.id
            print('Downgrade building {}, id = {}'.format(name, id))
        else:
            raise TypeError('Wrong argument type')

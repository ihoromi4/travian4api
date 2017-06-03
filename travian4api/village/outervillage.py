import re

import bs4

from .. import language
from . import buildings


class OuterVillage:
    def __init__(self, village):
        self.village = village
        self.login = village.login
        self.id = village.id
        self._buildings = {}
        self.__create_resource_fields()

    def get_html(self, params={}):
        return self.village.get_html("build.php", params=params)

    def get_buildings(self):
        self._update_buildings()
        return list(self._buildings.values())
    buildings = property(get_buildings)

    def get_building_by_id(self, id: int):
        for build in self.buildings:
            if build.id == id:
                return build
        return None

    def start_build(self, building_id, c):
        self.village.get_html('dorf1.php', {'a': building_id, 'c': c})

    def __create_resource_fields(self):
        resource_fields = self._parse_dorf1()
        for field_info in resource_fields:
            name = field_info['name']
            id = field_info['id']
            type_index = field_info['type']
            level = field_info['level']
            repr = language.index_to_building_repr(type_index)
            building_type = buildings.get_building_type(repr)
            field = building_type(self, name, id, level)
            self._buildings[id] = field

    def _update_buildings(self):
        info = self._parse_dorf1()
        for field_info in info:
            id = field_info['id']
            building = self._buildings[id]
            building.level = field_info['level']
            building.cost_for_upgrading = field_info['resources_to_build']
            building.is_build = field_info['is_build']
            building.is_top_level = field_info['is_top_level']

    def get_resource_fields(self):
        html = self.login.load_dorf1(self.id)
        # pattern = r'alt="(\b.*\b) Уровень (\d*)"/><area href='
        # buildings = re.findall(pattern, html_text)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        fields_data = soup.find_all('area')[:-1]
        resource_fields = []
        for field in fields_data:
            field_dict = dict()
            field_dict['name'], field_dict['level'] = re.findall(r'(.+) \b\S+\b (\d+)', field['alt'])[0]
            field_dict['id'] = int(re.findall(r'id=(\d+)', field['href'])[0])
            resource_fields.append(field_dict)
        return resource_fields

    @staticmethod
    def _parse_buildings_types(soup):
        village_map = soup.find('div', {'id': 'village_map'})
        div_all = village_map.find_all('div', recursive=False)
        types = {}
        for i in range(len(div_all)):
            div = div_all[i]
            id = i + 1
            build_type = -1
            for element in div['class']:
                if 'gid' in element:
                    build_type = int(element[3:])
            if build_type == -1:
                raise TypeError("build_type == -1")
            types[id] = build_type
        return types

    def _parse_dorf1(self):
        html = self.login.load_dorf1(self.id)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        types = self._parse_buildings_types(soup)
        village_map = soup.find('map', {'name': 'rx'})
        areas = village_map.find_all('area')
        resource_fields = []
        for area in areas:
            resource_field = {}
            href = area['href']
            id_list = re.findall(r'id=(\d+)', href)
            if not id_list:
                continue
            id = int(id_list[0])
            title = area['title']
            if title.find('span') == -1:
                name = title
                level = 0
                resources_to_build = None
                is_build = False
                is_top_level = False
            else:
                s = bs4.BeautifulSoup(title, 'html5lib')
                body = s.find('body')
                name = str(body.contents[0]).strip()
                level_text = body.find('span', {'class': 'level'}).text
                level = int(re.findall(r' (\d+)', level_text)[0])
                build_notice = body.find('span', {'class': 'notice'})
                is_build = bool(build_notice)
                resources_to_build = []
                for r in body.find_all('span', {'class': 'resources'}):
                    resources_to_build.append(int(r.contents[2]))
                is_top_level = not bool(resources_to_build)
            resource_field['name'] = name
            resource_field['level'] = level
            resource_field['id'] = id
            resource_field['type'] = types[id]
            resource_field['is_build'] = is_build
            resource_field['is_top_level'] = is_top_level
            resource_field['resources_to_build'] = resources_to_build
            resource_fields.append(resource_field)
        return resource_fields

import re

import bs4

from . import order


class BuildBox:
    def __init__(self, village):
        self.__village = village
        self.__orders = []

    def __getitem__(self, key):
        self.update_orders()
        return self.__orders[key]

    def __iter__(self):
        self.update_orders()
        return iter(self.__orders)

    def __repr__(self):
        self.update_orders()
        return list.__repr__(self.__orders)

    def __bool__(self):
        self.update_orders()
        return bool(self.__orders)

    def __len__(self):
        self.update_orders()
        return len(self.__orders)

    def _load_build_buildings(self) -> list:
        outer = self.__village.outer
        inner = self.__village.inner
        builds = []
        resource_fields_list = outer._parse_dorf1()
        for rf in resource_fields_list:
            if rf['is_build']:
                building = outer.get_building_by_id(rf['id'])
                builds.append(building)
        building_list = inner._parse_dorf2_village_map()
        for b in building_list:
            if b['is_build']:
                building = inner.get_building_by_id(b['id'])
                builds.append(building)
        return builds

    def _load_build_box_info(self):
        html = self.__village.login.load_dorf1(self.__village.id)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        building_list = soup.find('div', {'class': 'boxes buildingList'})
        if not building_list:
            return []
        ul = building_list.find('ul')
        all_li = ul.find_all('li')
        builds = []
        for li in all_li:
            build = {}
            div_name = li.find('div', {'class': 'name'})
            name = div_name.contents[0].strip()
            span_level = li.find('span', {'class': 'lvl'})
            level = int(re.findall(r' (\d+)', span_level.text)[0])
            div_duration = li.find('div', {'class': 'buildDuration'})
            duration = re.findall(r'(\d+:\d\d:\d\d)', div_duration.text)[0]
            time = re.findall(r' (\d+:\d\d)', div_duration.text)[0]
            build['name'] = name
            build['level'] = level
            build['duration'] = duration
            build['time'] = time
            builds.append(build)
        return builds

    def update_orders(self):
        build_box = self._load_build_box_info()
        build_buildings = self._load_build_buildings()
        orders = []
        for building in build_buildings:
            for info in build_box:
                if building.name != info['name']:
                    continue
                if building.level != info['level'] - 1:
                    continue
                ord = order.OrderBuild(building, info['level'], info['time'])
                orders.append(ord)
        self.__orders = orders

import re

import bs4

from ..import language


def parse_buildings_index_types(village_map):
    """ Возвращает словарь соответствий название постройки - внутреннее название """
    images = village_map.find_all('img')
    building_types = {}
    for img in images:
        if img['class'][0] in ('building', 'wall'):
            alt = img['alt']
            if 'span' in alt:
                name = re.findall(r'(.+) <span', img['alt'])[0]
                index = int(re.findall(r'g(\d+)', img['class'][1])[0])
            else:
                name = alt
                index = 0
            try:
                building_repr = language.index_to_building_repr(index)
            except KeyError:
                print(name, index)
                raise
            building_types[name] = building_repr
    return building_types


def parse_village_map(soup: bs4.BeautifulSoup):
    """
    Возвращает список с информацией о постройках внутри деревни.
    Каждый элемент словарь:
    {
        'name': название здания
        'level': уровень здания
        'id': идентификатор здания
        'repr': внутреннее название здания
        'is_build': строится или нет в даное время
        'is_top_level': логическое - достигла ли постройка миксимального уровня
        'resources_to_build': сколько нужно ресурсов для постройки
    }
    """
    village_map = soup.find('div', {'id': 'village_map'})
    # ---
    building_types = parse_buildings_index_types(village_map)
    # ---
    areas = village_map.find_all('area')
    buildings = []
    for area in areas:
        building = {}
        href = area['href']
        id = int(re.findall(r'id=(\d+)', href)[0])
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
        building['name'] = name
        building['level'] = level
        building['id'] = id
        building['repr'] = building_types[name]
        building['is_build'] = is_build
        building['is_top_level'] = is_top_level
        building['resources_to_build'] = resources_to_build
        buildings.append(building)
    return buildings

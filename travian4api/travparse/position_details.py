import re

import bs4


class PointType:
    """ Класс-контейнер для типов клеток на карте """
    NONE = 0  # exception
    VALLEY = 1  # abandoned-valley
    VILLAGE = 2
    OASIS = 3
    LANDSCAPE = 4  # name in html dom
    WILDERNESS = 4  # name in gui


def _parse_abandoned_valley(div_content_container: bs4.NavigableString) -> dict:
    """ Функция извлекает данные для покинутой долины """
    info = dict()
    info['type'] = PointType.VALLEY
    # get distribution
    table_distribution = div_content_container.find('table', {'id': 'distribution'})
    td_val_all = table_distribution.find_all('td', {'class': 'val'})
    distribution = [int(td.text.strip()) for td in td_val_all]
    info['distribution'] = tuple(distribution)
    return info


def _parse_village(div_content_container: bs4.NavigableString) -> dict:
    """ Функция извлекает данные для деревни игрока """
    if not div_content_container.find('table', {'id': 'village_info'}):
        # нужно извлекать данные для покинутой долины
        return _parse_abandoned_valley(div_content_container)
    info = dict()
    info['type'] = PointType.VILLAGE
    # get distribution
    table_distribution = div_content_container.find('table', {'id': 'distribution'})
    td_all = table_distribution.find_all('td')
    distribution = [int(td.text.strip()) for td in td_all]
    info['distribution'] = tuple(distribution)
    # get nation
    table_village_info = div_content_container.find('table', {'id': 'village_info'})
    all_td = table_village_info.find_all('td')
    nation = all_td[0].text.strip().lower()
    info['nation'] = nation
    # get aliance
    a = all_td[1].find('a')
    href = a['href']
    print(href)
    match = re.search(r'aid=(\d+)', href)
    alliance_id = int(match.group(1))
    info['alliance-id'] = alliance_id
    alliance = a.text.strip()
    info['alliance'] = alliance
    # get player
    a = all_td[2].find('a')
    href = a['href']
    match = re.search(r'uid=(\d+)', href)
    player_id = int(match.group(1))
    info['player-id'] = player_id
    player = a.text.strip()
    info['player'] = player
    # get population
    population = int(all_td[3].text.strip())
    info['population'] = population
    return info


def _parse_oasis(div_content_container: bs4.NavigableString) -> dict():
    """ Функция извлекает данные для оазса """
    info = dict()
    info['type'] = PointType.OASIS
    # get distribution
    table_distribution = div_content_container.find('table', {'id': 'distribution'})
    tr_all = table_distribution.find_all('tr')
    distribution = []
    for tr in tr_all:
        td_ico = tr.find('td', {'class': 'ico'})
        img = td_ico.find('img')
        resource_type = int(img['class'][0][-1])
        td_val = tr.find('td', {'class': 'val'})
        value = float(
            td_val.text.replace('\u200e', '').replace('\u202d', '').replace('\u202c', '').strip('\n\t %')) / 100
        distribution.append((resource_type, value))
    info['distribution'] = tuple(distribution)
    return info


def _parse_landscape(div_content_container: bs4.NavigableString) -> dict:
    """ Функция извлекает данные для дикой месности """
    info = dict()
    info['type'] = PointType.LANDSCAPE  # Wilderness
    return info


def parse_position_details(soup: bs4.BeautifulSoup) -> dict:
    """ Функция извлекает данные для любого типа клетки на карте """
    div_content_container = soup.find('div', {'class': 'contentContainer'})
    point_type = div_content_container.find('div', {'id': 'tileDetails'})['class'][0]
    # Базовые значения параметров клетки:
    info = dict()
    info['type'] = PointType.NONE
    info['distribution'] = (0, 0, 0, 0)
    info['nation'] = ''
    info['alliance-id'] = -1
    info['alliance'] = ''
    info['player_id'] = -1
    info['player'] = ''
    info['population'] = 0
    # Извлекаем параметры в зависимости от типа клетки:
    if point_type == 'village':  # деревня или покинутая долина
        info.update(_parse_village(div_content_container))
    elif point_type == 'oasis':  # оазис
        info.update(_parse_oasis(div_content_container))
    elif point_type == 'landscape':  # дикая местность
        info.update(_parse_landscape(div_content_container))
    return info

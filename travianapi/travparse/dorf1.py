import bs4

import re


def parse_game_version(html: str) -> float:
    pattern = r"Travian.Game.version = '([.\d]*)';"
    regex = re.compile(pattern)
    results = regex.findall(html)
    if len(results):
        game_version = float(results[0])
        return game_version
    raise TypeError("It is not valid page!")


def parse_server_language(html: str) -> str:
    pattern = r"Travian.Game.worldId = '(\D+)\d+';"
    regex = re.compile(pattern)
    results = regex.findall(html)
    if results:
        return results[0]
    raise TypeError("It is not valid page!")


def parse_ajax_token(html: str) -> str:
    pattern = r'ajaxToken\s*=\s*\'(\w+)\''
    ajax_token_compile = re.compile(pattern)
    results = ajax_token_compile.findall(html)
    if len(results):
        ajax_token = results[0]
        return ajax_token
    raise TypeError('Page sources not contain ajax token')


def parse_server_time(soup: bs4.BeautifulSoup) -> str:
    div_server_time = soup.find('div', {'id': 'servertime'})
    span_timer = div_server_time.find('span', {'class': 'timer'})
    server_time = span_timer.text
    return server_time


def parse_nation_id(soup: bs4.BeautifulSoup) -> int:
    div_player_name = soup.find('div', {'class': 'playerName'})
    img = div_player_name.find('img')
    nation_id = int(img['class'][1][-1])
    return nation_id


def parse_gold_silver(soup: bs4.BeautifulSoup) -> dict:
    gold_silver_container = soup.find('div', {'id': 'goldSilverContainer'})
    gold_container = gold_silver_container.find('div', {'class': 'gold'})
    gold_span = gold_container.find('span', {'class': 'ajaxReplaceableGoldAmount'})
    silver_container = gold_silver_container.find('div', {'class': 'silver'})
    silver_span = silver_container.find('span', {'class': 'ajaxReplaceableSilverAmount'})
    return {'gold': int(gold_span.text), 'silver': int(silver_span.text)}


def parse_villages_data(soup: bs4.BeautifulSoup) -> list:
    div = soup.find('div', {'id': 'sidebarBoxVillagelist'})
    inner_box = div.find('div', {'class': 'innerBox content'})
    all_li = inner_box.find_all('li')
    villages_data = []
    for li in all_li:
        village = {}
        href = li.find('a')['href']
        id = int(re.findall(r'id=(\d+)&', href)[0])
        village['id'] = id

        div_name = li.find('div', {'class': 'name'})
        name = div_name.text
        village['name'] = name

        strip = lambda x: x.replace('\u202d', '').replace('\u202c', '').strip('()')
        span_x = li.find('span', {'class': 'coordinateX'})
        x = int(strip(span_x.text))
        span_y = li.find('span', {'class': 'coordinateY'})
        y = int(strip(span_y.text))
        village['coords'] = (x, y)
        villages_data.append(village)
    return villages_data


def parse_all_troops(soup: bs4.BeautifulSoup) -> dict:
    div_units = soup.find('div', {'class': 'boxes villageList units'})
    table_troops = div_units.find('table', {'id': 'troops'})
    tbody = table_troops.find('tbody')
    tr_all = tbody.find_all('tr')
    units = {}
    for tr in tr_all:
        td_all = tr.find_all('td')
        if len(td_all) < 3:
            return dict()

        img = td_all[0].find('img')
        unit_type = int(img['class'][1][1:])

        number = int(td_all[1].text)

        name = td_all[2].text

        units[unit_type] = [number, name]
    return units


def parse_movements(soup: bs4.BeautifulSoup) -> dict:
    replace_type = {
        'def1': 'return',  # Воины возвращаются
        'def2': 'reinforcement',  # Воины уходят в подкрепление
        'att2': 'out-attack',  # Исходящая атака
        'att1': 'in-attack',  # Деревню атакуют
        'hero_on_adventure': 'adventure'  # Герой идет в приключение
    }
    table_movements = soup.find('table', {'id': 'movements'})
    if not table_movements:
        return dict()
    tbody = table_movements.find('tbody')
    trs = tbody.find_all('tr', recursive=False)
    movements = {}
    for tr in trs:
        img = tr.find('img')
        if not img:
            continue
        original_type = img['class'][0]
        mov_type = replace_type.get(original_type, '')
        div_mov = tr.find('div', {'class': 'mov'})
        span = div_mov.find('span')
        pattern = r'(\d+) '
        number = int(re.findall(pattern, span.text)[0])
        span_timer = tr.find('span', {'class': 'timer'})
        time = span_timer.text
        data = dict()
        data['number'] = number
        data['time'] = time
        movements[mov_type] = data
    return movements

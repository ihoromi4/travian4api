import re

import bs4


def parse_rank(soup: bs4.BeautifulSoup) -> int:
    table_details = soup.find('table', {'id': 'details'})
    tr_rank = table_details.find_all('tr')[0]
    rank = int(tr_rank.find('td').text)
    return rank


def parse_alliance(soup: bs4.BeautifulSoup) -> int:
    table_details = soup.find('table', {'id': 'details'})
    tr_alliance = table_details.find_all('tr')[2]
    td_alliance = tr_alliance.find('td')
    name = td_alliance.text
    if name == '-':
        return None
    id_url = td_alliance.find('a')['href']
    id = int(re.findall(r'aid=(\d+)', id_url)[0])
    return name, id


def parse_villages_amount(soup: bs4.BeautifulSoup) -> int:
    table_details = soup.find('table', {'id': 'details'})
    tr_villages_amount = table_details.find_all('tr')[3]
    villages_amount = int(tr_villages_amount.find('td').text)
    return villages_amount


def parse_population(soup: bs4.BeautifulSoup) -> int:
    table_details = soup.find('table', {'id': 'details'})
    tr_population = table_details.find_all('tr')[4]
    population = int(tr_population.find('td').text)
    return population


def parse_spieler(soup: bs4.BeautifulSoup) -> list:
    table = soup.find('table', {'id': 'villages'})
    table_body = table.find('tbody')
    all_tr = table_body.find_all('tr')
    villages_data = []
    for tr in all_tr:
        village = {}
        name_td = tr.find('td', {'class': 'name'})
        name_a = name_td.find('a')
        village_name = name_a.text
        village['name'] = village_name
        name_span_capital = name_td.find('span', {'class': 'mainVillage'})
        is_capital = bool(name_span_capital)
        village['is_capital'] = is_capital

        oases_td = tr.find('td', {'class': 'oases merged'})

        inhabitants_td = tr.find('td', {'class': 'inhabitants'})
        inhabitants = int(inhabitants_td.text)
        village['inhabitants'] = inhabitants

        coords_td = tr.find('td', {'class': 'coords'})
        span_x = coords_td.find('span', {'class': 'coordinateX'})
        strip = lambda x: x.replace('\u202d', '').replace('\u202c', '').strip('()')
        x = int(strip(span_x.text))
        span_y = coords_td.find('span', {'class': 'coordinateY'})
        y = int(strip(span_y.text))
        village['coords'] = (x, y)
        villages_data.append(village)
    return villages_data

import re
import bs4

from .. import base


def parse_t0(soup: bs4.BeautifulSoup) -> dict:
    merchants = soup.find_all('div', {'class': 'whereAreMyMerchants'})[0]
    text = merchants.text
    merchants_data = re.findall(r'(\d+)', text)
    data = dict()
    data['free_merchants'] = int(merchants_data[0])
    data['max_merchants'] = int(merchants_data[1])
    data['busy_on_marketplace_merchants'] = int(merchants_data[3])
    data['merchants_in_travel'] = int(merchants_data[4])
    return data


def parse_t1(soup: bs4.BeautifulSoup) -> dict:
    data = dict()
    return data


def parse_t5(soup: bs4.BeautifulSoup) -> dict:
    """
    Функция парсит страницу с перемещениями торговцев. Извлекает всю информацию.
    Перемещения делит на три типа:
        1. Исходящие - транспортировка ресурсов из деревни
        2. Возвращение - возвращение своих торговцев
        3. Входящие - входящие торговцы из других деревень
    """
    result = dict()
    result['outgoing'] = []
    result['incoming'] = []
    result['inbound'] = []

    form = soup.find('form', {'id': 'merchantsOnTheWayFormular'})
    span = form.find('span', {'id': 'merchantsOnTheWay'})
    tables = span.find_all('table', {'class': 'traders'})  # одна таблица описывает одно перемещение

    # парсим таблицу с перемещениями
    for table in tables:
        move = {}

        thead = table.find('thead')

        # извлекаем информацию о пользователе
        td = thead.find('td')
        a = td.find('a')
        user_id = base.href_to_uid(a['href'])
        user_name = a.text

        # извлекаем информацию о деревне
        td_dorf = thead.find('td', {'class': 'dorf'})
        a = td_dorf.find('a')
        village_id = base.href_to_did(a['href'])
        village_name = a.text

        tbody = table.find('tbody')

        # извлекаем информацию о времени прибытия
        span_timer = tbody.find('span', {'class': 'timer'})
        time = span_timer.text
        div_at = tbody.find('div', {'class': 'at'})
        time_at = div_at.text.strip()

        # извлекаем информацию о ресурсах
        tr_res = tbody.find('tr', {'class': 'res'})
        td = tr_res.find('td')
        span = td.find('span')
        if 'class' in span.attrs:  # бинарный признак - пустой ли торговец
            # в этом случае class="none"
            is_empty = True  # да, торговец пустой
        else:
            is_empty = False  # торговец переносит ресурсы
        pattern = r'\s+'.join([r'(\d+)'] * 4)
        resources = re.findall(pattern, span.text)[0]
        resources = [int(r) for r in resources]

        # set data
        move['user_id'] = user_id
        move['user_name'] = user_name
        move['village_id'] = village_id
        move['village_name'] = village_name
        move['time'] = time
        move['time_at'] = time_at
        move['resources'] = resources
        if is_empty:  # признак возвращающегося
            result['inbound'].append(move)
        else:
            parts = (' in ', ' в ')  # маркеры в языках eng/ru/ua
            # проверяем есть ли хоть один маркер в td_dorf.text
            flag = bool(sum([(part in td_dorf.text) for part in parts]))
            if flag:  # признак исходящего торговца
                result['outgoing'].append(move)
            else:  # иначе это входящий торговец
                result['incoming'].append(move)

    return result

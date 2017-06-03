import json
import re

import bs4

from ...travparse import parsebuild
from ... import language
from . import building


class Marketplace(building.Building):
    def __init__(self, village_part, name, id, level):
        building.Building.__init__(self, village_part, name, id, level)
        # self.eng_name = 'marketplace'
        self._max_merchants = 0
        self._free_merchants = 0
        self._busy_on_marketplace_merchants = 0
        self._merchants_in_travel = 0

    def _update_merchants_data(self):
        """ Обновляет информацию о количестве торговцев """
        html = self.village_part.get_building_html({'id': self.id, 't': 0})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        data = parsebuild.marketplace.parse_t0(soup)
        self._free_merchants = data['free_merchants']
        self._max_merchants = data['max_merchants']
        self._busy_on_marketplace_merchants = data['busy_on_marketplace_merchants']
        self._merchants_in_travel = data['merchants_in_travel']

    def get_max_merchants(self) -> int:
        """ Возвращает максимальное количество торговцев """
        self._update_merchants_data()
        return self._max_merchants
    max_merchants = property(get_max_merchants)

    def get_free_merchants(self) -> int:
        """ Возвращает количество не занятых торговцев """
        self._update_merchants_data()
        return self._free_merchants
    free_merchants = property(get_free_merchants)

    def get_busy_on_marketplace_merchants(self) -> int:
        """ Возвращает количество торговцев занятых на рынке """
        self._update_merchants_data()
        return self._busy_on_marketplace_merchants
    busy_on_marketplace_merchants = property(get_busy_on_marketplace_merchants)

    def get_merchants_in_travel(self) -> int:
        """ Возвращает количество торговцев находящихся в пути """
        self._update_merchants_data()
        return self._merchants_in_travel
    merchants_in_travel = property(get_merchants_in_travel)

    def get_merchants_moves(self) -> list:
        """ Возвращает спсок перемещений торговцев """
        html = self.village_part.get_building_html({'id': self.id, 't': 5})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        result = parsebuild.marketplace.parse_t5(soup)
        return result

    def get_exchange_pages_amount(self) -> int:
        """ Возвращает количество страниц с предложениями на рынке """
        html = self.village_part.get_building_html({'id': self.id, 't': 1})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        paginator = soup.find('div', {'class': 'paginator'})
        contents = paginator.children
        page_amount = 1
        for element in contents:
            try:
                page_amount = max(page_amount, int(element.string))
            except TypeError:
                pass
            except ValueError:
                pass
        return page_amount

    def get_exchange_page(self, page=1) -> list:
        """ Возвращает список предложений на указаной странице """
        html = self.village_part.get_building_html({'id': self.id, 't': 1, 'page': page})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        table = soup.find('table', {'id': "range"})
        rows = table.find_all('tr')[1:]
        biddings = []
        for row in rows:
            bid = {}
            elements = row.find_all('td')
            f1 = int(elements[0].text.strip())
            # f1_type_name = elements[0].find('img')['alt']
            rid = int(elements[0].find('img')['class'][0][1:]) - 1
            # f1_type = self.village_part.login.language.resource_to_int(f1_type_name)
            bid['offering'] = (f1, rid)
            relation = float(elements[1].text.strip())
            bid['relation'] = relation
            f2 = int(elements[2].text.strip())
            rid = int(elements[0].find('img')['class'][0][1:]) - 1
            bid['searching'] = (f2, rid)
            player = elements[3].find('a').text
            bid['player'] = player
            time = elements[4].text.strip()
            bid['time'] = time
            biddings.append(bid)
        return biddings

    def get_exchange_pages(self, max_page=99) -> list:
        """ Возвращает список всех предложений """
        biddings = []
        max_page = min(max_page, self.get_exchange_pages_amount())
        for page in range(1, max_page + 1):
            biddings.extend(self.get_exchange_page(page))
        return biddings

    def send_resources(self, target, resources=[0, 0, 0, 0]) -> bool:
        """ Отправляет ресурсы в указаную деревню """
        if not type(resources) in (list, tuple):
            raise TypeError("type of argument res must be list or tuple, not {}".format(type(resources)))
        if len(resources) != 4:
            raise TypeError('len of argument res must be 4')
        login = self.village_part.village.login
        html = self.village_part.get_building_html({'id': self.id, 't': '5'})
        data = dict()
        for i in range(0, 4):
            data["r{}".format(i+1)] = str(resources[i])
        data['dname'] = ''
        data['x'] = ''
        data['y'] = ''
        if type(target) is str:
            data['dname'] = target
        elif type(target) in (tuple, list):
            if len(target) == 2:
                data['x'] = str(target[0])
                data['y'] = str(target[1])
        else:
            raise TypeError("name_or_pos wrong argument type")
        data['id'] = str(self.id)
        data['t'] = '5'
        data['x2'] = '1'
        data['cmd'] = 'prepareMarketplace'
        html = login.get_ajax(data=data)
        response = json.loads(html)['response']
        if response['error']:
            print('send resource: error true')
            print(response['data'])
            return False
        bs = bs4.BeautifulSoup(html, 'html5lib')
        form = bs.find('form')
        if not form:
            return False
        for i in form.children:
            if i.name == 'input':
                data[i['name'].strip('\\\"\'')] = i['value'].strip('\\\"\'')
        html = login.get_ajax('ajax.php', data=data)
        return True

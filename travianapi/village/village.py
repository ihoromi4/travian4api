import re

import bs4

from . import outervillage
from . import innervillage
from . import buildbox
from . import troopsbox


class Village:
    def __init__(self, account, id, pos):
        self.account = account
        self.login = account.login
        self.id = id
        self.pos = tuple(pos)
        # ---
        self.outer = outervillage.OuterVillage(self)
        self.inner = innervillage.InnerVillage(self)
        self.builds = buildbox.BuildBox(self)
        self.troops = troopsbox.TroopsBox(self)

    def get_html(self, last_url='', params={}) -> str:
        params['newdid'] = self.id
        return self.login.get_html(last_url, params=params)

    def get_name(self) -> str:
        html_text = self.login.load_dorf1(self.id)
        pattern = r'<div id="villageNameField" class="boxTitle">(.*)</div>'
        regex = re.compile(pattern)
        names = regex.findall(html_text)
        return names[0]
    name = property(get_name)

    def get_warehouse(self) -> float:
        html_text = self.login.load_dorf1(self.id)
        pattern = r'<span class="value" id="stockBarWarehouse">(\d*)</span>'
        warehouse = int(re.findall(pattern, html_text)[0])
        return warehouse
    warehouse = property(get_warehouse)

    def get_granary(self) -> float:
        html_text = self.login.load_dorf1(self.id)
        pattern = r'<span class="value" id="stockBarGranary">(\d*)</span>'
        granary = int(re.findall(pattern, html_text)[0])
        return granary
    granary = property(get_granary)

    def get_resources(self) -> list:
        html_text = self.login.load_dorf1(self.id)
        pattern = r'<span id="l\d" class="value(?: alert)?">(\d*)</span>'
        raw_resources = re.findall(pattern, html_text)
        resources = [int(p) for p in raw_resources]
        return resources
    resources = property(get_resources)

    def get_production(self) -> list:
        """
        Возвращает информацию о производстве в выбраной деревне
        """
        html_text = self.login.load_dorf1(self.id)
        pattern = r'"l\d": (-?\d+)'
        result = re.findall(pattern, html_text)[0:4]
        production = [int(p) for p in result]
        return production
    production = property(get_production)

    def get_free_crop(self) -> int:
        html = self.login.load_dorf1(self.id)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        span_free_crop = soup.find('span', {'id': 'stockBarFreeCrop'})
        free_crop = int(span_free_crop.text)
        return free_crop
    free_crop = property(get_free_crop)

    def get_building_by_id(self, id: int):
        return self.inner.get_building_by_id(id) or \
                self.outer.get_building_by_id(id)

    def get_building_by_repr(self, repr: str):
        return self.inner.get_building(repr)

    def get_building(self, repr):
        if type(repr) is int:
            return self.get_building_by_id(repr)
        return self.get_building_by_repr(repr)

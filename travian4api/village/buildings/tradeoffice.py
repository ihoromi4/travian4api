import json
import re

import bs4

from ...travparse import parsebuild
from . import building


class Tradeoffice(building.Building):
    def __init__(self, village_part, name, id, level):
        building.Building.__init__(self, village_part, name, id, level)

    def get_able_carry(self) -> int:
        html = self.village_part.get_building_html({'id': self.id})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return parsebuild.tradeoffice.parse_tradeoffice(soup)
    able_carry = property(get_able_carry)

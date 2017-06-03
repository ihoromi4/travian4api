# Ратуша
import re

import bs4

from . import building


class TownHall(building.Building):
    def get_culture_small_celebration(self):
        html = self.village_part.get_html({'id': self.id, 'a': 1})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        div_p = soup.find('div', {'class': 'build_details researches'})
        culture_points_text = div_p.find('span', {'class': 'points'}).text
        culture_points = int(re.findall(r'(\d+) .+', culture_points_text)[0])
        return culture_points
    culture_small_celebration = property(get_culture_small_celebration)

    def make_small_celebration(self):
        self.village_part.get_html({'id': self.id, 'a': 1})

    def make_great_celebration(self):
        self.village_part.get_html({'id': self.id, 'a': 2})

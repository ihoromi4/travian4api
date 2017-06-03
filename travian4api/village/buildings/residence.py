import time

import bs4

from . import building


class Residence(building.Building):
    def __init__(self, village_part, name, id, level):
        building.Building.__init__(self, village_part, name, id, level)
        self._village_amount = None
        self._village_max_amount = None
        self._culture = None
        self._culture_for_new_village = None
        self._need_culture = None
        self._this_village = None
        self._other_villages = None
        self._hero = None
        self._total = None
        self._update_time = 0

    def get_culture_data(self):
        if time.time() - self._update_time < 3.0:
            # даные были обновлены не позже чем 3 сек назад
            return
        # иначе обновляем данные
        self._update_time = time.time()
        culture_page = 2
        # скачиваем страницу с информацией
        html = self.village_part.get_html({'id': self.id, 's': culture_page})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        # извлекаем информацию о единицах культуры
        culture_production_hint = soup.find_all('div', {'id': 'culturePointsProductionHint'})[0]
        culture_production = culture_production_hint.find_all('td')
        self._this_village = int(culture_production[0].text)
        self._other_villages = int(culture_production[1].text)
        self._hero = int(culture_production[2].text)
        self._total = int(culture_production[3].find('div', {'class': ''}).text)
        # извлекаем информацию о деревнях и культуре
        village_slot_information = soup.find_all('div', {'id': 'villageSlotInformation'})[0]
        data = village_slot_information.find_all('td')
        self._village_amount = int(data[0].text)
        self._village_max_amount = int(data[1].text)
        self._culture = int(data[2].text)
        self._culture_for_new_village = int(data[3].text)
        self._need_culture = int(data[4].find('div', {'class': ''}).text)

    def get_village_amount(self):
        self.get_culture_data()
        return self._village_amount
    village_amount = property(get_village_amount)

    def get_village_max_amount(self):
        self.get_culture_data()
        return self._village_max_amount
    village_max_amount = property(get_village_max_amount)

    def get_culture(self):
        self.get_culture_data()
        return self._culture
    culture = property(get_culture)

    def get_culture_for_new_village(self):
        self.get_culture_data()
        return self._culture_for_new_village
    culture_for_new_village = property(get_culture)

    def get_need_culture(self):
        self.get_culture_data()
        return self._need_culture
    need_culture = property(get_need_culture)

    def get_this_village(self):
        self.get_culture_data()
        return self._this_village
    this_village = property(get_this_village)

    def get_other_villages(self):
        self.get_culture_data()
        return self._other_villages
    other_villages = property(get_other_villages)

    def get_hero(self):
        self.get_culture_data()
        return self._hero
    hero = property(get_hero)

    def get_total(self):
        self.get_culture_data()
        return self._total
    total = property(get_total)
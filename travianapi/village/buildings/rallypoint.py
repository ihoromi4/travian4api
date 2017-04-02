import bs4

from ...travparse import parsebuild
from . import building


# Точка сбора
class RallyPoint(building.Building):
    def __init__(self, village_part, name, id, level):
        building.Building.__init__(self, village_part, name, id, level)
        self.eng_name = 'rallypoint'

    def post(self, url, params, data):
        pass

    def get_incoming(self):
        html = self.village_part.get_html({'id': self.id, 'tt': 1})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return parsebuild.rallypoint.parse_troops(soup)['incoming']
    incoming = property(get_incoming)

    def get_outgoing(self):
        html = self.village_part.get_html({'id': self.id, 'tt': 1})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return parsebuild.rallypoint.parse_troops(soup)['outgoing']
    outgoing = property(get_outgoing)

    def get_in_village(self):
        html = self.village_part.get_html({'id': self.id, 'tt': 1})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        return parsebuild.rallypoint.parse_troops(soup)['in_village']
    in_village = property(get_in_village)

    def reinforcement(self):
        pass

    def attack_normal(self):
        pass

    def attack_raid(self, pos):
        pass

    def step_1(self, pos, troops, c=4):
        send_troops_page = 2
        html = self.village_part.village.login.get_html('build.php', {'id': self.id, 'tt': send_troops_page})
        soup = bs4.BeautifulSoup(html, 'html5lib')
        div_build = soup.find('div', {'id': 'build'})
        data = dict()
        data['x'] = pos[0]
        data['y'] = pos[1]
        data['c'] = c
        data['timestamp'] = div_build.find('input', {'name': 'timestamp'})['value']
        data['timestamp_checksum'] = div_build.find('input', {'name': 'timestamp_checksum'})['value']
        data['b'] = div_build.find('input', {'name': 'b'})['value']
        data['currentDid'] = div_build.find('input', {'name': 'currentDid'})['value']
        data.update(troops)
        # data['t5'] = 5
        data['s1'] = 'ok'
        self.step_2(data, troops)

    def step_2(self, data, troops):
        send_troops_page = 2
        params = {'id': self.id, 'tt': send_troops_page}
        html = self.village_part.village.login.server_post('build.php', data=data, params=params)
        soup = bs4.BeautifulSoup(html, 'html5lib')
        div_build = soup.find('div', {'id': 'build'})
        # data = {}
        data['timestamp'] = div_build.find('input', {'name': 'timestamp'})['value']
        data['timestamp_checksum'] = div_build.find('input', {'name': 'timestamp_checksum'})['value']
        input_id = div_build.find('input', {'name': 'id'})
        if not input_id:
            return      # some problem
        data['id'] = input_id['value']
        data['a'] = div_build.find('input', {'name': 'a'})['value']
        data['c'] = div_build.find('input', {'name': 'c'})['value']
        data['kid'] = div_build.find('input', {'name': 'kid'})['value']
        for i in range(1, 12):
            data['t%s' % (i,)] = int(div_build.find('input', {'name': 't%s' % (i,)})['value'])
        # костыль:
        for key in troops:
            if data[key] < troops[key]:
                return
        data['sendReally'] = div_build.find('input', {'name': 'sendReally'})['value']
        data['troopsSent'] = div_build.find('input', {'name': 'troopsSent'})['value']
        data['currentDid'] = div_build.find('input', {'name': 'currentDid'})['value']
        data['b'] = div_build.find('input', {'name': 'b'})['value']
        data['dname'] = div_build.find('input', {'name': 'dname'})['value']
        data['x'] = div_build.find('input', {'name': 'x'})['value']
        data['y'] = div_build.find('input', {'name': 'y'})['value']
        html = self.village_part.village.login.server_post('build.php', data=data, params=params)

    def send_troops(self, pos, troops={'t5': 5}, c=4):
        # c = 2       # Reinforcement
        # c = 3       # Attack: Normal
        # c = 4       # Attack: Raid
        print(self.village_part.village.name, 'raid to', pos)
        self.step_1(pos, troops, c)

import bs4

from ..travparse import dorf1


class TroopsBox:
    """ Агрегирует информацию о всех войсках в деревне """

    def __init__(self, village):
        self.village = village

    def get_movements(self):
        """ Возвращает информацию о передвижениях """
        html = self.village.get_html('dorf1.php')
        soup = bs4.BeautifulSoup(html, 'html5lib')
        movements = dorf1.parse_movements(soup)
        return movements

    def get_incoming(self):
        return self.rallypoint.incoming
    incoming = property(get_incoming)

    def get_outgoing(self):
        return self.rallypoint.outgoing
    outgoing = property(get_outgoing)

    def get_in_village(self):
        return self.rallypoint.in_village
    in_village = property(get_in_village)

    def get_rallypoint(self):
        return self.village.inner.get_building('rallypoint')
    rallypoint = property(get_rallypoint)

    def get_all_troops(self):
        html = self.village.get_html('dorf1.php')
        soup = bs4.BeautifulSoup(html, 'html5lib')
        troops = dorf1.parse_all_troops(soup)
        return troops

    def reinforcement(self):
        pass

    def attack_normal(self):
        pass

    def attack_raid(self, pos, troops):
        self.rallypoint.send_troops(pos, troops)

from . import nations


romans = {
    1: 'legionnaire',  # t1
    2: 'praetorian',
    3: 'imperian',
    4: 'equites_legati',
    5: 'equites_imperatoris',
    6: 'equites_caesaris',
    7: 'battering_ram',
    8: 'fire_catapult',
    9: 'senator',
    10: 'settler',
    11: 'hero'
}

teutons = {
    1: 'clubswinger',  # t1
    2: 'spearman',
    3: 'axeman',
    4: 'scout',
    5: 'paladin',
    6: 'teutonic_knight',
    7: 'ram',
    8: 'catapult',
    9: 'chief',
    10: 'settler',
    11: 'hero'
}

gauls = {
    1: 'phalanx',  # t1
    2: 'swordsman',
    3: 'pathfinder',
    4: 'theutates_thunder',
    5: 'druidrider',
    6: 'haeduan',
    7: 'ram',
    8: 'trebuchet',
    9: 'chieftain',
    10: 'settler',
    11: 'hero'
}

unit_types = {
    'hero': 'hero',

    1: 'legionnaire',  # u1
    2: 'praetorian',
    3: 'imperian',
    4: 'equites_legati',
    5: 'equites_imperatoris',
    6: 'equites_caesaris',
    7: 'battering_ram',
    8: 'fire_catapult',
    9: 'senator',
    10: 'settler',

    11: 'clubswinger',  # u11
    12: 'spearman',
    13: 'axeman',
    14: 'scout',
    15: 'paladin',
    16: 'teutonic_knight',
    17: 'ram',
    18: 'catapult',
    19: 'chief',
    20: 'settler',

    21: 'phalanx',  # u21
    22: 'swordsman',
    23: 'pathfinder',
    24: 'theutates_thunder',
    25: 'druidrider',
    26: 'haeduan',
    27: 'ram',
    28: 'trebuchet',
    29: 'chieftain',
    30: 'settler',
}


class Troop:
    def __init__(self, troops: dict=dict(), nation: str=nations.ROMANS):
        self.nation = nation
        self.troops = troops

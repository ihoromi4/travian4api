import logging
import json

BUILDINGS_REPR = {
    (-1, "building"),
    (0, "buildingsite"),
    (1, "woodcutter"),
    (2, "claypit"),
    (3, "ironmine"),
    (4, "cropland"),
    (5, 'sawmill'),
    (6, 'brickyard'),
    (7, 'ironfoundry'),
    (8, 'grainmill'),
    (9, 'bakery'),
    (10, 'warehouse'),
    (11, 'granary'),

    (13, 'smithy'),
    (14, 'tournamentsquare'),
    (15, "mainbuilding"),
    (16, "rallypoint"),
    (17, "marketplace"),
    (18, 'embassy'),
    (19, 'barracks'),
    (20, 'stable'),
    (21, 'workshop'),
    (22, 'academy'),
    (23, 'cranny'),
    (24, "townhall"),
    (25, "residence"),
    (26, "palace"),
    (27, 'treasury'),
    (28, 'tradeoffice'),

    (31, 'wall'),
    (32, 'earthwall'),
    (33, "palisade"),
    (34, 'stonemasonslodge'),
    (35, 'brewery'),
    (36, 'trapper'),
    (37, 'herosmansion'),
    (38, 'greatwarehouse'),
    (39, 'greatgranary')
}

DICT_INDEX_TO_BUILDING = dict(BUILDINGS_REPR)


def index_to_building_repr(index: int) -> str:
    """ Принимает идентификатор ГРАФИКИ постройки. Возвращает внутреннее представление """
    repr = DICT_INDEX_TO_BUILDING.get(index, '')
    if not repr:
        logging.error('Language building repr no has key: {}'.format(index))
        repr = DICT_INDEX_TO_BUILDING[-1]
    return repr

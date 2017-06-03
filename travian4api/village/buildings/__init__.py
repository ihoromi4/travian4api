from . import building
from . import marketplace
from . import tradeoffice
from . import palace
from . import residence
from . import resourcefield
from . import townhall
from . import rallypoint

building_dict = {
    "building": building.Building,
    "woodcutter": resourcefield.Woodcutter,
    "claypit": resourcefield.Claypit,
    "ironmine": resourcefield.Ironmine,
    "cropland": resourcefield.Cropland,
    "marketplace": marketplace.Marketplace,
    "tradeoffice": tradeoffice.Tradeoffice,
    "residence": residence.Residence,
    "palace": palace.Palace,
    "townhall": townhall.TownHall,
    "rallypoint": rallypoint.RallyPoint
}


def get_building_type(name):
    if name in building_dict:
        return building_dict[name]
    return building.Building

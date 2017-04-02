from . import building


class ResourceField(building.Building):
    """
    Class ResourceField is base class for all resource fields classes in the API.
    """
    pass


class Woodcutter(ResourceField):
    pass


class Claypit(ResourceField):
    pass


class Ironmine(ResourceField):
    pass


class Cropland(ResourceField):
    pass

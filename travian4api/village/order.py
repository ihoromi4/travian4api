
class Order:
    pass


class OrderBuild(Order):
    def __init__(self, building, to_level, end_time):
        self.building = building
        self.to_level = to_level
        self.end_time = end_time

    def __repr__(self):
        return 'Build order <{}>, building: {}, to level: {}, end: {}'.format(id(self),
                                                                              self.building.name,
                                                                              self.to_level,
                                                                              self.end_time)

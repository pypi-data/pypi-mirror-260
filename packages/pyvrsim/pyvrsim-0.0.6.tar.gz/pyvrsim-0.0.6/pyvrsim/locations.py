# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Abdelouahed Ben Mhamed
Email: a.benmhamed@intelligentica.net
Email: abdelouahed.benmhamed@um6p.ma
Website: https://intelligentica.net
"""
from .location import Location


class Locations:
    """
    A class for the Location objects
    :param locations: the list of Location instances
    """

    def __init__(self, locations):

        if not isinstance(locations, list):
            raise TypeError("Expected a list of Location objects")

        if not all(isinstance(item, Location) for item in locations):
            raise TypeError("Expected a list of Location objects")

        self.locations = locations
        self.total_size = len(locations)
        self.names = self.set_names()

    def __repr__(self):
        return f"{self.__class__.__name__}(\n" \
               f"\tcoordinates = {[loc.coordinates for loc in self.locations]},\n" \
               f"\tcategories = {[loc.category for loc in self.locations]},\n" \
               f"\tnames = {self.names},\n" \
               f"\ttotal_size = {self.total_size},\n)"

    def __len__(self):
        return len(self.locations)

    def set_names(self):
        counter = {"Depot": 0, "Customer": 0}
        names = []
        for loc in self.locations:
            counter[loc.category] += 1
            name = loc.category + counter[loc.category]
            names.append(name)
        return names

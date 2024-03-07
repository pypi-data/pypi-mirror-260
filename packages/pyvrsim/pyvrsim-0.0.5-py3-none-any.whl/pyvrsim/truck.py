# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Abdelouahed Ben Mhamed
Email: a.benmhamed@intelligentica.net
Email: abdelouahed.benmhamed@um6p.ma
Website: https://intelligentica.net
"""
from .fleet import Fleet


class Truck:
    """
    A class for the Truck objects

    :param speed: The speed of the truck in (km/h)
    :param capacity: The maximum capacity of the truck in (kg)
    """

    # Class attribute
    category = "vehicles"
    type = "truck"

    def __init__(self, speed=None, capacity=None):
        """
        Initialize a Truck instance with the given parameters.
        """
        # Validate the model parameter

        if speed is not None and not isinstance(speed, (int, float)):
            raise TypeError("Invalid 'speed' value. 'speed' must be a numeric")

        if capacity is not None and not isinstance(capacity, (int, float)):
            raise TypeError("Invalid 'capacity' value. 'capacity' must be a numeric")

        # Instance attributes
        self.speed = speed
        self.capacity = capacity

    def __repr__(self):
        return f"{self.__class__.__name__}(\n" \
               f"\ttype = {self.type}\n" \
               f"\tcapacity = {self.capacity} (kg), \n" \
               f"\tspeed = {self.speed} (km/h), \n)"

    def get_category(self):
        return self.category

    def get_type(self):
        return self.type

    def __add__(self, other):
        if isinstance(other, Fleet):
            fleet = Fleet([self] + other.vehicles)
            return fleet
        elif other.category != "vehicles":
            raise TypeError("Invalid operation. The addition must be between objects within the 'vehicles' category.")
        else:
            t1 = Truck(speed=self.speed, capacity=self.capacity)
            t2 = Truck(speed=other.speed, capacity=other.capacity)
            fleet = Fleet([t1, t2])
            return fleet

    def __mul__(self, scalar):
        if not isinstance(scalar, int):
            raise TypeError("Invalid multiplication. The scalar must be an integer")

        fleet = Fleet([Truck(speed=self.speed, capacity=self.capacity) for _ in range(scalar)])
        return fleet

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

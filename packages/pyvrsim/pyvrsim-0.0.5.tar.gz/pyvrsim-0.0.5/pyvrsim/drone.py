# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Abdelouahed Ben Mhamed
Email: a.benmhamed@intelligentica.net
Email: abdelouahed.benmhamed@um6p.ma
Website: https://intelligentica.net
"""
from .fleet import Fleet


class Drone:
    """
    A class for the Drone objects

    :param speed: The speed of the truck in (km/h)
    :param capacity: The maximum capacity of the truck in (kg)
    :param flight_time: The flight time of the drone in (minutes)
    """

    # Class attribute
    category = "vehicles"
    type = "drone"

    def __init__(self, speed=None, capacity=None, flight_time=None):
        """
        Initialize a Drone instance with the given parameters.
        """
        # Validate the model parameter

        if speed is not None and not isinstance(speed, (int, float)):
            raise TypeError("Invalid 'speed' value. 'speed' must be a numeric")

        if capacity is not None and not isinstance(capacity, (int, float)):
            raise TypeError("Invalid 'capacity' value. 'capacity' must be a numeric")

        if flight_time is not None and not isinstance(flight_time, (int, float)):
            raise TypeError("Invalid 'flight_time' value. 'flight_time' must be a numeric")

        # Instance attributes
        self.speed = speed
        self.capacity = capacity
        self.flight_time = flight_time

    def __repr__(self):
        return f"{self.__class__.__name__}(\n" \
               f"\ttype = {self.type}\n" \
               f"\tcapacity = {self.capacity} (kg), \n" \
               f"\tspeed = {self.speed} (km/h), \n"\
               f"\tflight_time = {self.flight_time} (minutes) \n)"

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
            d1 = Drone(speed=self.speed, capacity=self.capacity, flight_time=self.flight_time)
            d2 = Drone(speed=other.speed, capacity=other.capacity, flight_time=other.flight_time)
            fleet = Fleet([d1, d2])
            return fleet

    def __mul__(self, scalar):
        if not isinstance(scalar, int):
            raise TypeError("Invalid multiplication. The scalar must be an integer")

        fleet = Fleet([Drone(speed=self.speed, capacity=self.capacity, flight_time=self.flight_time) for _ in range(scalar)])
        return fleet

    def __rmul__(self, scalar):
        return self.__mul__(scalar)


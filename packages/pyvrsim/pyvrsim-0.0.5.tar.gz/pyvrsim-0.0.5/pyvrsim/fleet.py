# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Abdelouahed Ben Mhamed
Email: a.benmhamed@intelligentica.net
Email: abdelouahed.benmhamed@um6p.ma
Website: https://intelligentica.net
"""


class Fleet:
    def __init__(self, vehicles):
        self.vehicles = vehicles
        self.total_size = len(vehicles)
        self.homogeneous = self.is_homogeneous()
        self.number_groups, self.groups_sizes, self.groups_features = self.calculate_groups()

    def is_homogeneous(self):
        from .truck import Truck
        from .drone import Drone

        if not self.vehicles:
            return True

        first_vehicle = self.vehicles[0]
        vehicle_type = first_vehicle.get_type()

        if vehicle_type == "truck":
            return all(isinstance(vehicle, Truck) and
                       vehicle.speed == first_vehicle.speed and
                       vehicle.capacity == first_vehicle.capacity
                       for vehicle in self.vehicles)
        elif vehicle_type == "drone":
            return all(isinstance(vehicle, Drone) and
                       vehicle.speed == first_vehicle.speed and
                       vehicle.capacity == first_vehicle.capacity and
                       vehicle.flight_time == first_vehicle.flight_time
                       for vehicle in self.vehicles)
        else:
            return False

    def calculate_groups(self):
        from .truck import Truck
        from .drone import Drone

        if not self.vehicles:
            return 0, [], []

        groups = {}
        for vehicle in self.vehicles:
            vehicle_type = vehicle.get_type()
            features = (vehicle.speed, vehicle.capacity)

            if isinstance(vehicle, Drone):
                features += (vehicle.flight_time,)

            if vehicle_type not in groups:
                groups[vehicle_type] = {'size': 1, 'features': features}
            else:
                groups[vehicle_type]['size'] += 1

        number_groups = len(groups)
        groups_sizes = [group['size'] for group in groups.values()]
        groups_features = [(vehicle_type,) + group['features'] for vehicle_type, group in groups.items()]

        return number_groups, groups_sizes, groups_features

    def __repr__(self):
        return f"{self.__class__.__name__}(\n" \
               f"\ttotal_size = {self.total_size}, \n" \
               f"\thomogeneous = {self.homogeneous}, \n" \
               f"\tnumber_groups = {self.number_groups}, \n" \
               f"\tgroups_sizes = {self.groups_sizes}, \n" \
               f"\tgroups_features = {self.groups_features}\n)"

    def __add__(self, other):
        if isinstance(other, Fleet):
            return Fleet(self.vehicles + other.vehicles)
        else:
            raise TypeError("Invalid operation. The addition must be between Fleet objects.")

    def __mul__(self, scalar):
        if not isinstance(scalar, int):
            raise TypeError("Invalid multiplication. The scalar must be an integer")

        return Fleet(self.vehicles * scalar)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

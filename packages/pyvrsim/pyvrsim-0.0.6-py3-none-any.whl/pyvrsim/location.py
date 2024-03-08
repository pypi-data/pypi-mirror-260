# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Abdelouahed Ben Mhamed
Email: a.benmhamed@intelligentica.net
Email: abdelouahed.benmhamed@um6p.ma
Website: https://intelligentica.net
"""
from geopy.geocoders import Nominatim
import pandas as pd
import random
import googlemaps
import folium
import polyline
from IPython.display import IFrame


class Location:
    """
    A class for the Location objects
    :param category: The category of the location (values should be in ('Customer', 'Depot'))
    :param coordinates: The decimal latitude and longitude of the location
    """

    def __init__(self, category, coordinates):
        if not isinstance(coordinates, tuple):
            raise TypeError("Invalid 'coordinates' type. 'coordinates' must be a tuple (x, y)")
        if category not in ['Customer', 'Depot']:
            raise ValueError("'category' must be in 'Customer', 'Depot'")
        self.category = [category]
        self.coordinates = [coordinates]

    def __repr__(self):
        return f"{self.__class__.__name__}(\n" \
               f"\tcategory = {self.category},\n" \
               f"\tcoordinates = {self.coordinates},\n)"

    def __len__(self):
        """Return the number of locations"""
        return len(self.category)

    def __add__(self, other):
        from .locations import Locations
        if isinstance(other, Location):
            new_loc = [Location(category=self.category[0], coordinates=self.coordinates[0]),
                       Location(category=other.category[0], coordinates=other.coordinates[0])]
        elif isinstance(other, Locations):
            new_loc = [Location(category=self.category[0], coordinates=self.coordinates[0])]
            new_loc.extend(other)
        else:
            raise TypeError("Invalid operation. 'other' must be a Location object.")
        return new_loc

    @classmethod
    def create_manual(cls, data):
        """
        Create Location objects manually by providing category/categories and the tuple of the location.
        :param data: A tuple (category, coordinates) or a list of tuples
        :return: Location object(s)
        """
        if not isinstance(data, list):
            data = [data]
        locations = [cls(category, coordinates) for category, coordinates in data]
        return cls._merge_locations(locations)

    @classmethod
    def create_from_file(cls, file_path):
        """
        Create Location objects by importing from an xlsx, csv, or txt file.
        The file should contain three columns: category, x or longitude, and y or latitude.
        :param file_path: Path to the file
        :return: Location object(s)
        """
        data = pd.read_csv(file_path)

        # Dynamically determine column names
        expected_columns = {'category', 'x', 'y'}
        actual_columns = set(data.columns)

        if expected_columns.issubset(actual_columns):
            category_col = 'category'
            longitude_col = 'x'
            latitude_col = 'y'
        elif {'category', 'longitude', 'latitude'}.issubset(actual_columns):
            category_col = 'category'
            longitude_col = 'longitude'
            latitude_col = 'latitude'
        else:
            raise ValueError(
                "Invalid column names. Columns should be: 'category', 'x', 'y' or 'category', 'longitude', 'latitude'.")

        locations = [(row[category_col], (row[longitude_col], row[latitude_col])) for _, row in data.iterrows()]
        return cls._merge_locations(locations)

    @classmethod
    def create_random(cls, num_locations, latitude_limits, longitude_limits, first_as_depot=False):
        """
        Generate Location objects by generating random locations within specified latitude and longitude limits.
        Verify if the location is on land.
        :param num_locations: Number of locations to generate
        :param latitude_limits: Tuple (min_latitude, max_latitude)
        :param longitude_limits: Tuple (min_longitude, max_longitude)
        :param first_as_depot: If True, the first location will be assigned the category 'Depot'
        :return: Location object(s)
        """
        locations = []
        geolocator = Nominatim(user_agent="location_verification")
        counter = 1
        while len(locations) < num_locations:
            latitude = random.uniform(*latitude_limits)
            longitude = random.uniform(*longitude_limits)
            if first_as_depot and counter == 1:
                location = ("Depot", (round(latitude, 3), round(longitude, 3)))
            else:
                location = ("Customer", (round(latitude, 3), round(longitude, 3)))

            # Verify if the location is on land
            address = geolocator.reverse((latitude, longitude), language='en')
            if "water" not in address.raw['address']:
                counter += 1
                locations.append(location)

        return cls._merge_locations(locations)

    @classmethod
    def _merge_locations(cls, locations):
        """
        Helper method to merge multiple Location objects into one.
        :param locations: List of Location objects
        :return: Merged Location object
        """
        if not locations:
            raise ValueError("No locations provided.")

        categ, coords = locations[0]
        merged_loc = cls(category=categ, coordinates=coords)

        for loc in locations[1:]:
            categ, coords = loc
            merged_loc.category.append(categ)
            merged_loc.coordinates.append(coords)

        return merged_loc

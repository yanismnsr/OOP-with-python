from json import *
from pprint import *
from math import pi
import matplotlib.pyplot as plt

# all this work is accomplished thanks to https://openclassrooms.com/fr/
# I generated random people from a virtual database of the entire population
# from the website : http://pplapi.com/

# example of an agent :
# [('age', 16), ('agreeableness', -0.6804278417648575), ('conscientiousness', -0.6805758063751579), ('country_name', 'Mozambique'),
#    ('country_tld', 'mz'), ('date_of_birth', '2001-01-23'), ('extraversion', -0.02993482312867385), ('id', 6243924129), ('id_str', 'Yt0-7wr'),
#    ('income', 731), ('internet', False), ('language', 'Cisena'), ('latitude', -18.114071465621226), ('longitude', 35.281777814295076),
#   ('neuroticism', -1.122907039486035), ('openness', 1.4842576176353213), ('religion', 'Protestant'), ('sex', 'Female')]

class Agent:
    """
    each agent is a person from my world
    he has many caracters : agreeableness, position by
    latitud and longitud ...
    """

    def say_hello(self, first_name):
        """
        the first method I created,
        concidering that my agents are agreable,
        they say hello yanis !
        """
        return "hello " + first_name + " !"

    def __init__ (self, position, **agent):
        self.position = position
        for attr_name, attr_value in agent.items():
            setattr(self, attr_name, attr_value)


class Position:
    """
    a position is an object that contains 2 attributes :
        latitud_degrees
        longitud_degrees
    we use it to determinate a location of an agent,
    the zone to wich he belongs ...
    it contains also two properties wich convert latitud and
    longitud to radians
    """

    def __init__(self, longitude_degrees, latitude_degrees):
        self.latitude_degrees = latitude_degrees
        self.longitude_degrees = longitude_degrees

    @property
    def longitude(self):
        return self.longitude_degrees * pi / 180

    @property
    def latitude(self):
        return self.latitude_degrees * pi / 180


class Zone:
    """
    this is our main and biggest class
    it contains class attributes
    each zone is a square determinated by its bottom_left_corner
    and its top_right_corner
    """

    MIN_LONGITUDE_DEGREES = -180
    MAX_LONGITUDE_DEGREES = 180
    MIN_LATITUDE_DEGREES = -90
    MAX_LATITUDE_DEGREES = 90
    WIDTH_DEGREES = 1
    HEIGHT_DEGREES = 1
    ZONE = []
    EARTH_RADIUS_KILOMETERS = 6371

    def __init__(self, corner1, corner2):
        self.corner1 = corner1
        self.corner2 = corner2
        self.habitants = []

    def add_inhabitants(self, agent):
        self.habitants.append(agent)

    @property
    def population(self):
        return len(self.habitants)

    @classmethod
    def _initialize_zone(cls):
        for latitude in range(cls.MIN_LATITUDE_DEGREES, cls.MAX_LATITUDE_DEGREES, cls.HEIGHT_DEGREES):
            for longitude in range(cls.MIN_LONGITUDE_DEGREES, cls.MAX_LONGITUDE_DEGREES, cls.WIDTH_DEGREES):
                bottom_left_corner = Position(longitude, latitude)
                top_right_corner = Position(longitude + cls.WIDTH_DEGREES, latitude + cls.HEIGHT_DEGREES)
                zone = Zone(bottom_left_corner, top_right_corner)
                cls.ZONE.append(zone)

    def contains(self, position):
        return min(self.corner1.longitude, self.corner2.longitude) <= position.longitude < max(self.corner1.longitude, self.corner2.longitude) \
        and min(self.corner1.latitude, self.corner2.latitude) <= position.latitude < max(self.corner1.latitude, self.corner2.latitude)

    @classmethod
    def zone_that_contains(cls, position):

        if not Zone.ZONE :
            cls._initialize_zone()

        longitude_position = int((position.longitude_degrees - cls.MIN_LONGITUDE_DEGREES) / cls.WIDTH_DEGREES)
        latitude_position = int((position.latitude_degrees - cls.MIN_LATITUDE_DEGREES) / cls.HEIGHT_DEGREES)
        longitude_bins = int((cls.MAX_LONGITUDE_DEGREES - cls.MIN_LONGITUDE_DEGREES) / cls.WIDTH_DEGREES)
        zone_index = latitude_position * longitude_bins + longitude_position

        zone = Zone.ZONE[zone_index]
        assert zone.contains(position)

        return zone

    @property
    def width(self):
        return (self.corner2.longitude - self.corner1.longitude) * self.EARTH_RADIUS_KILOMETERS

    @property
    def height(self):
        return (self.corner2.latitude - self.corner1.latitude) * self.EARTH_RADIUS_KILOMETERS

    @property
    def area(self):
        return self.width * self.height

    @property
    def density(self):
        return self.population / self.area

    @property
    def agreeableness(self):
        if not self.habitants :
            return 0
        return sum([person.agreeableness for person in self.habitants]) / self.population   # my first use of a list comprehension in python



class Base_graphe:
    """
    this is a parent class, we need its caracteristics in
    a child classes
    we wanted to create two graphics, but we did only one
    """
    def __init__(self):
        self.title = "graphe title"
        self.x_label = "X-axis label"
        self.y_label = "Y-axis label"
        self.grid = True

    def show(self, zones):
        x_values, y_values = self.xy_values(zones)
        plt.plot(x_values, y_values, '.')
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.title(self.title)
        plt.grid(self.grid)
        plt.show()

    def xy_values(self, zones):
        raise NotImplementedError




class Agreeableness_graph(Base_graphe):
    """
    this is the child class which inherited all his parent's
    attributes and methods
    we modified many things to adapt it to the type of our graph
    """
    def __init__(self):
        super().__init__()
        self.title = "nice people live in the countryside"
        self.x_label = "population density"
        self.y_label = "agreeableness"

    def xy_values(self, zones):
        x_values = [zone.density for zone in zones]
        y_values = [zone.agreeableness for zone in zones]
        return x_values, y_values



def main():

    with open("agents-100k.json", 'r') as f:
        data = f.read()
        data = loads(data)


    for agent_attribute in data :
        print(agent_attribute.items())
        longitude = agent_attribute.pop("longitude")
        latitude = agent_attribute.pop("latitude")
        position = Position(longitude, latitude)
        zone = Zone.zone_that_contains(position)
        agent = Agent(position, **agent_attribute)
        zone.add_inhabitants(agent)

    ag_graph = Agreeableness_graph()
    ag_graph.show(Zone.ZONE)




main()

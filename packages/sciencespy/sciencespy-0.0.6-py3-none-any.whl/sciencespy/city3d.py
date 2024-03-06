"""
Module dedicated to extract data stored within a 3D city model.

Delft University of Technology
Dr. Miguel Martin
"""

import json
from sciencespy.dom import *
from simplification.cutil import simplify_coords, simplify_coords_vw, simplify_coords_vwp
from shapely.geometry import Polygon
from pyproj import Proj, transform, Transformer
import pytz
from tzwhere import tzwhere
from enum import Enum
import numpy as np

from pint import UnitRegistry
ureg = UnitRegistry()
ureg.default_format = '.3f'
Q_ = ureg.Quantity

class CityModelFormatException(Exception):
    """
    Class of exception referring to the format of a 3D city model
    """
    pass

class CityModelCoordinateReferenceSystemException(Exception):
    """
    Class of exception referring to the format of a 3D city model
    """
    pass

class CityModelReferenceSystem(Enum):
    UNKNOWN = 0
    EPSG_7415 = 1
    CRS84 = 2

class CompressCoordinates():
    """
    Class used to compress coordinates
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def compress(self, x, y):
        """
        Compress the coordinates
        :param x: x-coordinates to compress
        :param y: y-coordinates to compress
        :return: compressed xy coordinates
        """
        pass

class CompressCoordinatesScaleTranslate(CompressCoordinates):
    """
    Class to compress coordinates based on the scale and translate of the map

    Attributes:
        xscale: scale of x-axis
        yscal: scale of y-axis
        xtranslate: translate of x-axis
        ytranslate: translate of y-axis
    """

    def __init__(self, xscale, yscale, zscale, xtranslate, ytranslate, ztranslate):
        """
        Construct the compression of coordinates based on the scale and translate
        :param xscale: scale of x-axis
        :param yscal: scale of y-axis
        :param zscale: scale of z-axis
        :param xtranslate: translate of x-axis
        :param ytranslate: translate of y-axis
        :param ztranslate: translate of z-axis
        """
        self.xscale = xscale
        self.yscale = yscale
        self.zscale = zscale
        self.xtranslate = xtranslate
        self.ytranslate = ytranslate
        self.ztranslate = ztranslate

    def compress(self, x, y, z):
        """
        Compress the coordinates
        :param x: x-coordinates to compress
        :param y: y-coordinates to compress
        :return: compressed xy coordinates
        """
        xc = [(x[n] - self.xtranslate) / self.xscale for n in range(0, len(x))]
        yc = [(y[n] - self.ytranslate) / self.yscale for n in range(0, len(y))]
        zc = [(z[n] - self.ztranslate) / self.zscale for n in range(0, len(z))]
        return xc, yc, zc

class DecompressCoordinates():
    """
    Class used to decompress coordinates
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def decompress(self, x, y, z):
        """
        Decompress the coordinates
        :param x: x-coordinates to decompress
        :param y: y-coordinates to decompress
        :param z: z-coordinates to decompress
        :return: decompressed xy coordinates
        """
        pass

class DecompressCoordinatesScaleTranslate(CompressCoordinates):
    """
    Class to decompress coordinates based on the scale and translate of the map

    Attributes:
        xscale: scale of x-axis
        yscal: scale of y-axis
        xtranslate: translate of x-axis
        ytranslate: translate of y-axis
    """

    def __init__(self, xscale, yscale, zscale, xtranslate, ytranslate, ztranslate):
        """
        Construct the decompression of coordinates based on the scale and translate
        :param xscale: scale of x-axis
        :param yscal: scale of y-axis
        :param zscale: scale of z-axis
        :param xtranslate: translate of x-axis
        :param ytranslate: translate of y-axis
        :param ztranslate: translate of z-axis
        """
        self.xscale = xscale
        self.yscale = yscale
        self.zscale = zscale
        self.xtranslate = xtranslate
        self.ytranslate = ytranslate
        self.ztranslate = ztranslate

    def decompress(self, x, y, z):
        """
        Decompress the coordinates
        :param x: x-coordinates to decompress
        :param y: y-coordinates to decompress
        :param z: z-coordinates to decompress
        :return: decompressed xyz coordinates
        """
        xd = [(x[n] * self.xscale) + self.xtranslate for n in range(0, len(x))]
        yd = [(y[n] * self.yscale) + self.ytranslate for n in range(0, len(y))]
        zd = [(z[n] * self.zscale) + self.ztranslate for n in range(0, len(z))]
        return xd, yd, zd

class CityModel():
    """
    Class representing a 3D city model
    """
    __metaclass__ = ABCMeta

    _city_model_data = []

    @abstractmethod
    def get_reference_system(self):
        """
        Get the reference system of the 3D city model.
        :return: the reference system
        """
        pass

    @abstractmethod
    def get_footprint(self, building_name):
        """
        Get the xyz-coordinates of the footprint of a building.
        :param building_name: name of the building.
        :return: the xyz-coordinates of the footprint.
        """
        pass

    @abstractmethod
    def get_location(self, building_name):
        """
        Get location of a building in the 3D city model.
        :param building_name: name of the building
        :return: the location of the building.
        """
        pass

    @abstractmethod
    def get_zones(self, building_name):
        """
        Get zones of a building in the 3D city model.
        :param building_name: name of the building
        :return: list of zones of the building.
        """
        pass


class CityJSON(CityModel):
    """
    Class representing a 3D city model with the CityJSON format (https://www.cityjson.org/)

    Attributes:
        lod: level of detail of the 3D city model expressed in CityJSON
    """

    @staticmethod
    def load(city_model_file, lod = 1.2):
        """
        Load a 3D city model using the CityJSON format.
        :param city_model_file: file containing the 3D city model expressed in CityJSON.
        :param lod: level of detail with which the 3D city model will be loaded
        :return: instance of the 3D city model expressed with CityJSON
        """
        city_model = CityJSON()
        with open(city_model_file, 'r') as f:
            city_model._city_model_data = json.load(f)
        city_model.lod = lod
        return city_model

    def get_reference_system(self):
        """
        Get the reference system of the 3D city model.
        :return: the reference system
        """
        if self._city_model_data['metadata']['referenceSystem'] == 'urn:ogc:def:crs:EPSG::7415':
            return CityModelReferenceSystem.EPSG_7415
        else:
            return CityModelReferenceSystem.UNKNOWN

    def get_decompressor(self):
        """
        Get decompressor of xyz-coordinates
        :return: the decompressor.
        """
        transform = self._city_model_data['transform']
        return DecompressCoordinatesScaleTranslate(transform["scale"][0], transform["scale"][1], transform["scale"][2],
                                                   transform["translate"][0], transform["translate"][1], transform["translate"][2])

    def get_footprint(self, building_name):
        """
        Get the xyz-coordinates of the footprint of a building.
        :param building_name: name of the building.
        :return: the xyz-coordinates of the footprint.
        """
        building_info = self._city_model_data['CityObjects'][building_name]
        building_geometries = self._city_model_data['CityObjects'][building_info['children'][0]]['geometry']
        city_model_vertices = self._city_model_data['vertices']
        city_model_metadata = self._city_model_data['metadata']

        point_indexes = building_geometries[0]['boundaries'][0][0][0]
        building_footprint = [city_model_vertices[n] for n in point_indexes]
        building_footprint.append(city_model_vertices[point_indexes[0]])
        xs, ys, zs = zip(*[point[0:3] for point in building_footprint])
        if self.get_reference_system() == CityModelReferenceSystem.EPSG_7415:
            decompressor = self.get_decompressor()
        else:
            raise CityModelCoordinateReferenceSystemException('The coordinate reference system is unknown.')
        return decompressor.decompress(xs, ys, zs)

    def get_location(self, building_name):
        """
        Get location of a building in the 3D city model.
        :param building_name: name of the building
        :return: the location of the building.
        """
        xs, ys, zs = self.get_footprint(building_name)
        if self.get_reference_system() == CityModelReferenceSystem.EPSG_7415:
            inProj = Proj(init='epsg:7415')
        else:
            raise CityModelCoordinateReferenceSystemException('The coordinate reference system is unknown.')
        polygon = Polygon([[xs[n], ys[n]] for n in range(len(xs))])
        outProj = Proj(init='epsg:4326')
        long, lat = transform(inProj, outProj, polygon.centroid.xy[0][0], polygon.centroid.xy[1][0])
        location = Location('location:' + building_name)
        location.latitude = Q_(lat, ureg.deg)
        location.longitude = Q_(long, ureg.deg)
        tz = tzwhere.tzwhere()
        location.timezone = pytz.timezone(tz.tzNameAt(lat, long))
        return location

    def get_zones(self, building_name):
        """
        Get zones of a building in the 3D city model.
        :param building_name: name of the building
        :param lod: level of detail of the building
        :return: list of zones of the building.
        """
        building_info = self._city_model_data['CityObjects'][building_name]
        building_geometries = self._city_model_data['CityObjects'][building_info['children'][0]]['geometry']
        city_model_vertices = self._city_model_data['vertices']
        for n in range(len(building_geometries)):
            if building_geometries[n]['lod'] == self.lod:
                building_geometry = building_geometries[n]
        building_vertices = building_geometry['boundaries']
        building_surface_semantics_values = building_geometry['semantics']['values'][0]
        decompressor = self.get_decompressor()
        xfp, yfp, zfp = self.get_footprint(building_name)
        min_x = min(xfp)
        min_y = min(yfp)
        min_z = min(zfp)
        zones = [Zone('zone:0')]
        n_roof_surfaces = 0
        roof_surfaces = []
        n_exterior_wall_surfaces = 0
        exterior_wall_surfaces = []
        ground_floor_surface = None
        for n in range(len(building_surface_semantics_values)):
            point_indexes = building_vertices[0][n][0]
            points = []
            for pindex in point_indexes:
                point = city_model_vertices[pindex]
                x, y, z = decompressor.decompress([point[0]], [point[1]], [point[2]])
                points.append(Point(x[0] - min_x, y[0] - min_y, z[0] - min_z))
            if building_geometry['semantics']['surfaces'][building_surface_semantics_values[n]]['type'] == 'GroundSurface':
                surface = Surface('zone:0:floor:0')
                surface.points = points
                ground_floor_surface = surface
            if building_geometry['semantics']['surfaces'][building_surface_semantics_values[n]]['type'] == 'RoofSurface':
                surface = Surface('zone:0:roof:' + str(n_roof_surfaces))
                surface.points = points
                n_roof_surfaces = n_roof_surfaces + 1
                roof_surfaces.append(surface)
            if building_geometry['semantics']['surfaces'][building_surface_semantics_values[n]]['type'] == 'WallSurface':
                surface = Surface('zone:0:extwall:' + str(n_exterior_wall_surfaces))
                surface.points = points
                n_exterior_wall_surfaces = n_exterior_wall_surfaces + 1
                exterior_wall_surfaces.append(surface)
        zones[0].ground_floor_surface = ground_floor_surface
        zones[0].roof_surfaces = roof_surfaces
        zones[0].exterior_wall_surfaces = exterior_wall_surfaces
        return zones


class GeoJSON(CityModel):
    """
    Class representing a 3D city model with the GeoJSON format (https://geojson.org/)
    """

    @staticmethod
    def load(city_model_file):
        """
        Load a 3D city model using the GeoJSON format.
        :param city_model_file: file containing the 3D city model expressed in GeoJSON.
        :return: instance of the 3D city model expressed with GeoJSON
        """
        city_model = GeoJSON()
        with open(city_model_file, 'r') as f:
            city_model._city_model_data = json.load(f)
        return city_model

    def get_reference_system(self):
        """
        Get the reference system of the 3D city model.
        :return: the reference system
        """
        if self._city_model_data['crs']['properties']['name'] == 'urn:ogc:def:crs:OGC:1.3:CRS84':
            return CityModelReferenceSystem.CRS84
        else:
            return CityModelReferenceSystem.UNKNOWN

    def get_footprint(self, building_name):
        """
        Get the xyz-coordinates of the footprint of a building.
        :param building_name: name of the building.
        :return: the xyz-coordinates of the footprint.
        """
        buildings_data = self._city_model_data['features']
        building_footprint = None
        for n in range(len(buildings_data)):
            if building_name == str(buildings_data[n]['properties']['OBJECTID']):
                building_footprint = buildings_data[n]['geometry']['coordinates']
                break
        building_footprint = np.asarray(building_footprint[0][0])
        x = building_footprint[:, 0]
        y = building_footprint[:, 1]
        z = building_footprint[:, 2]
        return x, y, z

    def get_location(self, building_name):
        """
        Get location of a building in the 3D city model.
        :param building_name: name of the building
        :return: the location of the building.
        """
        x, y, z = self.get_footprint(building_name)
        location = Location('location:' + building_name)
        location.latitude = Q_(np.mean(y), ureg.deg)
        location.longitude = Q_(np.mean(x), ureg.deg)
        tz = tzwhere.tzwhere()
        location.timezone = pytz.timezone(tz.tzNameAt(np.mean(y), np.mean(x)))
        return location

    def get_zones(self, building_name):
        """
        Get zones of a building in the 3D city model.
        :param building_name: name of the building
        :return: list of zones of the building.
        """
        buildings_data = self._city_model_data['features']
        building_height = 0.0
        building_footprint = None
        for n in range(len(buildings_data)):
            if building_name == str(buildings_data[n]['properties']['OBJECTID']):
                building_height = buildings_data[n]['properties']['Height']
                building_footprint = buildings_data[n]['geometry']['coordinates']
                break
        coordinates = np.array(building_footprint[0][0])
        lat = coordinates[:, 1]
        lon = coordinates[:, 0]
        transformer = None
        if self.get_reference_system() == CityModelReferenceSystem.CRS84:
            transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857")
        else:
            raise CityModelCoordinateReferenceSystemException('The coordinate reference system is unknown.')
        x, y = transformer.transform(lat, lon)
        x = x - min(x)
        y = y - min(y)
        zones = [Zone('zone:0')]
        roof_surface = Surface('zone:0:roof:0')
        exterior_wall_surfaces = []
        ground_floor_surface = Surface('zone:0:floor:0')
        N = len(x)
        for n in range(N - 1):
            exterior_wall_surface = Surface('zone:0:extwall:' + str(n))
            ground_floor_surface.points.append(Point(x[n], y[n], 0.0))
            roof_surface.points.append(Point(x[N - 1 - n], y[N - 1 - n], building_height))
            exterior_wall_surface.points.append(Point(x[n], y[n], 0.0))
            exterior_wall_surface.points.append(Point(x[n + 1], y[n + 1], 0.0))
            exterior_wall_surface.points.append(Point(x[n + 1], y[n + 1], building_height))
            exterior_wall_surface.points.append(Point(x[n], y[n], building_height))
            exterior_wall_surfaces.append(exterior_wall_surface)
        zones[0].ground_floor_surface = ground_floor_surface
        zones[0].roof_surfaces = [roof_surface]
        zones[0].exterior_wall_surfaces = exterior_wall_surfaces
        return zones


class BuildingFootprintSimplificationMethod():
    """
    Class representing a method of simplification of the building footprint
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def simplify_building_footprint(self, xs, ys):
        """
        Simplify the building footprint
        :param xs: x-coordinates of the building footprint expressed in engineering meters system
        :param ys: y-coordinates of the building footprint expressed in engineering meters system
        :return: simplified building footprint (i.e. modified x and y coordinates)
        """
        pass

class BuildingFootprintSimplificationMethodDouglasPeuker():
    """
    Class representing the simplification of the building footprint applying the Douglas-Peuker algorithm
    """
    __metaclass__ = ABCMeta

    def __init__(self, epsilon):
        """
        Construction of the Douglas-Peuker algorithm for simplifying the building footprint
        :param epsilon: epsilon parameter
        """
        self.epsilon = epsilon

    def simplify_building_footprint(self, xs, ys):
        """
        Simplify the building footprint
        :param xs: x-coordinates of the building footprint expressed in engineering meters system
        :param ys: y-coordinates of the building footprint expressed in engineering meters system
        :return: simplified building footprint (i.e. modified x and y coordinates)
        """
        building_footprint_2d = [[xs[n], ys[n]] for n in range(0, len(xs))]
        building_footprint_2d_simplified = simplify_coords(building_footprint_2d, self.epsilon)
        xss, yss = zip(*building_footprint_2d_simplified)
        return xss, yss

def extract_building_footprint(building_name, city_model, simplification_method = None):
    """
    Extract building footprint of a builing from the 3D city model.
    """
    xs, ys, zs = city_model.get_footprint(building_name)
    if not simplification_method is None:
        xs, ys = simplification_method.simplify_building_footprint(xs, ys)
    return xs, ys, zs

def extract_building_from_city_model(building_name, city_model):
    """
    Extract a building from a 3D city model
    :param building_name: name or ID of the building to extract
    :param city_model: the 3D city model
    :return: the building with its geometry and orientation
    """
    building = Building(building_name)
    building.zones = city_model.get_zones(building_name)
    return building

def extract_buildings_from_city_model(building_names, city_model):
    """
    Extract buildings from a 3D city model
    :param building_names: list of names or IDs of the buildings to extract
    :param lod: level of detailed of buildings to be extracted from the 3D city model
    :return: list of buildings
    """
    return [extract_building_from_city_model(bn, city_model) for bn in building_names]














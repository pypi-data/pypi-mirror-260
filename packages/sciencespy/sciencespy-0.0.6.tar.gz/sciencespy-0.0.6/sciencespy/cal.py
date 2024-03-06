"""
Module dedicated to calibration of an urban building energy model.

Delft University of Technology
Dr. Miguel Martin
"""

from abc import ABCMeta, abstractmethod

import torch
from eppy.modeleditor import IDF
import os
import platform
import numpy as np
import pandas as pd
import calendar
from enum import Enum
import json
import gpflow
import pickle
import pyro
import pyro.distributions as dist
from pyro.infer import MCMC, NUTS
import tensorflow as tf


from sklearn.metrics import mean_squared_error

from SALib.analyze import morris
from SALib.sample import morris as morris_sampler

from sciencespy.bem import *
from sciencespy.cosim import *
from sciencespy.dom import *
from sciencespy.utils import *

class CategoryParameterBuildingEnergyModel(Enum):
    """
    Enumeration of parameter caregories for a building energy model.
    """
    OCCUPANCY = 1
    LIGHTING = 2
    ELECTRIC_EQUIPMENT = 3
    INFILTRATION = 4
    WINDOW_TO_WALL_RATIO = 5
    WINDOW_THERMAL_RESISTANCE = 6
    WINDOW_SHGC = 7
    WALL_THERMAL_RESISTANCE = 8
    WALL_DENSITY = 9
    WALL_SPECIFIC_HEAT_CAPACITY = 10
    WALL_THERMAL_EMISSIVITY = 11
    WALL_THERMAL_ABSORPTIVITY = 12
    HEATING_TEMPERATURE_SETPOINT = 13
    COOLING_TEMPERATURE_SETPOINT = 14
    MECHANICAL_VENTILATION = 15

class ParameterBuildingEnergyModel():
    """
    Class representing the parameter of a building energy model to be calibrated.

    Attributes:
        name: name of the parameter
        _value: value of the parameter
    """
    __metaclass__ = ABCMeta

    def __init__(self, name = None):
        """
        :param name: name of the parameter.
        """
        self.name = name

    @abstractmethod
    def get_category(self):
        """
        :return: category of parameter of the building energy model.
        """
        pass

    @abstractmethod
    def get_value(self):
        """
        :return: value of the parameter
        """
        pass

    @abstractmethod
    def set_value(self, value):
        """
        :param value: value of the parameter.
        """
        pass

class ParameterEnergyPlusModel(ParameterBuildingEnergyModel):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """
    __metaclass__ = ABCMeta

    def __init__(self, name = None, idf = None):
        """
        :param name: name of the parameter.
        :param idf: list of IDF objects representing the EnergyPlus model.
        """
        ParameterBuildingEnergyModel.__init__(self, name)
        self.idf = idf

    def get_value(self):
        """
        :return: value of the parameter
        """
        object_name = self.name.split(':')[0]
        category_name = self.name.split(':')[1]
        for obj in self.idf.idfobjects[self.get_classname()]:
            if self.get_name(obj) == object_name and category_name == self.get_category_name():
                return self.get_field_value(obj)
        return None

    def set_value(self, value):
        """
        :param value: value of the parameter.
        """
        object_name = self.name.split(':')[0]
        category_name = self.name.split(':')[1]
        for obj in self.idf.idfobjects[self.get_classname()]:
            if self.get_name(obj) == object_name and category_name == self.get_category_name():
                self.update(obj, value)

    @abstractmethod
    def get_classname(self):
        """
        :return: name of the class of the EnergyPlus object
        """
        pass

    @abstractmethod
    def get_category_name(self):
        """
        :return: name of the category of the parameter
        """
        pass

    @abstractmethod
    def get_name(self, obj):
        """
        :param obj: EnergyPlus object.
        :return: name of the object.
        """
        pass

    @abstractmethod
    def get_field_value(self, obj):
        """
        :param obj: EnergyPlus object
        :return: desired field value.
        """
        pass

    @abstractmethod
    def update(self, obj, value):
        """
        Update IDF object accordingly.
        :param obj: EnergyPlus object
        :param value: value to be set.
        """
        pass

class ParameterEnergyPlusModelOccupancy(ParameterEnergyPlusModel):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    def __init__(self, name = None, idf = None):
        """
        :param name: name of the parameter.
        :param idf: list of IDF objects representing the EnergyPlus model.
        """
        ParameterEnergyPlusModel.__init__(self, name, idf)

    def get_category(self):
        """
        :return: category of parameter of the building energy model.
        """
        return CategoryParameterBuildingEnergyModel.OCCUPANCY

    def get_classname(self):
        """
        :return: name of the class of the EnergyPlus object
        """
        return 'PEOPLE'

    def get_category_name(self):
        """
        :return:
        """
        return 'Occupancy'

    def get_name(self, obj):
        """
        :param obj: EnergyPlus object.
        :return: name of the object.
        """
        return obj.Name

    def get_field_value(self, obj):
        """
        :param obj: EnergyPlus object
        :return: desired field value.
        """
        return float(obj.Number_of_People)

    def update(self, obj, value):
        """
        Update IDF object accordingly.
        :param obj: EnergyPlus object
        :param value: value to be set.
        """
        obj.Number_of_People_Calculation_Method = 'People'
        obj.Number_of_People = "{:.2f}".format(round(value, 2))
        obj.People_per_Floor_Area = ''
        obj.Floor_Area_per_Person = ''


class ParameterEnergyPlusModelLighting(ParameterEnergyPlusModel):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    def __init__(self, name = None, idf = None):
        """
        :param name: name of the parameter.
        :param idf: list of IDF objects representing the EnergyPlus model.
        """
        ParameterEnergyPlusModel.__init__(self, name, idf)

    def get_category(self):
        """
        :return: category of parameter of the building energy model.
        """
        return CategoryParameterBuildingEnergyModel.LIGHTING

    def get_classname(self):
        """
        :return: name of the class of the EnergyPlus object
        """
        return 'LIGHTS'

    def get_category_name(self):
        """
        :return:
        """
        return 'Lighting Level'

    def get_name(self, obj):
        """
        :param obj: EnergyPlus object.
        :return: name of the object.
        """
        return obj.Name

    def get_field_value(self, obj):
        """
        :param obj: EnergyPlus object
        :return: desired field value.
        """
        return float(obj.Lighting_Level)

    def update(self, obj, value):
        """
        Update IDF object accordingly.
        :param obj: EnergyPlus object
        :param value: value to be set.
        """
        obj.Design_Level_Calculation_Method = 'LightingLevel'
        obj.Lighting_Level = "{:.2f}".format(round(value, 2))
        obj.Watts_per_Zone_Floor_Area = ''
        obj.Watts_per_Person = ''


class ParameterEnergyPlusModelElectricEquipment(ParameterEnergyPlusModel):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    def __init__(self, name = None, idf = None):
        """
        :param name: name of the parameter.
        :param idf: list of IDF objects representing the EnergyPlus model.
        """
        ParameterEnergyPlusModel.__init__(self, name, idf)

    def get_category(self):
        """
        :return: category of parameter of the building energy model.
        """
        return CategoryParameterBuildingEnergyModel.ELECTRIC_EQUIPMENT

    def get_classname(self):
        """
        :return: name of the class of the EnergyPlus object
        """
        return 'ELECTRICEQUIPMENT'

    def get_category_name(self):
        """
        :return:
        """
        return 'Electric Equipment Level'

    def get_name(self, obj):
        """
        :param obj: EnergyPlus object.
        :return: name of the object.
        """
        return obj.Name

    def get_field_value(self, obj):
        """
        :param obj: EnergyPlus object
        :return: desired field value.
        """
        return float(obj.Design_Level)

    def update(self, obj, value):
        """
        Update IDF object accordingly.
        :param obj: EnergyPlus object
        :param value: value to be set.
        """
        obj.Design_Level_Calculation_Method = 'EquipmentLevel'
        obj.Design_Level = "{:.2f}".format(round(value, 2))
        obj.Watts_per_Zone_Floor_Area = ''
        obj.Watts_per_Person = ''


class ParameterEnergyPlusModelInfiltration(ParameterEnergyPlusModel):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    def __init__(self, name = None, idf = None):
        """
        :param name: name of the parameter.
        :param idf: list of IDF objects representing the EnergyPlus model.
        """
        ParameterEnergyPlusModel.__init__(self, name, idf)

    def get_category(self):
        """
        :return: category of parameter of the building energy model.
        """
        return CategoryParameterBuildingEnergyModel.INFILTRATION

    def get_classname(self):
        """
        :return: name of the class of the EnergyPlus object
        """
        return 'ZONEINFILTRATION:DESIGNFLOWRATE'

    def get_category_name(self):
        """
        :return:
        """
        return 'Infiltration Flow Rate'

    def get_name(self, obj):
        """
        :param obj: EnergyPlus object.
        :return: name of the object.
        """
        return obj.Name

    def get_field_value(self, obj):
        """
        :param obj: EnergyPlus object
        :return: desired field value.
        """
        return float(obj.Design_Flow_Rate)

    def update(self, obj, value):
        """
        Update IDF object accordingly.
        :param obj: EnergyPlus object
        :param value: value to be set.
        """
        obj.Design_Flow_Rate_Calculation_Method = 'Flow/Zone'
        obj.Design_Flow_Rate = "{:.2f}".format(round(value, 2))
        obj.Flow_Rate_per_Floor_Area = ''
        obj.Flow_Rate_per_Exterior_Surface_Area = ''
        obj.Air_Changes_per_Hour = ''

class FactorySurface():
    """"
    Class used to create surface from IDF object.

    Attributes:
        surface_idfobject: the IDF object containing information of the surface.
    """


    __metaclass__ = ABCMeta

    def __init__(self, surface_idfobject):
        """
        :param surface_idfobject: the IDF object containing information of the surface.
        """
        self.surface_idfobject = surface_idfobject

    def get_surface(self):
        """
        :return: the corresponding dom.Surface object.
        """
        coords_position_0 = self.get_position_initial_x()
        coords = [None, None, None]
        points = []
        for n, field in enumerate(self.surface_idfobject.obj):
            if n >= coords_position_0 and str(field).strip():
                coords[(n - coords_position_0) % 3] = float(field)
                if not any(coord is None for coord in coords):
                    points.append(coords)
                    coords = [None, None, None]
        return Surface(self.surface_idfobject.Name, np.array(points))


    @abstractmethod
    def get_position_initial_x(self):
        """
        :return: the position in the IDF object of the first x-coordinate.
        """
        pass

class FactorySurfaceExteriorWall(FactorySurface):
    """"
    Class used to create surface from IDF object.

    Attributes:
        surface_idfobject: the IDF object containing information of the surface.
    """

    def __init__(self, surface_idfobject):
        """
        :param surface_idfobject: the IDF object containing information of the surface.
        """
        FactorySurface.__init__(self, surface_idfobject)


    def get_position_initial_x(self):
        """
        :return: the position in the IDF object of the first x-coordinate.
        """
        return 12


class FactorySurfaceExteriorWindow(FactorySurface):
    """"
    Class used to create surface from IDF object.

    Attributes:
        surface_idfobject: the IDF object containing information of the surface.
    """

    def __init__(self, surface_idfobject):
        """
        :param surface_idfobject: the IDF object containing information of the surface.
        """
        FactorySurface.__init__(self, surface_idfobject)

    def get_position_initial_x(self):
        """
        :return: the position in the IDF object of the first x-coordinate.
        """
        return 10

def add_imaginary_exterior_window_layer(idf):
    """
    Add an imaginary exterior window layer to the IDF
    :param idf: IDF file contain
    :return: IDF object corresponding to the imaginary exterior window layer.
    """
    is_imaginary_exterior_window = False
    for obj in idf.idfobjects['WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM']:
        if obj.Name == 'Imaginary Exterior Window Layer':
            is_imaginary_exterior_window = True
            break
    if not is_imaginary_exterior_window:
        idf.newidfobject('WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM')
        materials = idf.idfobjects['WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM']
        exterior_window_layer = materials[-1]
        exterior_window_layer.Name = 'Imaginary Exterior Window Layer'
        exterior_window_layer.UFactor = '1.5'
        exterior_window_layer.Solar_Heat_Gain_Coefficient = '0.7'
        exterior_window_layer.Visible_Transmittance = ''
        idf.newidfobject("CONSTRUCTION")
        constructions = idf.idfobjects["CONSTRUCTION"]
        constructions[-1].Name = 'Imaginary Exterior Window'
        constructions[-1].Outside_Layer = 'Imaginary Exterior Window Layer'
    else:
        for obj in idf.idfobjects['WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM']:
            if obj.Name == 'Imaginary Exterior Window Layer':
                exterior_window_layer = obj
    for obj in idf.idfobjects["FENESTRATIONSURFACE:DETAILED"]:
        if obj.Surface_Type == 'Window':
            obj.Construction_Name = 'Imaginary Exterior Window'
    return exterior_window_layer


class ParameterEnergyPlusModelWindowToWallRatio(ParameterEnergyPlusModel):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    def __init__(self, name = None, idf = None):
        """
        :param name: name of the parameter.
        :param idf: list of IDF objects representing the EnergyPlus model.
        """
        ParameterEnergyPlusModel.__init__(self, name, idf)

    def get_category(self):
        """
        :return: category of parameter of the building energy model.
        """
        return CategoryParameterBuildingEnergyModel.WINDOW_TO_WALL_RATIO

    def get_value(self):
        """
        :return: value of the parameter
        """
        total_wall_surface = 0
        total_window_surface = 0
        for obj in self.idf.idfobjects["BUILDINGSURFACE:DETAILED"]:
            if obj.Surface_Type == 'Wall' and obj.Sun_Exposure == 'SunExposed' and obj.Wind_Exposure == 'WindExposed':
                total_wall_surface += FactorySurfaceExteriorWall(obj).get_surface().get_area()
        for obj in self.idf.idfobjects["FENESTRATIONSURFACE:DETAILED"]:
            if obj.Surface_Type == 'Window':
                total_window_surface += FactorySurfaceExteriorWindow(obj).get_surface().get_area()
        return total_window_surface.m / total_wall_surface.m

    def set_value(self, value):
        """
        :param value: value of the parameter.
        """
        window_surfaces = self.idf.idfobjects["FENESTRATIONSURFACE:DETAILED"]
        while len(window_surfaces) > 0:
            window_surfaces.pop(0)
        if value > 0:
            for obj in self.idf.idfobjects["BUILDINGSURFACE:DETAILED"]:
                if obj.Surface_Type == 'Wall' and obj.Sun_Exposure == 'SunExposed' and obj.Wind_Exposure == 'WindExposed':
                    wall_surface = FactorySurfaceExteriorWall(obj).get_surface()
                    window_surface = wall_surface.crop(value).bounding_box()
                    self.idf.newidfobject("FENESTRATIONSURFACE:DETAILED")
                    window_surface_idf = self.idf.idfobjects["FENESTRATIONSURFACE:DETAILED"][-1]
                    window_surface_idf.Name = obj.Name + ":Window"
                    window_surface_idf.Surface_Type = 'Window'
                    window_surface_idf.Building_Surface_Name = obj.Name
                    window_surface_idf.View_Factor_to_Ground = 'autocalculate'
                    window_surface_idf.Multiplier = '1'
                    num_vertices = 4
                    window_surface_idf.Number_of_Vertices = str(num_vertices)
                    for n_vertice in range(num_vertices):
                        window_surface_idf["Vertex_" + str(n_vertice + 1) + "_Xcoordinate"] = str(window_surface.points[n_vertice][0])
                        window_surface_idf["Vertex_" + str(n_vertice + 1) + "_Ycoordinate"] = str(window_surface.points[n_vertice][1])
                        window_surface_idf["Vertex_" + str(n_vertice + 1) + "_Zcoordinate"] = str(window_surface.points[n_vertice][2])
            add_imaginary_exterior_window_layer(self.idf)


class ParameterEnergyPlusModelExteriorWindow(ParameterEnergyPlusModel):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    __metaclass__ = ABCMeta

    def __init__(self, name = None, idf = None):
        ParameterEnergyPlusModel.__init__(self, name, idf)

    def set_value(self, value):
        exterior_window_layer = add_imaginary_exterior_window_layer(self.idf)
        self.update(exterior_window_layer, value)


class ParameterEnergyPlusModelWindowThermalResistance(ParameterEnergyPlusModelExteriorWindow):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    def __init__(self, name = None, idf = None):
        """
        :param name: name of the parameter.
        :param idf: list of IDF objects representing the EnergyPlus model.
        """
        ParameterEnergyPlusModelExteriorWindow.__init__(self, name, idf)

    def get_category(self):
        """
        :return: category of parameter of the building energy model.
        """
        return CategoryParameterBuildingEnergyModel.WINDOW_THERMAL_RESISTANCE

    def get_classname(self):
        """
        :return: name of the class of the EnergyPlus object
        """
        return 'WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM'

    def get_category_name(self):
        """
        :return:
        """
        return 'Window Thermal Resistance'

    def get_name(self, obj):
        """
        :param obj: EnergyPlus object.
        :return: name of the object.
        """
        return obj.Name

    def get_field_value(self, obj):
        """
        :param obj: EnergyPlus object
        :return: desired field value.
        """
        return float(obj.UFactor)

    def update(self, obj, value):
        """
        Update IDF object accordingly.
        :param obj: EnergyPlus object
        :param value: value to be set.
        """
        obj.UFactor = "{:.2f}".format(round(value, 2))

class ParameterEnergyPlusModelWindowSolarHeatGainCoefficient(ParameterEnergyPlusModelExteriorWindow):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    def __init__(self, name = None, idf = None):
        """
        :param name: name of the parameter.
        :param idf: list of IDF objects representing the EnergyPlus model.
        """
        ParameterEnergyPlusModelExteriorWindow.__init__(self, name, idf)

    def get_category(self):
        """
        :return: category of parameter of the building energy model.
        """
        return CategoryParameterBuildingEnergyModel.WINDOW_SHGC

    def get_classname(self):
        """
        :return: name of the class of the EnergyPlus object
        """
        return 'WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM'

    def get_category_name(self):
        """
        :return:
        """
        return 'Window Solar Heat Gain Coefficient'

    def get_name(self, obj):
        """
        :param obj: EnergyPlus object.
        :return: name of the object.
        """
        return obj.Name

    def get_field_value(self, obj):
        """
        :param obj: EnergyPlus object
        :return: desired field value.
        """
        return float(obj.Solar_Heat_Gain_Coefficient)

    def update(self, obj, value):
        """
        Update IDF object accordingly.
        :param obj: EnergyPlus object
        :param value: value to be set.
        """
        obj.Solar_Heat_Gain_Coefficient = "{:.2f}".format(round(value, 2))

class ParameterEnergyPlusModelExteriorWall(ParameterEnergyPlusModel):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    __metaclass__ = ABCMeta

    def __init__(self, name = None, idf = None):
        ParameterEnergyPlusModel.__init__(self, name, idf)

    def set_value(self, value):
        is_imaginary_exterior_wall = False
        for obj in self.idf.idfobjects['MATERIAL']:
            if obj.Name == 'Imaginary Exterior Wall Outer Layer' or obj.Name == 'Imaginary Exterior Wall Inner Layer':
                is_imaginary_exterior_wall = True
                break
        if not is_imaginary_exterior_wall:
            self.idf.newidfobject("MATERIAL")
            materials = self.idf.idfobjects["MATERIAL"]
            exterior_wall_outer_layer = materials[-1]
            exterior_wall_outer_layer.Name = 'Imaginary Exterior Wall Outer Layer'
            exterior_wall_outer_layer.Roughness = 'MediumSmooth'
            exterior_wall_outer_layer.Thickness = 0.5
            exterior_wall_outer_layer.Conductivity = 0.1
            exterior_wall_outer_layer.Density = 500
            exterior_wall_outer_layer.Specific_Heat = 1000
            exterior_wall_outer_layer.Thermal_Absorptance = 0.9
            exterior_wall_outer_layer.Solar_Absorptance = 0.7
            exterior_wall_outer_layer.Visible_Absorptance = 0.7
            self.idf.newidfobject("MATERIAL")
            materials = self.idf.idfobjects["MATERIAL"]
            exterior_wall_inner_layer = materials[-1]
            exterior_wall_inner_layer.Name = 'Imaginary Exterior Wall Inner Layer'
            exterior_wall_inner_layer.Roughness = 'MediumSmooth'
            exterior_wall_inner_layer.Thickness = 0.5
            exterior_wall_inner_layer.Conductivity = 0.1
            exterior_wall_inner_layer.Density = 500
            exterior_wall_inner_layer.Specific_Heat = 1000
            exterior_wall_inner_layer.Thermal_Absorptance = 0.9
            exterior_wall_inner_layer.Solar_Absorptance = 0.7
            exterior_wall_inner_layer.Visible_Absorptance = 0.7
            self.idf.newidfobject("CONSTRUCTION")
            constructions = self.idf.idfobjects["CONSTRUCTION"]
            constructions[-1].Name = 'Imaginary Exterior Wall'
            constructions[-1].Outside_Layer = 'Imaginary Exterior Wall Outer Layer'
            constructions[-1].Layer_2 = 'Imaginary Exterior Wall Inner Layer'
            for obj in self.idf.idfobjects["BUILDINGSURFACE:DETAILED"]:
                if obj.Surface_Type == 'Wall' and obj.Sun_Exposure == 'SunExposed' and obj.Wind_Exposure == 'WindExposed':
                    obj.Construction_Name = 'Imaginary Exterior Wall'
        else:
            for obj in self.idf.idfobjects["MATERIAL"]:
                if obj.Name == 'Imaginary Exterior Wall Outer Layer':
                    exterior_wall_outer_layer = obj
                elif obj.Name == 'Imaginary Exterior Wall Inner Layer':
                    exterior_wall_inner_layer = obj
        self.update(exterior_wall_outer_layer, value)
        self.update(exterior_wall_inner_layer, value)

class ParameterEnergyPlusModelWallThermalResistance(ParameterEnergyPlusModelExteriorWall):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    def __init__(self, name = None, idf = None):
        """
        :param name: name of the parameter.
        :param idf: list of IDF objects representing the EnergyPlus model.
        """
        ParameterEnergyPlusModel.__init__(self, name, idf)

    def get_category(self):
        """
        :return: category of parameter of the building energy model.
        """
        return CategoryParameterBuildingEnergyModel.WALL_THERMAL_RESISTANCE

    def get_classname(self):
        """
        :return: name of the class of the EnergyPlus object
        """
        return 'MATERIAL'

    def get_category_name(self):
        """
        :return:
        """
        return 'Wall Thermal Resistance'

    def get_name(self, obj):
        """
        :param obj: EnergyPlus object.
        :return: name of the object.
        """
        return obj.Name

    def get_field_value(self, obj):
        """
        :param obj: EnergyPlus object
        :return: desired field value.
        """
        return 1 / float(obj.Conductivity)

    def update(self, obj, value):
        """
        Update IDF object accordingly.
        :param obj: EnergyPlus object
        :param value: value to be set.
        """
        obj.Conductivity = "{:.2f}".format(round(1 / value, 2))

class ParameterEnergyPlusModelWallDensity(ParameterEnergyPlusModelExteriorWall):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    def __init__(self, name = None, idf = None):
        """
        :param name: name of the parameter.
        :param idf: list of IDF objects representing the EnergyPlus model.
        """
        ParameterEnergyPlusModelExteriorWall.__init__(self, name, idf)

    def get_category(self):
        """
        :return: category of parameter of the building energy model.
        """
        return CategoryParameterBuildingEnergyModel.WALL_DENSITY

    def get_classname(self):
        """
        :return: name of the class of the EnergyPlus object
        """
        return 'MATERIAL'

    def get_category_name(self):
        """
        :return:
        """
        return 'Wall Density'

    def get_name(self, obj):
        """
        :param obj: EnergyPlus object.
        :return: name of the object.
        """
        return obj.Name

    def get_field_value(self, obj):
        """
        :param obj: EnergyPlus object
        :return: desired field value.
        """
        return float(obj.Density)

    def update(self, obj, value):
        """
        Update IDF object accordingly.
        :param obj: EnergyPlus object
        :param value: value to be set.
        """
        obj.Density = str(round(value))

class ParameterEnergyPlusModelWallSpecificHeatCapacity(ParameterEnergyPlusModelExteriorWall):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    def __init__(self, name = None, idf = None):
        """
        :param name: name of the parameter.
        :param idf: list of IDF objects representing the EnergyPlus model.
        """
        ParameterEnergyPlusModelExteriorWall.__init__(self, name, idf)

    def get_category(self):
        """
        :return: category of parameter of the building energy model.
        """
        return CategoryParameterBuildingEnergyModel.WALL_SPECIFIC_HEAT_CAPACITY

    def get_classname(self):
        """
        :return: name of the class of the EnergyPlus object
        """
        return 'MATERIAL'

    def get_category_name(self):
        """
        :return:
        """
        return 'Wall Specific Heat Capacity'

    def get_name(self, obj):
        """
        :param obj: EnergyPlus object.
        :return: name of the object.
        """
        return obj.Name

    def get_field_value(self, obj):
        """
        :param obj: EnergyPlus object
        :return: desired field value.
        """
        return float(obj.Specific_Heat)

    def update(self, obj, value):
        """
        Update IDF object accordingly.
        :param obj: EnergyPlus object
        :param value: value to be set.
        """
        obj.Specific_Heat = str(round(value))

class ParameterEnergyPlusModelWallThermalEmissivity(ParameterEnergyPlusModelExteriorWall):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    def __init__(self, name=None, idf=None):
        """
        :param name: name of the parameter.
        :param idf: list of IDF objects representing the EnergyPlus model.
        """
        ParameterEnergyPlusModelExteriorWall.__init__(self, name, idf)

    def get_category(self):
        """
        :return: category of parameter of the building energy model.
        """
        return CategoryParameterBuildingEnergyModel.WALL_THERMAL_EMISSIVITY

    def get_classname(self):
        """
        :return: name of the class of the EnergyPlus object
        """
        return 'MATERIAL'

    def get_category_name(self):
        """
        :return:
        """
        return 'Wall Thermal Emissivity'

    def get_name(self, obj):
        """
        :param obj: EnergyPlus object.
        :return: name of the object.
        """
        return obj.Name

    def get_field_value(self, obj):
        """
        :param obj: EnergyPlus object
        :return: desired field value.
        """
        return float(obj.Thermal_Absorptance)

    def update(self, obj, value):
        """
        Update IDF object accordingly.
        :param obj: EnergyPlus object
        :param value: value to be set.
        """
        if obj.Name == 'Imaginary Exterior Wall Outer Layer':
            obj.Thermal_Absorptance = "{:.2f}".format(round(value, 2))

class ParameterEnergyPlusModelWallThermalAbsorptivity(ParameterEnergyPlusModelExteriorWall):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    def __init__(self, name=None, idf=None):
        """
        :param name: name of the parameter.
        :param idf: list of IDF objects representing the EnergyPlus model.
        """
        ParameterEnergyPlusModelExteriorWall.__init__(self, name, idf)

    def get_category(self):
        """
        :return: category of parameter of the building energy model.
        """
        return CategoryParameterBuildingEnergyModel.WALL_THERMAL_ABSORPTIVITY

    def get_classname(self):
        """
        :return: name of the class of the EnergyPlus object
        """
        return 'MATERIAL'

    def get_category_name(self):
        """
        :return:
        """
        return 'Wall Thermal Absorptivity'

    def get_name(self, obj):
        """
        :param obj: EnergyPlus object.
        :return: name of the object.
        """
        return obj.Name

    def get_field_value(self, obj):
        """
        :param obj: EnergyPlus object
        :return: desired field value.
        """
        return float(obj.Solar_Absorptance)

    def update(self, obj, value):
        """
        Update IDF object accordingly.
        :param obj: EnergyPlus object
        :param value: value to be set.
        """
        if obj.Name == 'Imaginary Exterior Wall Outer Layer':
            obj.Solar_Absorptance = "{:.2f}".format(round(value, 2))

class ParameterEnergyPlusModelHeatingTemperatureSetpoint(ParameterEnergyPlusModel):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    def __init__(self, name = None, idf = None):
        """
        :param name: name of the parameter.
        :param idf: list of IDF objects representing the EnergyPlus model.
        """
        ParameterEnergyPlusModel.__init__(self, name, idf)

    def get_category(self):
        """
        :return: category of parameter of the building energy model.
        """
        return CategoryParameterBuildingEnergyModel.HEATING_TEMPERATURE_SETPOINT

    def get_classname(self):
        """
        :return: name of the class of the EnergyPlus object
        """
        return 'HVACTEMPLATE:THERMOSTAT'

    def get_category_name(self):
        """
        :return:
        """
        return 'Heating Setpoint'

    def get_name(self, obj):
        """
        :param obj: EnergyPlus object.
        :return: name of the object.
        """
        return obj.Name

    def get_field_value(self, obj):
        """
        :param obj: EnergyPlus object
        :return: desired field value.
        """
        return float(obj.Constant_Heating_Setpoint)

    def update(self, obj, value):
        """
        Update IDF object accordingly.
        :param obj: EnergyPlus object
        :param value: value to be set.
        """
        obj.Heating_Setpoint_Schedule_Name = ''
        obj.Constant_Heating_Setpoint = "{:.2f}".format(round(value, 2))


class ParameterEnergyPlusModelCoolingTemperatureSetpoint(ParameterEnergyPlusModel):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    def __init__(self, name = None, idf = None):
        """
        :param name: name of the parameter.
        :param idf: list of IDF objects representing the EnergyPlus model.
        """
        ParameterEnergyPlusModel.__init__(self, name, idf)

    def get_category(self):
        """
        :return: category of parameter of the building energy model.
        """
        return CategoryParameterBuildingEnergyModel.COOLING_TEMPERATURE_SETPOINT

    def get_classname(self):
        """
        :return: name of the class of the EnergyPlus object
        """
        return 'HVACTEMPLATE:THERMOSTAT'

    def get_category_name(self):
        """
        :return:
        """
        return 'Cooling Setpoint'

    def get_name(self, obj):
        """
        :param obj: EnergyPlus object.
        :return: name of the object.
        """
        return obj.Name

    def get_field_value(self, obj):
        """
        :param obj: EnergyPlus object
        :return: desired field value.
        """
        return float(obj.Constant_Cooling_Setpoint)

    def update(self, obj, value):
        """
        Update IDF object accordingly.
        :param obj: EnergyPlus object
        :param value: value to be set.
        """
        obj.Cooling_Setpoint_Schedule_Name = ''
        obj.Constant_Cooling_Setpoint = "{:.2f}".format(round(value, 2))


class ParameterEnergyPlusModelMechanicalVentilation(ParameterEnergyPlusModel):
    """
    Class representing the parameter of an EnergyPlus model to be calibrated.

    Attributes:
        name: name of the parameter
        idf: list of IDF objects representing the EnergyPlus model.
    """

    def __init__(self, name = None, idf = None):
        """
        :param name: name of the parameter.
        :param idf: list of IDF objects representing the EnergyPlus model.
        """
        ParameterEnergyPlusModel.__init__(self, name, idf)

    def get_category(self):
        """
        :return: category of parameter of the building energy model.
        """
        return CategoryParameterBuildingEnergyModel.MECHANICAL_VENTILATION

    def get_classname(self):
        """
        :return: name of the class of the EnergyPlus object
        """
        return 'HVACTEMPLATE:ZONE:IDEALLOADSAIRSYSTEM'

    def get_category_name(self):
        """
        :return:
        """
        return 'Mechanical Ventilation'

    def get_name(self, obj):
        """
        :param obj: EnergyPlus object.
        :return: name of the object.
        """
        return obj.Zone_Name

    def get_field_value(self, obj):
        """
        :param obj: EnergyPlus object
        :return: desired field value.
        """
        return float(obj.Outdoor_Air_Flow_Rate_per_Zone)

    def update(self, obj, value):
        """
        Update IDF object accordingly.
        :param obj: EnergyPlus object
        :param value: value to be set.
        """
        obj.Outdoor_Air_Method = 'Flow/Zone'
        obj.Outdoor_Air_Flow_Rate_per_Person = ''
        obj.Outdoor_Air_Flow_Rate_per_Zone_Floor_Area = ''
        obj.Outdoor_Air_Flow_Rate_per_Zone = "{:.2f}".format(round(value, 2))



class ProxyBuildingEnergyModel():
    """
    Class representing the proxy of a building energy model to be calibrated.

    Attributes:
        name: the name of the building energy model
        _parameters : list of parameters of the building energy model
    """
    __metaclass__ = ABCMeta

    def __init__(self, name):
        """
        :param name: name of the building energy model
        """
        self.name = name
        self._parameters = []
        self._parameters.extend(self.create_parameters(CategoryParameterBuildingEnergyModel.OCCUPANCY))
        self._parameters.extend(self.create_parameters(CategoryParameterBuildingEnergyModel.LIGHTING))
        self._parameters.extend(self.create_parameters(CategoryParameterBuildingEnergyModel.ELECTRIC_EQUIPMENT))
        self._parameters.extend(self.create_parameters(CategoryParameterBuildingEnergyModel.INFILTRATION))
        self._parameters.extend(self.create_parameters(CategoryParameterBuildingEnergyModel.WINDOW_TO_WALL_RATIO))
        self._parameters.extend(self.create_parameters(CategoryParameterBuildingEnergyModel.WINDOW_THERMAL_RESISTANCE))
        self._parameters.extend(self.create_parameters(CategoryParameterBuildingEnergyModel.WINDOW_SHGC))
        self._parameters.extend(self.create_parameters(CategoryParameterBuildingEnergyModel.WALL_THERMAL_RESISTANCE))
        self._parameters.extend(self.create_parameters(CategoryParameterBuildingEnergyModel.WALL_DENSITY))
        self._parameters.extend(self.create_parameters(CategoryParameterBuildingEnergyModel.WALL_SPECIFIC_HEAT_CAPACITY))
        self._parameters.extend(self.create_parameters(CategoryParameterBuildingEnergyModel.WALL_THERMAL_EMISSIVITY))
        self._parameters.extend(self.create_parameters(CategoryParameterBuildingEnergyModel.WALL_THERMAL_ABSORPTIVITY))
        self._parameters.extend(self.create_parameters(CategoryParameterBuildingEnergyModel.HEATING_TEMPERATURE_SETPOINT))
        self._parameters.extend(self.create_parameters(CategoryParameterBuildingEnergyModel.COOLING_TEMPERATURE_SETPOINT))
        self._parameters.extend(self.create_parameters(CategoryParameterBuildingEnergyModel.MECHANICAL_VENTILATION))

    def get_parameters(self, category):
        """
        :param category: category of parameter.
        :return: list of parameters corresponding to the category.
        """
        parameters = []
        for p in self._parameters:
            if p.get_category() == category:
                parameters.append(p)
        return parameters

    def get_parameter_values(self, names):
        """
        :param names: list of parameter names.
        :return: list of parameter values.
        """
        values = []
        for p in self._parameters:
            if p.name in names:
                values.append(p.get_value())
        return values

    def set_parameters(self, names, values):
        """
        Set parameters of the building energy model.
        :param names: list of parameter names.
        :param values: list of parameter values.
        """
        priority = [CategoryParameterBuildingEnergyModel.WINDOW_TO_WALL_RATIO]
        for n, name in enumerate(names):
            for param in self._parameters:
                if param.name == name and param.get_category() in priority:
                    param.set_value(values[n])
        for n, name in enumerate(names):
            for param in self._parameters:
                if param.name == name and not param.get_category() in priority:
                    param.set_value(values[n])
        self.save()


    @abstractmethod
    def create_parameters(self, category):
        """
        Create parameters of a certain category.

        :param category: category of parameter.
        :return: list of parameters corresponding to the category.
        """
        pass

    @abstractmethod
    def save(self):
        """
        Save the building energy model after setting parameters.
        """
        pass


class ProxyEnergyPlusModel(ProxyBuildingEnergyModel):
    """
    Class representing the proxy of an EnergyPlus model to be calibrated.

    Attribute:
        name: name of the building energy model.
        idf: pointer towards IDF objects.
        output_filename: name of the output file storing the updated EnergyPlus model.
    """

    def __init__(self, idf_filename, output_filename):
        if platform.system() == 'Windows':
            IDF.setiddname(os.environ['ENERGYPLUS'] + '\\Energy+.idd')
        elif platform.system() == 'Linux':
            IDF.setiddname(os.environ['ENERGYPLUS'] + '/Energy+.idd')
        self.idf = IDF(idf_filename)
        self.output_filename = output_filename
        ProxyBuildingEnergyModel.__init__(self, os.path.splitext(os.path.basename(idf_filename))[0])

    def create_parameters(self, category):
        """
        Create parameters of a certain category.

        :param category: category of parameter.
        :return: list of parameters corresponding to the category.
        """
        parameters = []
        is_changing_window_to_wall_ratio = False
        if category == CategoryParameterBuildingEnergyModel.OCCUPANCY:
            for obj in self.idf.idfobjects[ParameterEnergyPlusModelOccupancy().get_classname()]:
                parameters.append(ParameterEnergyPlusModelOccupancy(obj.Name + ':' + ParameterEnergyPlusModelOccupancy().get_category_name(), self.idf))
        elif category == CategoryParameterBuildingEnergyModel.LIGHTING:
            for obj in self.idf.idfobjects[ParameterEnergyPlusModelLighting().get_classname()]:
                parameters.append(ParameterEnergyPlusModelLighting(obj.Name + ':' + ParameterEnergyPlusModelLighting().get_category_name(), self.idf))
        elif category == CategoryParameterBuildingEnergyModel.ELECTRIC_EQUIPMENT:
            for obj in self.idf.idfobjects[ParameterEnergyPlusModelElectricEquipment().get_classname()]:
                parameters.append(ParameterEnergyPlusModelElectricEquipment(obj.Name + ':' + ParameterEnergyPlusModelElectricEquipment().get_category_name(), self.idf))
        elif category == CategoryParameterBuildingEnergyModel.INFILTRATION:
            for obj in self.idf.idfobjects[ParameterEnergyPlusModelInfiltration().get_classname()]:
                parameters.append(ParameterEnergyPlusModelInfiltration(obj.Name + ':' + ParameterEnergyPlusModelInfiltration().get_category_name(), self.idf))
        elif category == CategoryParameterBuildingEnergyModel.WINDOW_TO_WALL_RATIO:
            p = ParameterEnergyPlusModelWindowToWallRatio(self.name + ':Window to Wall Ratio', self.idf)
            p.set_value(0.5)
            parameters.append(p)
        elif category == CategoryParameterBuildingEnergyModel.WINDOW_THERMAL_RESISTANCE:
            for obj in self.idf.idfobjects[ParameterEnergyPlusModelWindowThermalResistance().get_classname()]:
                parameters.append(ParameterEnergyPlusModelWindowThermalResistance('Imaginary Exterior Window Layer:'  + ParameterEnergyPlusModelWindowThermalResistance().get_category_name(), self.idf))
        elif category == CategoryParameterBuildingEnergyModel.WINDOW_SHGC:
            for obj in self.idf.idfobjects[ParameterEnergyPlusModelWindowSolarHeatGainCoefficient().get_classname()]:
                parameters.append(ParameterEnergyPlusModelWindowSolarHeatGainCoefficient('Imaginary Exterior Window Layer:' + ParameterEnergyPlusModelWindowSolarHeatGainCoefficient().get_category_name(), self.idf))
        elif category == CategoryParameterBuildingEnergyModel.WALL_THERMAL_RESISTANCE:
            for obj in self.idf.idfobjects[ParameterEnergyPlusModelWallThermalResistance().get_classname()]:
                parameters.append(ParameterEnergyPlusModelWallThermalResistance('Imaginary Exterior Wall Outer Layer:' + ParameterEnergyPlusModelWallThermalResistance().get_category_name(), self.idf))
        elif category == CategoryParameterBuildingEnergyModel.WALL_DENSITY:
            for obj in self.idf.idfobjects[ParameterEnergyPlusModelWallDensity().get_classname()]:
                parameters.append(ParameterEnergyPlusModelWallDensity('Imaginary Exterior Wall Outer Layer:' + ParameterEnergyPlusModelWallDensity().get_category_name(), self.idf))
        elif category == CategoryParameterBuildingEnergyModel.WALL_SPECIFIC_HEAT_CAPACITY:
            for obj in self.idf.idfobjects[ParameterEnergyPlusModelWallSpecificHeatCapacity().get_classname()]:
                parameters.append(ParameterEnergyPlusModelWallSpecificHeatCapacity('Imaginary Exterior Wall Outer Layer:' + ParameterEnergyPlusModelWallSpecificHeatCapacity().get_category_name(), self.idf))
        elif category == CategoryParameterBuildingEnergyModel.WALL_THERMAL_EMISSIVITY:
            for obj in self.idf.idfobjects[ParameterEnergyPlusModelWallThermalEmissivity().get_classname()]:
                parameters.append(ParameterEnergyPlusModelWallThermalEmissivity('Imaginary Exterior Wall Outer Layer:' + ParameterEnergyPlusModelWallThermalEmissivity().get_category_name(), self.idf))
        elif category == CategoryParameterBuildingEnergyModel.WALL_THERMAL_ABSORPTIVITY:
            for obj in self.idf.idfobjects[ParameterEnergyPlusModelWallThermalAbsorptivity().get_classname()]:
                parameters.append(ParameterEnergyPlusModelWallThermalAbsorptivity('Imaginary Exterior Wall Outer Layer:' + ParameterEnergyPlusModelWallThermalAbsorptivity().get_category_name(), self.idf))
        elif category == CategoryParameterBuildingEnergyModel.HEATING_TEMPERATURE_SETPOINT:
            for obj in self.idf.idfobjects[ParameterEnergyPlusModelHeatingTemperatureSetpoint().get_classname()]:
                parameters.append(ParameterEnergyPlusModelHeatingTemperatureSetpoint(obj.Name + ':' + ParameterEnergyPlusModelHeatingTemperatureSetpoint().get_category_name(), self.idf))
        elif category == CategoryParameterBuildingEnergyModel.COOLING_TEMPERATURE_SETPOINT:
            for obj in self.idf.idfobjects[ParameterEnergyPlusModelCoolingTemperatureSetpoint().get_classname()]:
                parameters.append(ParameterEnergyPlusModelCoolingTemperatureSetpoint(obj.Name + ':' + ParameterEnergyPlusModelCoolingTemperatureSetpoint().get_category_name(), self.idf))
        elif category == CategoryParameterBuildingEnergyModel.MECHANICAL_VENTILATION:
            for obj in self.idf.idfobjects[ParameterEnergyPlusModelMechanicalVentilation().get_classname()]:
                parameters.append(ParameterEnergyPlusModelMechanicalVentilation(obj.Zone_Name + ':' + ParameterEnergyPlusModelMechanicalVentilation().get_category_name(), self.idf))
        return parameters

    def save(self):
        """
        Save the building energy model after setting parameters.
        """
        self.idf.save(self.output_filename)

class UrbanBuildingEnergyModel():
    """
    Class representing an urban building energy model to be calibrated.

    Attributes:
        building_names: list of building names.
        bems_directory (str): directory where building energy models to be calibrated are stored.
        bem_proxies (dict): dictionary containing proxies of each building energy model to be calibrated.
    """
    __metaclass__ = ABCMeta

    def __init__(self, input_dir, output_dir = '.'):
        """
        :param building_names: list of building names.
        :param input_dir: directory in which building energy models are stored.
        :param output_dir: directory in which modified building energy models are stored.
        """
        self.bems_directory = output_dir
        self.bem_proxies = self.create_bem_proxies(input_dir, output_dir)

    def get_building_names(self):
        """
        :return: list of building names
        """
        return self.bem_proxies.keys()

    def get_parameters(self, building_name, category):
        """
        :param building_name: name of the building
        :param category: category of parameters
        :return: list of parameters of the building corresponding to the category
        """
        return self.bem_proxies[building_name].get_parameters(category)

    def set_parameters(self, building_name, param_names, values):
        """
        Set a list of
        """
        self.bem_proxies[building_name].set_parameters(param_names, values)

    @abstractmethod
    def create_bem_proxies(self, input_dir, output_dir):
        """
        Create the dictionary of proxies for each building energy model.
        :param input_dir: directory in which building energy models are stored.
        :param output_dir: directory in which modified building energy models are stored.
        """
        pass

    @abstractmethod
    def simulate(self, from_date, to_date, dt):
        """
        Simulate the urban building energy model.

        :param from_date: date from which simulations must be performed using the urban building energy model.
        :param to_date: date to which simulations must be performed using the urban building energy model.
        :param dt: time step between outputs.
        :return: outputs of simulation.
        """
        pass

class StandaloneEnergyPlusModels(UrbanBuildingEnergyModel):
    """
    Class representing an urban building energy model consisting of individual EnergyPlus models.

    Attributes:
        building_names: list of building names.
        bems_directory (str): directory where building energy models to be calibrated are stored.
        bem_proxies (dict): dictionary containing proxies of each building energy model to be calibrated.
        weather_file: file containing weather data to perform EnergyPlus simulations.
    """

    def __init__(self, input_dir, weather_file, output_dir = '.'):
        """
        :param input_dir: directory in which building energy models are stored.
        :param weather_file: file containing weather data to perform EnergyPlus simulations.
        :param output_vars: list of output variables to be used for calibration.
        :param output_dir: directory in which modified building energy models are stored.
        """
        UrbanBuildingEnergyModel.__init__(self, input_dir, output_dir)
        self.weather_file = weather_file

    def create_bem_proxies(self, input_dir, output_dir):
        """
        Create the dictionary of proxies for each building energy model.
        :param input_dir: directory in which building energy models are stored.
        :param output_dir: directory in which modified building energy models are stored.
        """
        proxies = {}
        for fn in os.listdir(input_dir):
            building_name = os.path.splitext(fn)[0]
            proxies[building_name] = ProxyEnergyPlusModel(idf_filename=input_dir + fn, output_filename=output_dir + fn)
        return proxies

    def simulate(self, from_date, to_date, dt):
        """
        Simulate the urban building energy model.

        :param from_date: date from which simulations must be performed using the urban building energy model.
        :param to_date: date to which simulations must be performed using the urban building energy model.
        :param dt: time step between outputs.
        :return: outputs of simulation.
        """
        bem_pool = EnergyPlusSimulationPool(EPWDataLoader(self.weather_file, year=from_date.year))
        bem_pool.pool = []
        for building_name, proxy in self.bem_proxies.items():
            bem_pool.pool.append(EnergyPlusModel(IDFBuildingLoader(self.bems_directory + building_name + '.idf')))
        bem_pool.output_dir = 'simulation\\'
        if platform.system() == 'Linux':
            bem_pool.output_dir = 'simulation/'
        bem_pool.run()
        output_data = {}
        for bem in bem_pool.pool:
            output_data[bem.building.name] = bem.building.get_sensible_cooling_load()[from_date:to_date].resample(dt).interpolate().values + \
                                                           bem.building.get_latent_cooling_load()[from_date:to_date].resample(dt).interpolate().values
        return output_data

class CoupledEnergyPlusModels(StandaloneEnergyPlusModels):
    """
    Class representing an urban building energy model consisting of EnergyPlus models coupled with a data driven urban canopy model.

    Attributes:
        building_names: list of building names.
        bems_directory (str): directory where building energy models to be calibrated are stored.
        bem_proxies (dict): dictionary containing proxies of each building energy model to be calibrated.
        weather_file: file containing weather data to perform EnergyPlus simulations.
        cfg_file: file containing configuration of the cosimulation engine.
        neighborhood_file: file containing information of the neighborhood to be considered for cosimulation.
        max_iter: maximum of iterations within which the coupled scheme should achieve convergence.
        ddm: type of data driven urban canopy model to be coupled with EnergyPlus models.
        training_split_ratio: ratio between the size of the training set and the total data set over the period of simulation.
        error_function: error function to determine whether the coupled scheme achieved convergence.
        n_processes: number of processes to speed up the training phase if it can be parallelized.
    """

    def __init__(self, input_dir, weather_file, cfg_file, neighborhood_file, output_dir = '.', max_iter = 100, ddm = 'dummy', training_split_ratio = 0.0, error_function = RootMeanSquareError(), n_processes = 2):
        """
        :param input_dir: directory in which building energy models are stored.
        :param weather_file: file containing weather data to perform EnergyPlus simulations.
        :param output_dir: directory in which modified building energy models are stored.
        :param cfg_file: file containing configuration of the cosimulation engine.
        :param neighborhood_file: file containing information of the neighborhood to be considered for cosimulation.
        :param max_iter: maximum of iterations within which the coupled scheme should achieve convergence.
        :param ddm: type of data driven urban canopy model to be coupled with EnergyPlus models.
        :param training_split_ratio: ratio between the size of the training set and the total data set over the period of simulation.
        :param n_processes: number of processes to speed up the training phase if it can be parallelized.
        """
        StandaloneEnergyPlusModels.__init__(self, input_dir, weather_file, output_dir)
        self.cfg_file = cfg_file
        self.neighborhood_file = neighborhood_file
        self.max_iter = max_iter
        self.ddm = ddm
        self.training_split_ratio = training_split_ratio
        self.was_trained = False
        self.error_function = error_function
        self.n_processes = n_processes

    def simulate(self, from_date, to_date, dt):
        """
        Simulate the urban building energy model.

        :param from_date: date from which simulations must be performed using the urban building energy model.
        :param to_date: date to which simulations must be performed using the urban building energy model.
        :param dt: time step between outputs.
        :return: outputs of simulation.
        """
        if not self.was_trained:
            cosim = ExclusiveCosimulationEnergyPlusDataDriven(self.cfg_file, self.neighborhood_file, self.weather_file, max_iter=self.max_iter, ddm=self.ddm, training_split_ratio=self.training_split_ratio, error_function=self.error_function, n_processes=self.n_processes)
            self.was_trained = True
        else:
            cosim = ExclusiveCosimulationEnergyPlusDataDriven(self.cfg_file, self.neighborhood_file, self.weather_file, max_iter=self.max_iter, ddm=self.ddm, error_function=self.error_function, n_processes=self.n_processes)
        cosim.cosimulate()
        output_data = {}
        for bem in cosim.bems:
            output_data[bem.building.name] = bem.building.get_sensible_cooling_load()[from_date:to_date].resample(dt).interpolate().values + \
                                             bem.building.get_latent_cooling_load()[from_date:to_date].resample(dt).interpolate().values
        return output_data


class Calibration():
    """
    Class representing an algorithm to calibrate an urban building energy model.

    Attributes:
        ubem: urban building energy model to calibrate
        metered_data: metered data used to calibrate the urban building energy model
        categories: categories of parameters that must be calibrated.
        upper_bounds: upper bounds for each category of parameters.
        lower_bounds: lower bounds for each category of parameters.
        from_date: date from which estimates and measurements must be compared.
        to_date: date to which estimates and measurements must be compared.
        dt: timestep with which estimates and measurements must be compared.
        error_function: method to calculate the discrepancy between measurements and estimates.
        must_be_trained: True if the UBEM needs some prior training before calibration.
    """
    __metaclass__ = ABCMeta

    def __init__(self, ubem, metered_data, categories, upper_bounds, lower_bounds, from_date, to_date, dt, error_function = RootMeanSquareError(), must_be_trained=False):
        """
        :param ubem: urban building energy model to calibrate
        :param metered_data: metered data used to calibrate the urban building energy model
        :param categories: categories of parameters that must be calibrated.
        :param upper_bounds: upper bounds for each category of parameters.
        :param lower_bounds: lower bounds for each category of parameters.
        :param from_date: date from which estimates and measurements must be compared.
        :param to_date: date to which estimates and measurements must be compared.
        :param dt: timestep with which estimates and measurements must be compared.
        :param error_function: method to calculate the discrepancy between measurements and estimates.
        :param must_be_trained: True if the UBEM needs some prior training before calibration.
        """
        self.ubem = ubem
        self.metered_data = metered_data
        self.categories = categories
        self.upper_bounds = upper_bounds
        self.lower_bounds = lower_bounds
        self.from_date = from_date
        self.to_date = to_date
        self.dt = dt
        self.error_function = error_function
        self.must_be_trained = must_be_trained

    def calibrate(self):
        if self.must_be_trained:
            for building_name in self.ubem.get_building_names():
                all_parameters = []
                mean_values = np.array([])
                for n, category in enumerate(self.categories):
                    params = self.ubem.get_parameters(building_name, category)
                    for p in params:
                        all_parameters.append(p.name)
                    mean_values = np.concatenate((mean_values, 0.5 * (self.upper_bounds[n] + self.lower_bounds[n]) * np.ones(len(params))))
                self.ubem.set_parameters(building_name, all_parameters, mean_values)
            self.ubem.simulate(self.from_date, self.to_date, self.dt)
        calibrated_params = self.get_calibrated_parameters()
        for building_name, proxy in self.ubem.bem_proxies.items():
            proxy.output_filename = "calibration\\" + building_name + '.idf'
            if platform.system() == 'Linux':
                proxy.output_dir = 'calibration/' + building_name + '.idf'
            proxy.set_parameters(calibrated_params[building_name]['names'], calibrated_params[building_name]['values'])

    @abstractmethod
    def get_calibrated_parameters(self):
        """
        :return (dict): calibrated parameters for each building of the urban building energy model.
        """
        pass

def model(output_samples, input_names, lower_bounds, upper_bounds, surrogate_model):
    priors = []
    for n, input_name in enumerate(input_names):
        priors.append(
            pyro.sample(input_name, dist.Uniform(torch.tensor(lower_bounds[n]), torch.tensor(upper_bounds[n]))))
    input_tensor = torch.tensor([priors]).detach().numpy()
    priors_array = tf.convert_to_tensor(input_tensor, dtype=tf.float64)
    expected_output = surrogate_model.predict(priors_array)
    pyro.sample("discrepancy", dist.Normal(expected_output[0, 0], 0.1), obs=output_samples)

class BayesianCalibration(Calibration):
    """
    Class representing the bayesian framework for calibration of an urban building energy model.

    Attributes:
        ubem: urban building energy model to calibrate
        metered_data: metered data used to calibrate the urban building energy model
        categories: categories of parameters that must be calibrated.
        upper_bounds: upper bounds for each category of parameters.
        lower_bounds: lower bounds for each category of parameters.
        from_date: date from which estimates and measurements must be compared.
        to_date: date to which estimates and measurements must be compared.
        dt: timestep with which estimates and measurements must be compared.
        error_function: method to calculate the discrepancy between measurements and estimates.
        must_be_trained: True if the UBEM needs some prior training before calibration.
        parameters_selector: method used to select parameters.
        num_training_samples: number of samples to train/test a surrogate model of buildings.
        surrogate_model_loader: method to load surrogate models of building energy models.
        num_warmup_steps: number of warmup steps before the MCMC sampling.
        num_chains: number of chains to run in parallel during the MCMC sampling.
    """

    def __init__(self, ubem, metered_data, categories, upper_bounds, lower_bounds, from_date, to_date, dt, parameters_selector,
                 num_training_samples, surrogate_model_loader, num_posterior_distribution_samples, error_function = RootMeanSquareError(),
                 must_be_trained=False, num_warmup_steps = 10, num_chains = 2):
        """
        :param ubem: urban building energy model to calibrate
        :param metered_data: metered data used to calibrate the urban building energy model
        :param categories: categories of parameters that must be calibrated.
        :param upper_bounds: upper bounds for each category of parameters.
        :param lower_bounds: lower bounds for each category of parameters.
        :param from_date: date from which estimates and measurements must be compared.
        :param to_date: date to which estimates and measurements must be compared.
        :param dt: timestep with which estimates and measurements must be compared.
        :param must_be_trained: True if the UBEM needs some prior training before calibration.
        :param parameters_selector: method used to select the most sensitive parameters of each building in an urban building energy model.
        :param num_training_samples: number of samples to train/test a surrogate model of buildings.
        :param surrogate_model_loader: method to load surrogate models of building energy models.
        :param num_posterior_distribution_samples: number of samples to evaluate the posterior distribution of each parameter.
        :param num_warmup_steps: number of warmup steps before the MCMC sampling.
        :param num_chains: number of chains to run in parallel during the MCMC sampling.
        """
        Calibration.__init__(self, ubem, metered_data, categories, upper_bounds, lower_bounds, from_date, to_date, dt, error_function, must_be_trained)
        self.parameters_selector = parameters_selector
        self.parameters_selector.ubem = ubem
        self.parameters_selector.metered_data = metered_data
        self.parameters_selector.categories = categories
        self.parameters_selector.upper_bounds = upper_bounds
        self.parameters_selector.lower_bounds = lower_bounds
        self.parameters_selector.from_date = from_date
        self.parameters_selector.to_date = to_date
        self.parameters_selector.dt = dt
        self.parameters_selector.error_function = error_function
        self.num_training_samples = num_training_samples
        self.surrogate_model_loader = surrogate_model_loader
        self.num_posterior_distribution_samples = num_posterior_distribution_samples
        self.num_warmup_steps = num_warmup_steps
        self.num_chains = num_chains


    def get_calibrated_parameters(self):
        """
        :return: calibrated parameters for each building of the urban building energy model.
        """
        if platform.system() == 'Windows':
            SAMPLES_DIR = 'calibration\\samples\\'
            POSTERIOR_DISTRIBUTIONS_DIR = 'calibration\\distributions\\'
            os.makedirs('calibration\\', exist_ok=True)
            os.makedirs(SAMPLES_DIR, exist_ok=True)
            os.makedirs('calibration\\sensitivity\\', exist_ok=True)
            os.makedirs('calibration\\surrogates\\', exist_ok=True)
            os.makedirs(POSTERIOR_DISTRIBUTIONS_DIR, exist_ok=True)
        elif platform.system() == 'Linux':
            SAMPLES_DIR = 'calibration/samples/'
            POSTERIOR_DISTRIBUTIONS_DIR = 'calibration/distributions/'
            os.makedirs('calibration/', exist_ok=True)
            os.makedirs(SAMPLES_DIR, exist_ok=True)
            os.makedirs('calibration/sensitivity/', exist_ok=True)
            os.makedirs('calibration/surrogates/', exist_ok=True)
            os.makedirs(POSTERIOR_DISTRIBUTIONS_DIR, exist_ok=True)
        selected_parameters = self.parameters_selector.select_parameters()
        calibrated_parameters = {}
        for building_name in self.ubem.get_building_names():
            calibrated_parameters[building_name] = {}
            training_samples = pd.read_csv(SAMPLES_DIR + building_name + '.csv').sample(n=self.num_training_samples)
            self.surrogate_model_loader.building_name = building_name
            self.surrogate_model_loader.inputs = training_samples[selected_parameters[building_name]['names']].values
            self.surrogate_model_loader.outputs = training_samples[self.error_function.get_name()].values
            surrogate_model = self.surrogate_model_loader.load()
            input_names = selected_parameters[building_name]['names']
            lower_bounds = selected_parameters[building_name]['lower_bounds']
            upper_bounds = selected_parameters[building_name]['upper_bounds']
            input_samples = np.random.uniform(low=lower_bounds, high=upper_bounds, size=(self.num_posterior_distribution_samples, len(input_names)))
            output_samples = surrogate_model.predict(input_samples)
            nuts_kernel = NUTS(model, adapt_step_size=True)
            mcmc = MCMC(nuts_kernel, num_samples=self.num_posterior_distribution_samples, warmup_steps=self.num_warmup_steps, num_chains=self.num_chains)
            mcmc.run(torch.tensor(output_samples), input_names, lower_bounds, upper_bounds, surrogate_model)
            posterior_samples = mcmc.get_samples()
            with open(POSTERIOR_DISTRIBUTIONS_DIR + building_name + '.pkl', 'wb') as f:
                pickle.dump(posterior_samples, f)
            calibrated_parameters[building_name] = {}
            calibrated_parameters[building_name]['names'] = []
            calibrated_parameters[building_name]['values'] = []
            for pname in selected_parameters[building_name]['names']:
                calibrated_parameters[building_name]['names'].append(pname)
                calibrated_parameters[building_name]['values'].append(posterior_samples[pname].mean().item())
        return calibrated_parameters


class ParametersSelector():
    """
    Class used to select parameters of an urban building energy model to be calibrated.

    Attributes:
        ubem: urban building energy model to be calibrated.
        metered_data: metered data used to calibrate the urban building energy model.
        categories: list of parameter categories to be calibrated.
        upper_bounds: list containing upper bounds for each parameter.
        lower_bounds: list containing lower bounds for each parameter.
        from_date: date from which estimates provided by the UBEM and measurements must be compared.
        to_date: date to which estimates provided by the UBEM and measurements must be compared.
        dt: timestep with which estimates provided by the UBEM and measurements must be compared.
        iter_saved: number of iterations to save samples for parameter selections.
    """
    __metaclass__ = ABCMeta

    def __init__(self, ubem = None, metered_data = None, categories = None, upper_bounds = None, lower_bounds = None,
                 from_date = None, to_date = None, dt = None, error_function = RootMeanSquareError(), iter_saved = 5):
        """
        :param ubem: urban building energy model to be calibrated.
        :param metered_data: metered data used to calibrate the urban building energy model.
        :param categories: list of parameter categories to be calibrated.
        :param upper_bounds: list containing upper bounds for each parameter.
        :param lower_bounds: list containing lower bounds for each parameter.
        :param from_date: date from which estimates provided by the UBEM and measurements must be compared.
        :param to_date: date to which estimates provided by the UBEM and measurements must be compared.
        :param dt: timestep with which estimates provided by the UBEM and measurements must be compared.
        :param error_function: method used to evaluate the discrepancy between measurements and estimates.
        :param iter_saved: number of iterations to save samples for parameter selections.
        """
        self.ubem = ubem
        self.metered_data = metered_data
        self.categories = categories
        self.upper_bounds = upper_bounds
        self.lower_bounds = lower_bounds
        self.from_date = from_date
        self.to_date = to_date
        self.dt = dt
        self.error_function = error_function
        self.iter_saved = iter_saved

    def select_parameters(self):
        """
        :return: selected parameters for each building of the urban building energy model.
        """
        calibration_data = {}
        for building_name in self.ubem.get_building_names():
            calibration_data[building_name] = {}
            all_parameters = []
            parameters_upper_bounds = np.array([])
            parameters_lower_bounds = np.array([])
            for n, category in enumerate(self.categories):
                params = self.ubem.get_parameters(building_name, category)
                for p in params:
                    all_parameters.append(p.name)
                parameters_upper_bounds = np.concatenate((parameters_upper_bounds, self.upper_bounds[n] * np.ones(len(params))))
                parameters_lower_bounds = np.concatenate((parameters_lower_bounds, self.lower_bounds[n] * np.ones(len(params))))
            calibration_data[building_name]['parameters'] = all_parameters
            calibration_data[building_name]['lower_bounds'] = parameters_lower_bounds
            calibration_data[building_name]['upper_bounds'] = parameters_upper_bounds
            calibration_data[building_name]['input_samples'] = self.generate_input_samples(building_name, all_parameters, parameters_upper_bounds, parameters_lower_bounds)
            number_samples = calibration_data[building_name]['input_samples'].shape[0]
            calibration_data[building_name]['output_samples'] = np.zeros(number_samples)
        path_to_save = 'calibration\\samples\\'
        if platform.system() == 'Linux':
            path_to_save = path_to_save.replace('\\', '/')
        n_start = 0
        if not (len(os.listdir(path_to_save)) == 0):
            for building_name in self.ubem.get_building_names():
                df = pd.read_csv(path_to_save + building_name + '.csv')
                for n in range(len(df)):
                    calibration_data[building_name]['output_samples'][n] = df[self.error_function.get_name()][n]
                    for m, pname in enumerate(calibration_data[building_name]['parameters']):
                        calibration_data[building_name]['input_samples'][n][m] = df[pname][n]
            n_start = len(df)
        print('Number samples to be generated: ' + str(number_samples - n_start))
        for n in range(n_start, number_samples):
            for building_name in self.ubem.get_building_names():
                self.ubem.set_parameters(building_name, calibration_data[building_name]['parameters'], calibration_data[building_name]['input_samples'][n])
            outputs = self.ubem.simulate(self.from_date, self.to_date, self.dt)
            for building_name in self.ubem.get_building_names():
                measurements = self.metered_data[building_name][self.from_date:self.to_date].resample(self.dt).interpolate().values
                estimates = outputs[building_name]
                calibration_data[building_name]['output_samples'][n] = self.error_function.err(estimates, measurements)
                if (n == number_samples - 1) or ((n % self.iter_saved) == 0):
                    print('Samples being saved ... (Remaining: ' + str(number_samples - n) + ')')
                    column_names = calibration_data[building_name]['parameters'] + [self.error_function.get_name()]
                    data = np.concatenate((calibration_data[building_name]['input_samples'][0:n+1], calibration_data[building_name]['output_samples'][0:n+1].reshape(-1, 1)), axis=1)
                    df = pd.DataFrame(data, columns=column_names)
                    df.to_csv(path_to_save + building_name + '.csv', index=False)
        selected_parameters = {}
        for building_name in self.ubem.get_building_names():
            sensitivity_data = self.perform_sensitivity_analysis(building_name, calibration_data[building_name]['input_samples'], calibration_data[building_name]['output_samples'])
            selected_parameters[building_name] = self.make_parameters_selection(sensitivity_data, calibration_data[building_name]['lower_bounds'], calibration_data[building_name]['upper_bounds'])
        return selected_parameters


    @abstractmethod
    def generate_input_samples(self, building_name, parameters, upper_bounds, lower_bounds):
        """
        Generate input samples for the sensitivity analysis.
        :param building_name: name of the building for which the sensitivity analysis must be performed.
        :param parameters: list of parameters for the sensitivity analysis.
        :param upper_bounds: upper bounds for each parameter.
        :param lower_bounds: lower bounds for each parameter.
        :return: input samples for the sensitivity analysis.
        """
        pass

    @abstractmethod
    def perform_sensitivity_analysis(self, building_name, inputs, outputs):
        """
        Perform sensitivity analysis for selection of parameters
        :param building_name: name of the building for which the sensitivity analysis must be performed.
        :param inputs: input samples for the sensitivity analysis.
        :param outputs: output samples for the sensitivity analysis.
        :return: results of sensitivity analysis.
        """
        pass

    @abstractmethod
    def make_parameters_selection(self, results, lower_bounds, upper_bounds):
        """
        Make the selection of parameters.
        :param results: results of the sensitivity analysis.
        :param lower_bounds: lower bounds of all parameters.
        :param upper_bounds: upper bounds of all parameters.
        :return: list of selected parameters.
        """
        pass


class ParametersSelectorMorris(ParametersSelector):
    """
    Class used to select parameters of an urban building energy model to be calibrated using the Morris method.

    Attributes:
        ubem: urban building energy model to be calibrated.
        metered_data: metered data used to calibrate the urban building energy model.
        categories: list of parameter categories to be calibrated.
        upper_bounds: list containing upper bounds for each parameter.
        lower_bounds: list containing lower bounds for each parameter.
        from_date: date from which estimates provided by the UBEM and measurements must be compared.
        to_date: date to which estimates provided by the UBEM and measurements must be compared.
        dt: timestep with which estimates provided by the UBEM and measurements must be compared.
        error_function: method used to evaluate the discrepancy between measurements and estimates.
        iter_saved: number of iterations to save samples for parameter selections.
        num_trajectories: number of trajectories to generate with the Morris method.
        num_levels: number of grid levels to consider with the Morris method.
        optimal_trajectories: number of optimal trajectories to samples using the Morris method.
        num_best_parameters: number of best parameters to select from the Morris method.
        problem: specification of the problem to be studied using the Morris method.
    """

    def __init__(self, ubem = None, metered_data = None, categories = None, upper_bounds = None, lower_bounds = None,
                 from_date = None, to_date = None, dt = None, error_function = RootMeanSquareError(), iter_saved = 5, num_trajectories=10,
                 num_levels=4, optimal_trajectories=2, num_best_parameters=1):
        """
        :param ubem: urban building energy model to be calibrated.
        :param metered_data: metered data used to calibrate the urban building energy model.
        :param categories: list of parameter categories to be calibrated.
        :param upper_bounds: list containing upper bounds for each parameter.
        :param lower_bounds: list containing lower bounds for each parameter.
        :param from_date: date from which estimates provided by the UBEM and measurements must be compared.
        :param to_date: date to which estimates provided by the UBEM and measurements must be compared.
        :param dt: timestep with which estimates provided by the UBEM and measurements must be compared.
        :param error_function: method used to evaluate the discrepancy between measurements and estimates.
        :param number_samples: number of samples to use for performing the parameter selection (i.e. sensitivity analysis).
        :param iter_saved: number of iterations to save samples for parameter selections.
        :param num_trajectories: number of trajectories to generate with the Morris method.
        :param num_levels: number of grid levels to consider with the Morris method.
        :param optimal_trajectories: number of optimal trajectories to samples using the Morris method.
        """
        ParametersSelector.__init__(self, ubem, metered_data, categories, upper_bounds, lower_bounds, from_date, to_date, dt, error_function, iter_saved)
        self.num_trajectories = num_trajectories
        self.num_levels = num_levels
        self.optimal_trajectories = optimal_trajectories
        self.num_best_parameters = num_best_parameters
        self.problems = {}

    def generate_input_samples(self, building_name, parameters, upper_bounds, lower_bounds):
        """
        Generate input samples for the sensitivity analysis.
        :param building_name: name of the building for which the sensitivity analysis must be performed.
        :param parameters: list of parameters for the sensitivity analysis.
        :param upper_bounds: upper bounds for each parameter.
        :param lower_bounds: lower bounds for each parameter.
        :return: input samples for the sensitivity analysis.
        """
        self.problems[building_name] = {
            'num_vars': len(parameters),
            'names': parameters,
            'groups': None,
            'bounds': np.concatenate((lower_bounds.reshape(-1, 1), upper_bounds.reshape(-1, 1)), axis=1)
        }
        return morris_sampler.sample(self.problems[building_name], N=self.num_trajectories, num_levels=self.num_levels, optimal_trajectories=self.optimal_trajectories)

    def perform_sensitivity_analysis(self, building_name, inputs, outputs):
        """
        Perform sensitivity analysis for selection of parameters.
        :param building_name: name of the building for which the sensitivity analysis must be performed.
        :param inputs: input samples for the sensitivity analysis.
        :param outputs: output samples for the sensitivity analysis.
        :return: results of sensitivity analysis.
        """
        sensitivity_analysis_data = {}
        results = morris.analyze(self.problems[building_name], inputs, outputs, conf_level=0.95, num_levels=4)
        sensitivity_analysis_data = {}
        sensitivity_analysis_data['parameters'] = results['names']
        sensitivity_analysis_data['mu_star'] = results['mu_star'].filled(fill_value=np.nan).tolist()
        sensitivity_analysis_data['sigma'] = results['sigma'].tolist()
        SENSITIVITY_DIR = 'calibration\\sensitivity\\'
        if platform.system() == 'Linux':
            SENSITIVITY_DIR = SENSITIVITY_DIR.replace('\\', '/')
        with open(SENSITIVITY_DIR + building_name + '.json', 'w') as file:
            json.dump(sensitivity_analysis_data, file)
        return sensitivity_analysis_data

    def make_parameters_selection(self, results, lower_bounds, upper_bounds):
        """
        Make the selection of parameters.
        :param results: results of the sensitivity analysis.
        :param lower_bounds: lower bounds of all parameters.
        :param upper_bounds: upper bounds of all parameters.
        :return: list of selected parameters.
        """
        sorted_indexes = [i for i, _ in sorted(enumerate(results['mu_star']), key=lambda x: x[1], reverse=True)]
        selected_parameters = {}
        selected_parameters['names'] = []
        selected_parameters['lower_bounds'] = []
        selected_parameters['upper_bounds'] = []
        for i in sorted_indexes[0:self.num_best_parameters]:
            selected_parameters['names'].append(results['parameters'][i])
            selected_parameters['lower_bounds'].append(lower_bounds[i])
            selected_parameters['upper_bounds'].append(upper_bounds[i])
        return selected_parameters


class SurrogateBuildingEnergyModel():
    """
    Class used to emulate the behaviour of a building energy model during the calibration of an urban building energy model.

    Attributes:
        building_name: name of the building the surrogate model is supposed to emulate.
    """
    __metaclass__ = ABCMeta

    def __init__(self, building_name):
        """
        :param building_name: building_name: name of the building the surrogate model is supposed to emulate.
        """
        self.building_name = building_name


    @abstractmethod
    def train(self, inputs, outputs):
        """
        Train a surrogate model.
        :param inputs: inputs used to train the surrogate model.
        :param outputs: outputs used to train the surrogate model.
        """
        pass

    @abstractmethod
    def save(self, folder):
        """
        Save the surrogate model.
        :param folder: folder in which to save the surrogate model.
        """
        pass

    @abstractmethod
    def predict(self, inputs):
        """
        Make predictions using the surrogate model.
        :param inputs: inputs used to make predictions.
        :return: predictions
        """
        pass

class GaussianProcessModel(SurrogateBuildingEnergyModel):
    """
    Class used to emulate the behaviour of a building energy model as a gaussian process.

    Attribute:
        building_name: name of the building the surrogate model is supposed to emulate.
        gaussian_process_model: internal state of the gaussian process model used to emulate a building energy model.
    """

    def __init__(self, building_name):
        SurrogateBuildingEnergyModel.__init__(self, building_name)
        tf.Module.__init__(self)
        self.gaussian_process_model = None

    @tf.function
    def __call__(self, inputs):
        return self.gaussian_process_model.predict_f(inputs)


    def train(self, inputs, outputs):
        """
        Train a surrogate model.
        :param inputs: inputs used to train the surrogate model.
        :param outputs: outputs used to train the surrogate model.
        """
        self.gaussian_process_model = gpflow.models.GPR(data=(inputs, outputs.reshape(-1, 1)), kernel=gpflow.kernels.SquaredExponential())
        optimizer = gpflow.optimizers.Scipy()
        optimizer.minimize(self.gaussian_process_model.training_loss, self.gaussian_process_model.trainable_variables)

    def save(self, folder):
        """
        Save the surrogate model.
        :param folder: folder in which to save the surrogate model.
        """
        with open(folder + self.building_name + '.pkl', 'wb') as file:
            pickle.dump(self.gaussian_process_model, file)


    def predict(self, inputs):
        """
        Make predictions using the surrogate model.
        :param inputs: inputs used to make predictions.
        :return: predictions
        """
        m, v = self.gaussian_process_model.predict_f(inputs)
        return m.numpy()


class SurrogateBuildingEnergyModelLoader():
    """
    Class used to load the surrogate of a building energy model.

    Attributes:
        building_name: name of the building the surrogate is supposed to emulate.
        inputs: inputs used to train the surrogate model in case it has not been previously saved.
        outputs: outputs used to train the surrogate model in case it has not been previously saved.
    """
    __metaclass__ = ABCMeta

    def __init__(self, building_name = None,  inputs = None, outputs = None):
        """
        :param building_name: name of the building the surrogate is supposed to emulate.
        :param inputs: inputs used to train the surrogate model in case it has not been previously saved.
        :param outputs: outputs used to train the surrogate model in case it has not been previously saved.
        """
        self.building_name = building_name
        self.inputs = inputs
        self.outputs = outputs

    def load(self):
        """
        Load the surrogate of a building energy model.
        :return: the surrogate model.
        """
        SURROGATE_MODELS_DIR = 'calibration\\surrogates\\'
        if platform.system() == 'Linux':
            SURROGATE_MODELS_DIR = SURROGATE_MODELS_DIR.replace('\\', '/')
        surrogate_model = None
        if self.has_not_been_saved(SURROGATE_MODELS_DIR):
            surrogate_model = self.get_instance()
            surrogate_model.train(self.inputs, self.outputs)
            surrogate_model.save(SURROGATE_MODELS_DIR)
        else:
            surrogate_model = self.read(SURROGATE_MODELS_DIR)
        return surrogate_model

    @abstractmethod
    def has_not_been_saved(self, folder):
        """
        Check if the surrogate model has been previously saved.
        :param folder: folder in which surrogate model were saved.
        :return: True if the surrogate model has not been saved.
        """
        pass

    @abstractmethod
    def get_instance(self):
        """
        Get instance of the surrogate model.
        """
        pass

    @abstractmethod
    def read(self, folder):
        """
        Read the recorded surrogate model.
        :param folder: folder where the surrogate model was saved.
        :return: the surrogate model.
        """
        pass

class GaussianProcessModelLoader(SurrogateBuildingEnergyModelLoader):
    """
    Class used to load the gaussian process model of a building.

    Attributes:
        building_name: name of the building the surrogate is supposed to emulate.
        training_samples: samples used to train the surrogate model if needed.
    """

    def __init__(self, building_name = None, inputs = None, outputs = None):
        """
        :param building_name: name of the building the surrogate is supposed to emulate.
        :param training_samples: samples used to train the surrogate model if needed.
        """
        SurrogateBuildingEnergyModelLoader.__init__(self, building_name, inputs, outputs)

    def has_not_been_saved(self, folder):
        """
        Check if the surrogate model has been previously saved.
        :param folder: folder in which surrogate model were saved.
        :return: True if the surrogate model has not been saved.
        """
        return not os.path.exists(folder + self.building_name + '.pkl')

    def get_instance(self):
        """
        Get instance of the surrogate model.
        """
        return GaussianProcessModel(self.building_name)

    def read(self, folder):
        """
        Read the recorded surrogate model.
        :param folder: folder where the surrogate model was saved.
        :return: the surrogate model.
        """
        surrogate_model = self.get_instance()
        surrogate_model.gaussian_process_model = pickle.load(open(folder + self.building_name + '.pkl', 'rb'))
        return surrogate_model












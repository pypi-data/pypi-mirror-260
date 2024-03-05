"""
Module to create and update building energy models, and perform building energy simulation in sequence or parallel.

Delft University of Technology
Dr. Miguel Martin
"""
import multiprocessing
from abc import ABCMeta, abstractmethod
import os
import shutil
from subprocess import Popen
import glob
import platform
import traceback

import numpy as np
import opyplus as op
import shutil
import subprocess
from datetime import datetime, date, timedelta
import string
import pandas as pd
from metpy.units import units

from sciencespy.dom import *

class WeatherData():
    """
    Class containing weather data.

    Attributes:
        year: year during which weather data were collected

    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self.year = date.today().year
        self.latitude = 0.0
        self.longitude = 0.0
        self.timestamps = None
        self.outdoor_air_temperature = None
        self.outdoor_air_relative_humidity = None
        self.outdoor_air_pressure = None

    @abstractmethod
    def set_year(self, new_year):
        """
        :param new_year: year weather data were collected
        """
        pass
    @abstractmethod
    def set_latitude(self, new_latitude):
        """
        :param new_latitude: latitude weather data were collected
        """
        pass
    @abstractmethod
    def set_longitude(self, new_longitude):
        """
        :param new_longitude: longitude weather data were collected
        """
        pass
    @abstractmethod
    def set_outdoor_air_temperature(self, new_outdoor_air_temperature):
        """
        :param new_outdoor_air_temperature: new values for the outdoor air temperature (in ^oC)
        """
        pass

    @abstractmethod
    def set_outdoor_air_relative_humidity(self, new_outdoor_air_relative_humidity):
        """
        :param new_outdoor_air_relative_humidity: new values for the outdoor air relative humidity (in %)
        """
        pass
    @abstractmethod
    def save(self, file_name, out_dir='.'):
        """
        Save weather data.
        :param file_name: file name where weather data must be saved
        :param out_dir: output directory where weather data must be saved
        """
        pass

class WeatherDataLoader():
    """
    Class to load weather data.

    Attributes:
        weather_file: file containing weather data.
    """
    __metaclass__ = ABCMeta

    def __init__(self, weather_file):
        """
        :param weather_file: file containg weather data.
        """
        self.weather_file = weather_file

    def load(self):
        weather_data = self.get_instance()
        weather_data.year = self.get_year()
        weather_data.latitude = self.get_latitude()
        weather_data.longitude = self.get_longitude()
        weather_data.timestamps = self.get_timestamps()
        weather_data.outdoor_air_temperature = self.get_outdoor_air_temperature()
        weather_data.outdoor_air_relative_humidity = self.get_outdoor_air_relative_humidity()
        weather_data.outdoor_air_pressure = self.get_outdoor_air_pressure()
        return weather_data

    @abstractmethod
    def get_instance(self):
        """
        :return: instance of weather data
        """
        pass


    @abstractmethod
    def get_year(self):
        """
        :return: year weather data were collected
        """
        pass

    @abstractmethod
    def get_latitude(self):
        """
        :return: latitude weather data were collected
        """
        pass

    @abstractmethod
    def get_longitude(self):
        """
        :return: longitude weather data were collected
        """
        pass

    @abstractmethod
    def get_timestamps(self):
        """
        :return: timestamps at which weather data were collected
        """
        pass

    @abstractmethod
    def get_outdoor_air_temperature(self):
        """
        :return: the outdoor air temperature (in ^oC)
        """
        pass

    @abstractmethod
    def get_outdoor_air_relative_humidity(self):
        """
        :return: the outdoor air relative humidity (in %)
        """
        pass

    @abstractmethod
    def get_outdoor_air_pressure(self):
        """
        :return: the outdoor air temperature (in Pa)
        """
        pass

class EPWDataLoader(WeatherDataLoader):
    """
    Class to load EPW data.

    Attributes:
        weather_file: file containing EPW data.
    """
    __metaclass__ = ABCMeta

    def __init__(self, weather_file, year=datetime.today().year):
        """
        :param weather_file: file containg EPW data.
        """
        self.weather_file = weather_file
        self.epw_data = op.WeatherData.load(weather_file, create_datetime_instants=True, start_year=year)
    def get_instance(self):
        """
        :return: instance of weather data
        """
        weather_data = EnergyPlusWeatherData()
        weather_data.raw_epw_data = self.epw_data
        return weather_data

    def get_year(self):
        """
        :return: year weather data were collected
        """
        bounds = self.epw_data.get_bounds()
        return bounds[0].year

    def get_latitude(self):
        """
        :return: latitude weather data were collected
        """
        return float(self.epw_data._headers['latitude'])

    def get_longitude(self):
        """
        :return: longitude weather data were collected
        """
        return float(self.epw_data._headers['longitude'])

    def get_timestamps(self):
        """
        :return: timestamps at which weather data were collected
        """
        weather_dataframe = self.epw_data.get_weather_series()
        return weather_dataframe.axes[0]

    def get_outdoor_air_temperature(self):
        """
        :return: the outdoor air temperature (in ^oC)
        """
        return np.asarray(self.epw_data.get_weather_series()['drybulb']) * units.degC

    def get_outdoor_air_relative_humidity(self):
        """
        :return: the outdoor air relative humidity (in %)
        """
        return np.asarray(self.epw_data.get_weather_series()['relhum']) * units.percent

    def get_outdoor_air_pressure(self):
        """
        :return: the outdoor air temperature (in Pa)
        """
        return np.asarray(self.epw_data.get_weather_series()['atmos_pressure']) * units.Pa

class EnergyPlusWeatherData(WeatherData):
    """
    Class representing EnergyPlus weather data.

    Attributes:
        raw_epw_data: raw epw data.
    """

    def __init__(self):
        self.raw_epw_data = None

    def set_year(self, new_year):
        """
        :param new_year: year weather data were collected
        """
        self.year = new_year
        weather_series = self.raw_epw_data.get_weather_series()
        vy = new_year * np.ones(len(weather_series))
        weather_series.year = weather_series.year.replace(to_replace = weather_series.axes[0], value = vy)
        self.raw_epw_data.set_weather_series(weather_series)

    def set_latitude(self, new_latitude):
        """
        :param new_latitude: latitude weather data were collected
        """
        self.latitude = new_latitude
        self.raw_epw_data._headers['latitude'] = str(new_latitude)

    def set_longitude(self, new_longitude):
        """
        :param new_longitude: longitude weather data were collected
        """
        self.longitude = new_longitude
        self.raw_epw_data._headers['longitude'] = str(new_longitude)

    def set_outdoor_air_temperature(self, new_outdoor_air_temperature):
        """
        :param new_outdoor_air_temperature: new values for the outdoor air temperature (in ^oC)
        """
        self.outdoor_air_temperature = new_outdoor_air_temperature
        cdf = self.raw_epw_data.get_weather_series()
        cdf['drybulb'] = new_outdoor_air_temperature
        self.raw_epw_data.set_weather_series(cdf)

    def set_outdoor_air_relative_humidity(self, new_outdoor_air_relative_humidity):
        """
        :param new_outdoor_air_relative_humidity: new values for the outdoor air relative humidity (in %)
        """
        self.outdoor_air_relative_humidity = new_outdoor_air_relative_humidity
        cdf = self.raw_epw_data.get_weather_series()
        cdf['relhum'] = new_outdoor_air_relative_humidity
        self.raw_epw_data.set_weather_series(cdf)
    def save(self, file_name, out_dir='.'):
        """
        Save weather data.
        :param file_name: file name where weather data must be saved
        :param out_dir: output directory where weather data must be saved
        """
        self.raw_epw_data.save(os.path.join(out_dir, file_name), use_datetimes=False)

class BuildingLoader():
    """
    Class to load a building.

    Attributes:
        building_file: file in which details of the building are stored.
        x: position of the building on the x-axis
        y: position of the building on the y-axis
    """
    __metaclass__ = ABCMeta

    def __init__(self, building_file, x = 0.0, y = 0.0):
        """
        :param building_file: file in which details of the building are stored.
        :paran x: position of the building on the x-axis
        :paran y: position of the building on the y-axis
        """
        self.building_file = building_file
        self.x = x
        self.y = y

    def load(self):
        """
        Load the building
        :return: loaded building
        """
        building = Building(self.get_building_name())
        building.zones = self.get_building_zones()
        (x_center, y_center, z_center) = building.get_footprint().get_centroid()
        building.move(self.x - x_center, self.y - y_center)
        return building

    @abstractmethod
    def get_building_name(self):
        """
        :return: name of the building
        """
        pass

    @abstractmethod
    def get_building_zones(self):
        """
        :return: name of the building
        """
        pass

class BuildingEnergyModel():
    """
    Class representing a building energy model.

    Attributes:
        building: building being modelled
        building_loader: loader of building
        outputs: outputs resulting from simulations using the building energy model
    """
    __metaclass__ = ABCMeta

    def __init__(self, building_loader):
        """
        :param building_loader: loader of building
        """
        self.building_loader = building_loader
        self.building = None
        self.outputs = None

    @abstractmethod
    def update(self):
        """
        Update the modelled building with respect to outputs of simulations.
        """
        pass

class BuildingEnergySimulationPool():
    """
    Pool to perform simulations of a sequence of building energy models in parallel.

    Attributes:
        weather_data: weather data to perform simulations of building energy models.
        weather_data_loader: loader of weather data.
        nproc: number of processors to run in parallel.
        pool: list of building energy models used for parallel simulations.
    """
    __metaclass__ = ABCMeta

    def __init__(self, weather_data_loader, nproc = 2):
        """
        :param weather_data_loader: loader of weather data.
        :param nproc: number of processors to run in parallel.
        """
        self.weather_data = None
        self.weather_data_loader = weather_data_loader
        self.nproc = nproc
        self.pool = []

    def run(self):
        """
        Perform building energy simulations in parallel.
        :return: list of buildings resulting from simulation
        """
        self.create_simulation_environment()
        for bem in self.pool:
            if bem.building is None:
                bem.building = bem.building_loader.load()
        if self.weather_data is None:
            self.weather_data = self.weather_data_loader.load()
        self.weather_data.save(self.get_weather_data_filename(), self.get_weather_data_directory())
        self.run_parallel_simulation()
        for bem in self.pool:
            while True:
                try:
                    bem.outputs = self.get_building_outputs(bem.building.name)
                    bem.update()
                    break
                except FileNotFoundError:
                    pass
                except PermissionError:
                    pass
        self.cleanup()

    @abstractmethod
    def create_simulation_environment(self):
        """
        Create simulation environment to perform simulations using the pool of building energy models
        """
        pass

    @abstractmethod
    def get_weather_data_filename(self):
        """
        :return: filename under which weather data must be saved.
        """
        pass

    @abstractmethod
    def get_weather_data_directory(self):
        """
        :return: directory under which weather data must be saved.
        """
        pass

    @abstractmethod
    def run_parallel_simulation(self):
        """
        Run parallel building energy simulations.
        """
        pass
    @abstractmethod
    def get_building_outputs(self, building_name):
        """
        :param building_name: name of the building
        :return: outputs of the simulation for the building
        """
        pass

    @abstractmethod
    def cleanup(self):
        """
        Cleanup the simulation environment.
        """
        pass

class IDFBuildingLoader(BuildingLoader):
    """
    Class to load a building from an IDF file

    Attributes:
        building_file: file in which details of the building are stored.
        idf_objects: IDF objects.
    """

    def __init__(self, building_file, x = 0.0, y = 0.0):
        """
        :param building_file: IDF file containing details of the building.
        :paran x: position of the building on the x-axis
        :paran y: position of the building on the y-axis
        """
        BuildingLoader.__init__(self, building_file, x, y)
        self.idf_objects = op.Epm.load(building_file)

    def get_building_name(self):
        """
        :return: name of the building
        """
        return self.idf_objects.Building.one().name
    def get_building_zones(self):
        """
        :return: name of the building
        """
        zones = []
        for zone_info in self.idf_objects.Zone:
            zone = Zone(zone_info.name)
            for surface in self.idf_objects.BuildingSurface_Detailed.select(
                    lambda x: x.zone_name.name == zone.name):
                number_points = int((len(surface) - 11) / 3)
                points = np.zeros((number_points, 3))
                offset = 0
                for point_ID in range(number_points):
                    points[point_ID][0] = surface[11 + offset]
                    points[point_ID][1] = surface[12 + offset]
                    points[point_ID][2] = surface[13 + offset]
                    offset = offset + 3
                if surface.surface_type == 'wall':
                    exterior_wall = ExteriorWall(surface.name, points)
                    for window_surface in self.idf_objects.FenestrationSurface_Detailed.select(
                        lambda x: x.building_surface_name.name == exterior_wall.name):
                        window_points = np.zeros((4, 3))
                        window_offset = 0
                        for point_ID in range(4):
                            window_points[point_ID][0] = window_surface[9 + window_offset]
                            window_points[point_ID][1] = window_surface[10 + window_offset]
                            window_points[point_ID][2] = window_surface[11 + window_offset]
                            window_offset = window_offset + 3
                        exterior_wall.windows.append(Surface(window_surface.name, window_points))
                    zone.exterior_walls.append(exterior_wall)
                elif surface.surface_type == 'floor':
                    zone.ground_floor = Surface(surface.name, points)
                elif surface.surface_type == 'roof':
                    zone.roofs.append(Surface(surface.name, points))
            zones.append(zone)
        return zones

class CityModelBuildingLoader(BuildingLoader):
    """
    Class to load a building from a 3D city model

    Attributes:
        building_file: file in which details of the building are stored.
        building_name: name of the building to be loaded.
        city_model: city model containing a building.
        template_file: file containg template information of the building.
    """
    __metaclass__ = ABCMeta

    def __init__(self, building_name, city_model, template_file, destination_file):
        """
        :param building_name: name of the building to be loaded.
        :param city_model: city model containing a building.
        :param template_file: file containg template information of the building.
        :param destination_file: file in which details of the building must be stored at the end of the loading.
        """
        self.building_name = building_name
        self.city_model = city_model
        self.template_file = template_file
        self.building_file = destination_file

    def load(self):
        """
        Load the building
        :return: loaded building
        """
        building = BuildingLoader.load(self)
        self.store(building)
        return building

    def get_building_name(self):
        """
        :return: name of the building
        """
        return self.building_name

    def get_building_zones(self):
        """
        :return: name of the building
        """
        return self.city_model.get_zones(self.building_name)
    @abstractmethod
    def store(self, building):
        """
        Store information of the loaded building in a file.
        """
        pass

class IDFCityModelBuildingLoader(CityModelBuildingLoader):
    """
    Class to load a building from a 3D city model and store it in an IDF file.

    Attributes:
        building_file: file in which details of the building are stored.
        building_name: name of the building to be loaded.
        city_model: city model containing a building.
        template_file: file containg template information of the building.
    """
    __metaclass__ = ABCMeta

    def __init__(self, building_name, city_model, template_file, destination_file):
        """
        :param building_name: name of the building to be loaded.
        :param city_model: city model containing a building.
        :param template_file: file containg template information of the building.
        :param destination_file: file in which details of the building must be stored at the end of the loading.
        """
        CityModelBuildingLoader.__init__(self, building_name, city_model, template_file, destination_file)

    def store(self, building):
        """
        Store information of the loaded building in a file.
        :param building: building to be stored.
        """
        adding_procedures = [AddZones(),
                             AddGroundFloorSurface(),
                             AddRoofSurfaces(),
                             AddExteriorWallSurfaces(),
                             AddOutsideSurfaceTemperature(),
                             AddSensibleCoolingLoad(),
                             AddLatentCoolingLoad()]
        idf_objects = op.Epm.load(self.template_file)
        for ap in adding_procedures:
            idf_objects = ap.add(idf_objects, building)
        idf_objects.save(self.building_file)


class AddIDFData():
    """
    Class representing a procedure to add building data into a building energy model.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, idf_objects, building):
        """
        Add IDF data
        :param idf_objects: current status of IDF data
        :param building: building to be stored.
        :return: new status of IDF data
        """
        pass

class AddZones(AddIDFData):
    """
    Class add zones in the EnergyPlus model
    """

    def add(self, idf_objects, building):
        """
        Add zones to IDF data
        :param idf_objects: current status of IDF data
        :param building: building to be stored.
        :return: new status of IDF data
        """
        for z in self.building.zones:
            idf_objects.Zone.add(
                name = z.name,
                floor_area = round(z.get_area().m, 3),
                volume = round(z.get_volume().m, 3)
            )
        return idf_objects

class AddSurfaces(AddIDFData):
    """
    Class add surfaces in the EnergyPlus model
    """
    __metaclass__ = ABCMeta

    def add(self, idf_objects, building):
        """
        Add surfaces to IDF data
        :param idf_objects: current status of IDF data
        :param building: building to be stored.
        :return: new status of IDF data
        """
        for z in building.zones:
            surfaces = self.get_surfaces(z)
            for s in surfaces:
                buidling_surface_detailed = self.get_buidling_surface_detailed(idf_objects, z, s)
                for p in s.points:
                    buidling_surface_detailed.add_fields(p.x, p.y, p.z)
        return idf_objects

    @abstractmethod
    def get_surfaces(self, zone):
        """
        :param zone: zone in which the surface is located
        :return: surfaces to be added in the EnergyPlus file
        """
        pass

    @abstractmethod
    def get_buidling_surface_detailed(self, idf_objects, zone, surface):
        """
        :param idf_objects: current status of IDF data
        :param zone: zone in which the surface is located
        :param surface: surface to be added in the EnergyPlus model
        :return: detailed of the surface
        """
        pass


class AddGroundFloorSurface(AddSurfaces):
    """
    Class add surfaces in the EnergyPlus model
    """
    def get_surfaces(self, zone):
        """
        :param zone: zone in which the surface is located
        :return: surfaces to be added in the EnergyPlus file
        """
        if not zone.ground_floor_surface is None:
            return [zone.ground_floor_surface]
        else:
            return []

    def get_buidling_surface_detailed(self, idf_objects, zone, surface):
        """
        :param idf_objects: current status of IDF data
        :param zone: zone in which the surface is located
        :param surface: surface to be added in the EnergyPlus model
        :return: detailed of the surface
        """
        buidling_surface_detailed = idf_objects.BuildingSurface_Detailed.add(
            name = surface.name,
            surface_type = 'Floor',
            construction_name = 'GROUND FLOOR',
            zone_name = zone.name,
            space_name = '',
            outside_boundary_condition = 'Ground',
            outside_boundary_condition_object = '',
            sun_exposure = 'NoSun',
            wind_exposure = 'NoWind',
            view_factor_to_ground = 'autocalculate',
            number_of_vertices = len(surface.points)
        )
        return buidling_surface_detailed

class AddRoofSurfaces(AddSurfaces):
    """
    Class add surfaces in the EnergyPlus model
    """
    def get_surfaces(self, zone):
        """
        :param zone: zone in which the surface is located
        :return: surfaces to be added in the EnergyPlus file
        """
        if len(zone.roof_surfaces) > 0:
            return zone.roof_surfaces
        else:
            return []

    def get_buidling_surface_detailed(self, idf_objects, zone, surface):
        """
        :param idf_objects: current status of IDF data
        :param zone: zone in which the surface is located
        :param surface: surface to be added in the EnergyPlus model
        :return: detailed of the surface
        """
        buidling_surface_detailed = idf_objects.BuildingSurface_Detailed.add(
            name = surface.name,
            surface_type = 'Roof',
            construction_name = 'ROOF',
            zone_name = zone.name,
            space_name = '',
            outside_boundary_condition = 'Outdoors',
            outside_boundary_condition_object = '',
            sun_exposure = 'SunExposed',
            wind_exposure = 'WindExposed',
            view_factor_to_ground = 'autocalculate',
            number_of_vertices = len(surface.points)
        )
        return buidling_surface_detailed

class AddExteriorWallSurfaces(AddSurfaces):
    """
    Class add surfaces in the EnergyPlus model
    """
    def get_surfaces(self, zone):
        """
        :param zone: zone in which the surface is located
        :return: surfaces to be added in the EnergyPlus file
        """
        if len(zone.exterior_wall_surfaces) > 0:
            return zone.exterior_wall_surfaces
        else:
            return []

    def get_buidling_surface_detailed(self, idf_objects, zone, surface):
        """
        :param idf_objects: current status of IDF data
        :param zone: zone in which the surface is located
        :param surface: surface to be added in the EnergyPlus model
        :return: detailed of the surface
        """
        buidling_surface_detailed = idf_objects.BuildingSurface_Detailed.add(
            name = surface.name,
            surface_type = 'Wall',
            construction_name = 'EXTERIOR WALL',
            zone_name = zone.name,
            space_name = '',
            outside_boundary_condition = 'Outdoors',
            outside_boundary_condition_object = '',
            sun_exposure = 'SunExposed',
            wind_exposure = 'WindExposed',
            view_factor_to_ground = 'autocalculate',
            number_of_vertices = len(surface.points)
        )
        return buidling_surface_detailed

class AddOutputVariable(AddIDFData):
    """
    Class to add an output variable of the EnergyPlus model.
    """
    __metaclass__ = ABCMeta

    def add(self, idf_objects, building):
        """
        Add an output variable into IDF data
        :param idf_objects: current status of IDF data
        :param building: building to be stored.
        :return: the building energy model after adding the output variable
        """
        idf_objects.Output_Variable.add(
            key_value = '*',
            variable_name = self.get_variable_name(),
            reporting_frequency = 'Timestep',
            schedule_name = ''
        )
        return idf_objects


    @abstractmethod
    def get_variable_name(self):
        """
        :return: name of the variable.
        """
        pass

class AddOutsideSurfaceTemperature(AddOutputVariable):
    """
    Class to add the outside surface temperature in the EnergyPlus model.
    """

    def get_variable_name(self):
        """
        :return: name of the variable.
        """
        return 'Surface Outside Face Temperature'

class AddSensibleCoolingLoad(AddOutputVariable):
    """
    Class to add the sensible cooling load in the EnergyPlus model.
    """

    def get_variable_name(self):
        """
        :return: name of the variable.
        """
        return 'Zone Ideal Loads Zone Sensible Cooling Rate'

class AddLatentCoolingLoad(AddOutputVariable):
    """
    Class to add the latent cooling load in the EnergyPlus model.
    """

    def get_variable_name(self):
        """
        :return: name of the variable.
        """
        return 'Zone Ideal Loads Zone Latent Cooling Rate'


class EnergyPlusModel(BuildingEnergyModel):
    """
    Class representing an EnergyPlus model

    Attributes:
        building: building being modelled
        building_loader: loader of building
        outputs: outputs resulting from simulations using the building energy model
    """

    def __init__(self, building_loader):
        """
        :param building_loader: loader of building
        """
        BuildingEnergyModel.__init__(self, building_loader)


    def update(self):
        """
        Update the modelled building with respect to outputs of simulations.
        """
        idcols = self.outputs.keys().to_list()
        for zone in self.building.zones:
            zone_name = zone.name.upper()
            idx_cooling_load = np.where([(zone_name in s) for s in idcols])[0]
            if 'Zone Ideal Loads Zone Sensible Cooling Rate' in idcols[idx_cooling_load[0]]:
                zone.sensible_cooling_load = pd.Series(self.outputs[idcols[idx_cooling_load[0]]] * units.watt, index = self.outputs.index)
                zone.latent_cooling_load = pd.Series(self.outputs[idcols[idx_cooling_load[1]]] * units.watt, index = self.outputs.index)
            else:
                zone.sensible_cooling_load = pd.Series(self.outputs[idcols[idx_cooling_load[1]]] * units.watt, index=self.outputs.index)
                zone.latent_cooling_load = pd.Series(self.outputs[idcols[idx_cooling_load[0]]] * units.watt, index=self.outputs.index)
            for roof in zone.roofs:
                roof_name = roof.name.upper()
                idx_roof_surface_temperature = np.where([(roof_name in s) for s in idcols])[0]
                roof.temperature = pd.Series(self.outputs[idcols[idx_roof_surface_temperature[0]]] * units.degC, index = self.outputs.index)
            for exterior_wall in zone.exterior_walls:
                exterior_wall_name = exterior_wall.name.upper()
                idx_exterior_wall_surface_temperature = np.where([(exterior_wall_name in s) for s in idcols])[0]
                exterior_wall.temperature = pd.Series(self.outputs[idcols[idx_exterior_wall_surface_temperature[0]]] * units.degC, index = self.outputs.index)
                for window in exterior_wall.windows:
                    window_name = window.name.upper()
                    idx_window_surface_temperature = np.where([(window_name in s) for s in idcols])[0]
                    window.temperature = pd.Series(self.outputs[idcols[idx_window_surface_temperature[0]]])
            ground_floor_name = zone.ground_floor.name.upper()
            idx_ground_floor_surface_temperature = np.where([(ground_floor_name in s) for s in idcols])[0]
            zone.ground_floor.temperature = pd.Series(self.outputs[idcols[idx_ground_floor_surface_temperature[0]]] * units.degC, index=self.outputs.index)

def read_ep_outputs(building_name, output_dir, year = datetime.today().year):
    """
    Read outputs generated by the EnergyPlus simulation engine.
    :param building_name: name of the building
    :param output_dir: directory in which the outputs are generated
    :param year: year in which simulation were performed
    :return: outputs as a dataframe
    """
    if platform.system() == 'Windows':
        if output_dir.endswith('\\'):
            output_file = output_dir + building_name + '.csv'
        else:
            output_file = output_dir + '\\' + building_name + '.csv'
    elif platform.system() == 'Linux':
        if output_dir.endswith('/'):
            output_file = output_dir + building_name + '.idfout.csv'
        else:
            output_file = output_dir + '/' + building_name + '.idfout.csv'
    df = pd.read_csv(output_file, index_col=[0])
    idxs = [str(year) + '/' + s[1:] for s in df.index.tolist()]
    idxd = []
    for sd in idxs:
        if '24:' in sd:
            s = sd.replace('24:', '00:')
            d = datetime.strptime(s, '%Y/%m/%d  %H:%M:%S')
            idxd.append(d + timedelta(days=1))
        else:
            idxd.append(datetime.strptime(sd, '%Y/%m/%d  %H:%M:%S'))
    return df.set_index(pd.DatetimeIndex(idxd))

def run_energyplus_linux(input_file):
    command = ["energyplus", "-x", "-r", "-w", os.getenv('ENERGYPLUS') + "/WeatherData/LOCAL_CLIMATE.epw",
               "-p", os.path.basename(input_file), "-d", os.path.dirname(input_file), "-r", input_file]
    subprocess.run(command)

class EnergyPlusSimulationPool(BuildingEnergySimulationPool):
    """
    Pool to perform simulations using EnergyPlus in parallel.

    Attributes:
        nproc: number of processors to run in parallel.
        pool: list of building energy models used for parallel simulations.
        output_dir: directory in which parallel simulations must be performed and outputs being stored.
    """
    def __init__(self, weather_data_loader, nproc = 2, output_dir = '.'):
        BuildingEnergySimulationPool.__init__(self, weather_data_loader, nproc)
        self.output_dir = output_dir
    def create_simulation_environment(self):
        """
        Create simulation environment to perform simulations using the pool of building energy models
        """
        ENERGYPLUS_DIR = os.getenv('ENERGYPLUS')
        if (self.output_dir != '.') and (not os.path.isdir(self.output_dir)):
            os.mkdir(self.output_dir)
        for bem in self.pool:
            shutil.copy(bem.building_loader.building_file, self.output_dir)
        if platform.system() == 'Windows':
            shutil.copy(ENERGYPLUS_DIR + '\\RunDirMulti.bat', self.output_dir)
            if self.weather_data is not None:
                self.weather_data_loader = EPWDataLoader(ENERGYPLUS_DIR + '\\WeatherData\\LOCAL_CLIMATE.epw', year=self.weather_data_loader.get_year())
        elif platform.system() == 'Linux':
            if self.weather_data is not None:
                self.weather_data_loader = EPWDataLoader(ENERGYPLUS_DIR + '/WeatherData/LOCAL_CLIMATE.epw', year=self.weather_data_loader.get_year())
    def get_weather_data_filename(self):
        """
        :return: filename under which weather data must be saved.
        """
        return 'LOCAL_CLIMATE.epw'
    def get_weather_data_directory(self):
        """
        :return: directory under which weather data must be saved.
        """
        if platform.system() == 'Windows':
            return os.getenv('ENERGYPLUS') + '\\WeatherData'
        elif platform.system() == 'Linux':
            return os.getenv('ENERGYPLUS') + '/WeatherData'


    def run_parallel_simulation(self):
        """
        Run parallel building energy simulations.
        """
        if platform.system() == 'Windows':
            p = Popen('RunDirMulti.bat LOCAL_CLIMATE ' + str(self.nproc), cwd=self.output_dir, shell=True)
            p.communicate()
        elif platform.system() == 'Linux':
            if self.output_dir.endswith("/"):
                input_files = [self.output_dir + file for file in os.listdir(self.output_dir) if file.endswith(".idf")]
            else:
                input_files = [self.output_dir + "/" + file for file in os.listdir(self.output_dir) if file.endswith(".idf")]
            for input_file in input_files:
                run_energyplus_linux(input_file)

    def get_building_outputs(self, building_name):
        """
        :param building_name: name of the building
        :return: outputs of the simulation for the building
        """
        return read_ep_outputs(building_name, self.output_dir, year = self.weather_data.year)

    def cleanup(self):
        """
        Cleanup the simulation environment.
        """
        if platform.system() == 'Windows':
            for f in glob.glob(self.output_dir + '\\*.audit'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '\\*.bnd'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '\\*.csv'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '\\*.eio'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '\\*.err'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '\\*.eso'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '\\*.expidf'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '\\*.idf'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '\\*.mdd'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '\\*.mtd'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '\\*.rdd'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '\\*.rvaudit'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '\\*.shd'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '\\*.sql'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '\\*.svg'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '\\*.html'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '\\tempsim*'):
                shutil.rmtree(f)
            os.remove(self.output_dir + '\\RunDirMulti.bat')
        elif platform.system() == 'Linux':
            for f in glob.glob(self.output_dir + '/*.audit'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '/*.bnd'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '/*.csv'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '/*.eio'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '/*.err'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '/*.eso'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '/*.expidf'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '/*.idf'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '/*.mdd'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '/*.mtd'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '/*.rdd'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '/*.rvaudit'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '/*.shd'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '/*.sql'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '/*.svg'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '/*.html'):
                os.remove(f)
            for f in glob.glob(self.output_dir + '/tempsim*'):
                shutil.rmtree(f)



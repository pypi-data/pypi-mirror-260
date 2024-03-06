"""
Module to create and update urban microclimate models, and perform urban microclimate simulations in sequence or parallel.

Delft University of Technology
Dr. Miguel Martin
"""
import math
from abc import ABCMeta, abstractmethod
import numpy as np
from datetime import datetime, timedelta
from metpy.calc import *
from metpy.units import units
from metpy.constants import dry_air_density_stp, dry_air_spec_heat_press, water_heat_vaporization
import scipy.signal as sig
import scipy.optimize as opt
from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.termination import get_termination
from pymoo.optimize import minimize
from pymoo.core.problem import StarmapParallelization
from sklearn.metrics import mean_squared_error
import multiprocessing

import pandas as pd
import parseidf

from sciencespy.dom import *
from sciencespy.bem import *


class UrbanMicroclimateModel():
    """
    Class representing an urban microclimate model.

    Attributes:
        pool_bems: pool of models that are used to perform building energy simulations.
    """

    __metaclass__ = ABCMeta

    def __init__(self, pool_bems):
        """
        :param pool_bems: pool of models that are used to perform building energy simulations.
        """
        self.pool_bems = pool_bems

    @abstractmethod
    def run(self, start_date, end_date, dt = timedelta(hours = 1)):
        """
        Perform simulation of the urban microclimate model
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        pass

class StreetCanyonLoader():
    """
    Class to load a street canyon.

    Attributes:
        street_canyon_name: name of the street canyon
        neighborhood_file: file containing details of the neighborhood in which the street canyon is located.
        bems_pool: pool of models that are used to perform building energy simulations.
    """
    __metaclass__ = ABCMeta

    def __init__(self, street_canyon_name, neighborhood_file, bems_pool):
        """
        :param street_canyon_name: name of the street canyon
        :param neighborhood_file: file containing details of the neighborhood in which the street canyon is located.
        :param bems_pool: pool of models that are used to perform building energy simulations.
        """
        self.street_canyon_name = street_canyon_name
        self.neighborhood_file = neighborhood_file
        self.bems_pool = bems_pool

    def load(self):
        """
        Load the street canyon from a file.
        :return: loaded street canyon.
        """
        street_canyon = StreetCanyon(self.street_canyon_name)
        street_canyon.atmosphere = self.get_street_canyon_atmosphere()
        street_canyon.pavements = self.get_street_canyon_pavements()
        street_canyon.surrounding_walls = self.get_street_canyon_surrounding_walls()
        street_canyon.waste_heat_sources_to_street_canyon = self.get_street_canyon_waste_heat_sources()
        street_canyon.traffic = self.get_street_canyon_traffic()
        street_canyon.vegetation = self.get_street_canyon_vegetation()
        street_canyon.weather_stations = self.get_street_canyon_weather_stations()
        return street_canyon

    @abstractmethod
    def get_street_canyon_atmosphere(self):
        """
        :return: atmoshperic layer of the street canyon
        """
        pass

    @abstractmethod
    def get_street_canyon_pavements(self):
        """
        :return: pavements of the street canyon
        """
        pass

    @abstractmethod
    def get_street_canyon_surrounding_walls(self):
        """
        :return: surrounding walls of the street canyon
        """
        pass

    @abstractmethod
    def get_street_canyon_waste_heat_sources(self):
        """
        :return: waste heat sources of the street canyon
        """
        pass

    @abstractmethod
    def get_street_canyon_traffic(self):
        """
        :return: traffic of the street canyon
        """
        pass

    @abstractmethod
    def get_street_canyon_vegetation(self):
        """
        :return: traffic of the street canyon
        """
        pass

    @abstractmethod
    def get_street_canyon_weather_stations(self):
        """
        :return: weather stations in the street canyon
        """
        pass


class UrbanCanopyModel(UrbanMicroclimateModel):
    """
    Class representing an urban canopy model.

    Attributes:
        street_canyon: street canyon being modelled by the urban canopy model.
        street_canyon_loader: loader of the street canyon.
    """
    __metaclass__ = ABCMeta

    def __init__(self, street_canyon_loader):
        """
        :param street_canyon_loader: loader of the street canyon.
        """
        UrbanMicroclimateModel.__init__(self, street_canyon_loader.bems_pool)
        self.street_canyon = None
        self.street_canyon_loader = street_canyon_loader

    def run(self, start_date, end_date, dt = timedelta(hours = 1)):
        """
        Perform simulation of the urban microclimate model
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        if self.street_canyon is None:
            self.street_canyon = self.street_canyon_loader.load()
        self.update_street_canyon(start_date, end_date, dt)

    @abstractmethod
    def update_street_canyon(self, start_date, end_date, dt):
        """
        Update the status of the street canyon.
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        pass

class PavementTemperatureLoader():
    """
    Class to load the temperature of the pavement.

    Attributes:
        pavement_temperature_file: file containing the temperature of the pavement.
    """
    __metaclass__ = ABCMeta

    def __init__(self, pavement_temperature_file):
        """
        :param pavement_temperature_file: file containing the temperature of the pavement.
        """
        self.pavement_temperature_file = pavement_temperature_file

    def load(self):
        """
        Load the street canyon from a file.
        :return: loaded street canyon.
        """
        pavement_temperature = self.get_pavement_temperature()
        return pavement_temperature

    @abstractmethod
    def get_pavement_temperature(self):
        """
        :return: temperature of the pavement (in degree Celsius)
        """
        pass

class CSVPavementTemperatureLoader(PavementTemperatureLoader):
    """
    Class to load the temperature of the pavement from a .csv file.

    Attributes:
        pavement_temperature_file: file containing the temperature of the pavement.
    """
    __metaclass__ = ABCMeta

    def __init__(self, pavement_temperature_file):
        """
        :param pavement_temperature_file: file containing the temperature of the pavement.
        """
        PavementTemperatureLoader.__init__(self, pavement_temperature_file)

    def get_pavement_temperature(self):
        """
        :return: temperature of the pavement (in degree Celsius)
        """
        return pd.read_csv(self.pavement_temperature_file, index_col=0, parse_dates=True,
                           date_parser=lambda x: pd.to_datetime(x, format='%d/%m/%Y %H:%M'))

class WeatherStationDataLoader():
    """
    Class to load data collected from a weather station.

    Attributes:
        weather_station_file: file containing data collected by a weather station.
    """
    __metaclass__ = ABCMeta

    def __init__(self, weather_station_file):
        """
        :param weather_station_file: file containing data collected by a weather station.
        """
        self.weather_station_file = weather_station_file

    def load(self):
        """
        Load the street canyon from a file.
        :return: loaded street canyon.
        """
        weather_data = self.get_weather_data()
        return weather_data

    @abstractmethod
    def get_weather_data(self):
        """
        :return: weather data collected by the station.
        """
        pass

class CSVWeatherStationDataLoader(WeatherStationDataLoader):
    """
    Class to load data collected from a weather station using the .csv format.

    Attributes:
        weather_station_file: .csv file containing data collected by a weather station.
    """

    def __init__(self, weather_station_file):
        """
        :param weather_station_file: .csv file containing data collected by a weather station.
        """
        WeatherStationDataLoader.__init__(self, weather_station_file)

    def get_weather_data(self):
        """
        :return: weather data collected by the station.
        """
        return pd.read_csv(self.weather_station_file, index_col=0, parse_dates=True,
                           date_parser=lambda x: pd.to_datetime(x, format='%d/%m/%Y %H:%M'))

class AtmosphericDataLoader():
    """
    Class to load data at the atmospheric layer

    Attributes:
        atmospheric_file: file containing data at the atmospheric layer.
    """
    __metaclass__ = ABCMeta

    def __init__(self, atmospheric_file):
        """
        :param atmospheric_file: file containing data at the atmospheric layer.
        """
        self.atmospheric_file = atmospheric_file

    def load(self):
        """
        Load atmospheric data from a file.
        :return: loaded atmospheric data.
        """
        atmospheric_data = self.get_atmospheric_data()
        return atmospheric_data

    @abstractmethod
    def get_atmospheric_data(self):
        """
        :return: atmospheric data.
        """
        pass

class EPWAtmosphericDataLoader(AtmosphericDataLoader):
    """
    Class to load data at the atmospheric layer from .epw file.

    Attributes:
        atmospheric_file: file containing data at the atmospheric layer.
    """

    def __init__(self, atmospheric_file):
        """
        :param atmospheric_file: file containing data at the atmospheric layer.
        """
        AtmosphericDataLoader.__init__(self, atmospheric_file)

    def get_atmospheric_data(self):
        """
        :return: atmospheric data.
        """
        epw_weather_data = EPWDataLoader(self.atmospheric_file, year = 2019).load()
        temperature = epw_weather_data.outdoor_air_temperature
        relative_humidity = epw_weather_data.outdoor_air_relative_humidity
        pressure = epw_weather_data.outdoor_air_pressure
        dew_point = dewpoint_from_relative_humidity(temperature, relative_humidity)
        specific_humidity = specific_humidity_from_dewpoint(pressure, dew_point)
        d = {'Atmospheric Temperature': temperature, 'Atmospheric Humidity': specific_humidity}
        return pd.DataFrame(index=epw_weather_data.timestamps, data = d)


class IDFStreetCanyonLoader(StreetCanyonLoader):
    """
    Class to load a street canyon.

    Attributes:
        street_canyon_name: name of the street canyon
        neighborhood_file: file containing details of the neighborhood in which the street canyon is located.
        bems_pool: pool of models that are used to perform building energy simulations.
        idf_objects: IDF objects containing information of the street canyon.
        atmospheric_data_dir: directory containing atmospheric data
        pavement_temperature_dir: directory containing measurements of the surface temperature.
        weather_data_dir: directory in which are stored weather data collected by several stations.
    """

    def __init__(self, street_canyon_name, neighborhood_file, bems_pool, atmosphere_dir = '.', pavement_temperature_dir = '.', weather_data_dir = '.'):
        """
        :param street_canyon_name: name of the street canyon
        :param neighborhood_file: file containing details of the neighborhood in which the street canyon is located.
        :param bems_pool: pool of models that are used to perform building energy simulations.
        :param atmosphere_dir: directory containing measurements at the atmospheric layer.
        :param pavement_temperature_dir: directory containing measurements of the surface temperature.
        :param weather_data_dir: directory in which are stored weather data collected by several stations.
        """
        StreetCanyonLoader.__init__(self, street_canyon_name, neighborhood_file, bems_pool)
        with open(self.neighborhood_file, 'r') as f:
            self.idf_objects = parseidf.parse(f.read())
        self.pavement_temperature_dir = pavement_temperature_dir
        self.weather_data_dir = weather_data_dir
        self.atmosphere_dir = atmosphere_dir

    def __get_idf_object_street_canyon(self):
        """
        :return: IDF object corresponding to the street canyon
        """
        idf_object_street_canyon = None
        n_street_canyons = len(self.idf_objects['STREETCANYON'])
        for n in range(n_street_canyons):
            if self.idf_objects['STREETCANYON'][n][1] == self.street_canyon_name:
                idf_object_street_canyon = self.idf_objects['STREETCANYON'][n]
                break
        return idf_object_street_canyon

    def get_street_canyon_atmosphere(self):
        """
        :return: atmoshperic layer of the street canyon
        """
        idf_object_street_canyon = self.__get_idf_object_street_canyon()
        atmosphere = Atmosphere()
        if platform.system() == 'Windows':
            atmospheric_data = EPWAtmosphericDataLoader(self.atmosphere_dir + '\\' + idf_object_street_canyon[2] + '.epw').load()
        elif platform.system() == 'Linux':
            atmospheric_data = EPWAtmosphericDataLoader(self.atmosphere_dir + '/' + idf_object_street_canyon[2] + '.epw').load()
        atmosphere.temperature = pd.Series(index=atmospheric_data.index, data=atmospheric_data['Atmospheric Temperature'])
        atmosphere.humidity = pd.Series(index=atmospheric_data.index, data=atmospheric_data['Atmospheric Humidity'])
        return atmosphere

    def get_street_canyon_pavements(self):
        """
        :return: pavements of the street canyon
        """
        idf_object_street_canyon = self.__get_idf_object_street_canyon()
        pavements = []
        name_list_pavements = idf_object_street_canyon[4]
        for r in range(len(self.idf_objects['STREETCANYON:PAVEMENTS'])):
            if name_list_pavements == self.idf_objects['STREETCANYON:PAVEMENTS'][r][1]:
                number_pavements = len(self.idf_objects['STREETCANYON:PAVEMENTS'][r]) - 2
                for p in range(number_pavements):
                    pavement_name = self.idf_objects['STREETCANYON:PAVEMENTS'][r][p + 2]
                    for m in range(len(self.idf_objects['PAVEMENT'])):
                        if pavement_name == self.idf_objects['PAVEMENT'][m][1]:
                            pavement_points = []
                            count = 2
                            for n in range(int((len(self.idf_objects['PAVEMENT'][0]) - 2) / 2)):
                                pavement_points.append([float(self.idf_objects['PAVEMENT'][0][count]),
                                                        float(self.idf_objects['PAVEMENT'][0][count + 1]),
                                                        0.0])
                                count = count + 2
                            pavement = Surface(pavement_name, np.array(pavement_points))
                            if platform.system() == 'Windows':
                                pavement_temperature_loader = CSVPavementTemperatureLoader(self.pavement_temperature_dir + '\\' + pavement_name + '.csv')
                            elif platform.system() == 'Linux':
                                pavement_temperature_loader = CSVPavementTemperatureLoader(self.pavement_temperature_dir + '/' + pavement_name + '.csv')
                            pavement_temperature = pavement_temperature_loader.load()
                            pavement.temperature = pd.Series(index=pavement_temperature.index, data=pavement_temperature['Surface Temperature'].values * units.degC)
                            pavements.append(pavement)
        return pavements

    def get_street_canyon_surrounding_walls(self):
        """
        :return: surrounding walls of the street canyon
        """
        idf_object_street_canyon = self.__get_idf_object_street_canyon()
        surrounding_walls = []
        name_list_surrounding_walls = idf_object_street_canyon[3]
        for r in range(len(self.idf_objects['SURROUNDINGWALLS'])):
            if name_list_surrounding_walls == self.idf_objects['SURROUNDINGWALLS'][r][1]:
                number_list_surrounding_walls_per_building = len(self.idf_objects['SURROUNDINGWALLS'][r]) - 2
                for spb in range(number_list_surrounding_walls_per_building):
                    name_list_surrounding_walls_per_building =  self.idf_objects['SURROUNDINGWALLS'][r][spb + 2]
                    for sws in range(len(self.idf_objects['SURROUNDINGWALLS:BUILDING'])):
                        if name_list_surrounding_walls_per_building == self.idf_objects['SURROUNDINGWALLS:BUILDING'][sws][1]:
                            number_surrounding_walls = len(self.idf_objects['SURROUNDINGWALLS:BUILDING'][sws]) - 3
                            name_building = self.idf_objects['SURROUNDINGWALLS:BUILDING'][sws][2]
                            for sw in range(number_surrounding_walls):
                                name_surrounding_wall = self.idf_objects['SURROUNDINGWALLS:BUILDING'][sws][sw + 3].lower()
                                for bem in self.bems_pool.pool:
                                    if name_building == bem.building.name:
                                        surrounding_walls.append(bem.building.get_exterior_wall(name_surrounding_wall))
        return surrounding_walls

    def get_street_canyon_waste_heat_sources(self):
        """
        :param pool_bems: pool of models that are used to perform building energy simulations.
        :return: waste heat sources of the street canyon
        """
        try:
            waste_heat_sources = []
            for q in range(len(self.idf_objects['WASTEHEATSOURCE'])):
                name_waste_heat_source = self.idf_objects['WASTEHEATSOURCE'][q][1]
                cwhg = float(self.idf_objects['WASTEHEATSOURCE'][q][2])
                fhs = float(self.idf_objects['WASTEHEATSOURCE'][q][3])
                buildings = []
                number_of_buildings = len(self.idf_objects['WASTEHEATSOURCE'][q]) - 2
                for nb in range(number_of_buildings):
                    building_name = self.idf_objects['WASTEHEATSOURCE'][q][nb + 2]
                    for bem in self.bems_pool.pool:
                        if building_name == bem.building.name:
                            buildings.append(bem.building)
                waste_heat_sources.append(WasteHeat(name_waste_heat_source, buildings, cwhg, fhs))
            idf_object_street_canyon = self.__get_idf_object_street_canyon()
            waste_heat_sources_to_street_canyon = []
            name_list_waste_heat_sources_to_street_canyon = idf_object_street_canyon[6]
            for r in range(len(self.idf_objects['WASTEHEATSOURCE:LIST'])):
                if name_list_waste_heat_sources_to_street_canyon == self.idf_objects['WASTEHEATSOURCE:LIST'][r][1]:
                    number_waste_heat_sources_to_street_canyon = len(self.idf_objects['WASTEHEATSOURCE:LIST'][r]) - 2
                    for whstosc in range(number_waste_heat_sources_to_street_canyon):
                        name_waste_heat_sources_to_street_canyon = self.idf_objects['WASTEHEATSOURCE:LIST'][r][whstosc + 2]
                        for p in range(len(self.idf_objects['WASTEHEATSOURCE:STREETCANYON'])):
                            if name_waste_heat_sources_to_street_canyon == self.idf_objects['WASTEHEATSOURCE:STREETCANYON'][p][1]:
                                name_waste_heat_source = self.idf_objects['WASTEHEATSOURCE:STREETCANYON'][p][2]
                                fraction = float(self.idf_objects['WASTEHEATSOURCE:STREETCANYON'][p][3])
                                for whs in waste_heat_sources:
                                    if name_waste_heat_source == whs.name:
                                        waste_heat_sources_to_street_canyon.append(WasteHeatToStreetCanyon(name_waste_heat_sources_to_street_canyon, whs, fraction))
        except KeyError:
            waste_heat_sources_to_street_canyon = []
        return waste_heat_sources_to_street_canyon

    def get_street_canyon_traffic(self):
        """
        :return: traffic of the street canyon
        """
        # TODO: Implementation
        return []

    def get_street_canyon_vegetation(self):
        """
        :return: vegetation of the street canyon
        """
        # TODO: Implementation
        return []

    def get_street_canyon_weather_stations(self):
        """
        :return: weather stations in the street canyon
        """
        idf_object_street_canyon = self.__get_idf_object_street_canyon()
        weather_stations = []
        name_list_weather_stations = idf_object_street_canyon[9]
        for r in range(len(self.idf_objects['WEATHERSTATIONS'])):
            if name_list_weather_stations == self.idf_objects['WEATHERSTATIONS'][r][1]:
                number_weather_stations = len(self.idf_objects['WEATHERSTATIONS'][r]) - 2
                for n in range(number_weather_stations):
                    weather_station = WeatherStation(self.idf_objects['WEATHERSTATIONS'][r][n + 2])
                    if platform.system() == 'Windows':
                        weather_station_data = CSVWeatherStationDataLoader(self.weather_data_dir + '\\' + weather_station.name + '.csv').load()
                    elif platform.system() == 'Linux':
                        weather_station_data = CSVWeatherStationDataLoader(self.weather_data_dir + '/' + weather_station.name + '.csv').load()
                    weather_station.temperature = pd.Series(index=weather_station_data.index, data=weather_station_data['Outdoor Air Temperature'])
                    weather_station.humidity = pd.Series(index=weather_station_data.index, data=weather_station_data['Outdoor Air Relative Humidity'])
                    weather_station.pressure = pd.Series(index=weather_station_data.index, data=weather_station_data['Outdoor Air Pressure'])
                    weather_stations.append(weather_station)
        return weather_stations

class DataDrivenUrbanCanopyModel(UrbanCanopyModel):
    """
    Class representing a data driven urban canopy model.

    Attributes:
        street_canyon: street canyon being modelled by the urban canopy model.
        street_canyon_loader: loader of the street canyon.
        training_split_ratio: ratio between the size of the training set and the total data set over the period of simulation.
        measured_outdoor_air_temperature: outoor air temperature as measured by a set of weather stations in the street canyon.
        measured_outdoor_air_humidity: outdoor air specific huimdity as measured by a set of weather stations in the street canyon.
    """
    __metaclass__ = ABCMeta

    def __init__(self, street_canyon_loader, training_split_ratio = 0.0):
        """
        :param urban_microclimate_file: file containing details of the data driven urban canopy model.
        :param training_split_ratio: ratio between the size of the training set and the total data set over the period of simulation
        """
        UrbanCanopyModel.__init__(self, street_canyon_loader)
        self.training_split_ratio = training_split_ratio
        self.measured_outdoor_air_temperature = None
        self.measured_outdoor_air_humidity = None

    def get_measured_outdoor_air_temperature(self):
        n_weather_stations = len(self.street_canyon.weather_stations)
        outdoor_air_temperature = self.street_canyon.weather_stations[0].temperature.copy()
        for n in range(1, n_weather_stations):
            outdoor_air_temperature += self.street_canyon.weather_stations[n].temperature
        return outdoor_air_temperature / n_weather_stations

    def get_measured_outdoor_air_humidity(self):
        n_weather_stations = len(self.street_canyon.weather_stations)
        outdoor_air_temperature = self.get_measured_outdoor_air_temperature()
        outdoor_air_relative_humidity = self.street_canyon.weather_stations[0].humidity.copy()
        outdoor_air_pressure = self.street_canyon.weather_stations[0].pressure.copy()
        for n in range(1, n_weather_stations):
            outdoor_air_relative_humidity += self.street_canyon.weather_stations[n].humidity
            outdoor_air_pressure += self.street_canyon.weather_stations[n].pressure
        outdoor_air_relative_humidity = outdoor_air_relative_humidity / n_weather_stations
        outdoor_air_pressure = outdoor_air_pressure / n_weather_stations
        outdoor_air_dew_point = dewpoint_from_relative_humidity(
            self.measured_outdoor_air_temperature.values * units.degC, outdoor_air_relative_humidity.values * units.percent)
        outdoor_air_specific_humidity = specific_humidity_from_dewpoint(outdoor_air_pressure.values * units.hPa, outdoor_air_dew_point)
        return pd.Series(index=outdoor_air_temperature.index, data=outdoor_air_specific_humidity)

    def update_street_canyon(self, start_date, end_date, dt):
        """
        Update the status of the street canyon.
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        n_weather_stations = len(self.street_canyon.weather_stations)
        if self.measured_outdoor_air_temperature is None:
            self.measured_outdoor_air_temperature = self.get_measured_outdoor_air_temperature()
        if self.measured_outdoor_air_humidity is None:
            self.measured_outdoor_air_humidity = self.get_measured_outdoor_air_humidity()
        if self.training_split_ratio > 0.0:
            dsplit = int(self.training_split_ratio * (end_date - start_date) / dt)
            split_date = start_date + dsplit * dt
            self.train(start_date, split_date, dt)
            previous_error_temperature = self.get_previous_error_temperature(start_date, split_date, dt)
            current_error_temperature = self.get_current_error_temperature(start_date, split_date, dt)
            previous_error_humidity = self.get_previous_error_humidity(start_date, split_date, dt)
            current_error_humidity = self.get_current_error_temperature(start_date, split_date, dt)
            if previous_error_temperature > current_error_temperature:
                self.update_previous_solution()
            self.test(split_date, end_date, dt)
        else:
            self.test(start_date, end_date, dt)


    @abstractmethod
    def train(self, start_date, end_date, dt):
        """
        Train the data driven urban canopy model
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        pass

    @abstractmethod
    def test(self, start_date, end_date, dt):
        """
        Test the data driven urban canopy model
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        pass

    @abstractmethod
    def get_previous_error_temperature(self, start_date, end_date, dt):
        """
        Previous error made on temperature
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        pass

    @abstractmethod
    def get_current_error_temperature(self, start_date, end_date, dt):
        """
        Current error made on temperature
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        pass

    @abstractmethod
    def get_previous_error_humidity(self, start_date, end_date, dt):
        """
        Previous error made on humidity
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        pass

    @abstractmethod
    def get_current_error_humidity(self, start_date, end_date, dt):
        """
        Current error made on humidity
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        pass

    @abstractmethod
    def update_previous_solution(self):
        """
        Update previous solution found by the data driven model
        """
        pass

    @abstractmethod
    def get_solution(self):
        """
        :return: dictionary showing information about solution found by the data driven UCM
        """
        pass

class DummyDataDrivenUrbanCanopyModel(DataDrivenUrbanCanopyModel):
    """
    Class representing a dummy data driven urban canopy model.

    Attributes:
        street_canyon: street canyon being modelled by the urban canopy model.
        street_canyon_loader: loader of the street canyon.
        training_split_ratio: ratio between the size of the training set and the total data set over the period of simulation.
    """
    __metaclass__ = ABCMeta

    def __init__(self, street_canyon_loader, training_split_ratio = 0.0):
        """
        :param urban_microclimate_file: file containing details of the data driven urban canopy model.
        :param training_split_ratio: ratio between the size of the training set and the total data set over the period of simulation
        """
        DataDrivenUrbanCanopyModel.__init__(self, street_canyon_loader, training_split_ratio)

    def train(self, start_date, end_date, dt):
        """
        Train the data driven urban canopy model
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        self.street_canyon.temperature = self.measured_outdoor_air_temperature[start_date:end_date].resample(dt).interpolate()
        self.street_canyon.humidity = self.measured_outdoor_air_humidity[start_date:end_date].resample(dt).interpolate()

    def test(self, start_date, end_date, dt):
        """
        Test the data driven urban canopy model
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        if self.street_canyon.temperature is not None:
            self.street_canyon.temperature = pd.concat([self.street_canyon.temperature, self.measured_outdoor_air_temperature[start_date:end_date].resample(dt).interpolate()])
        else:
            self.street_canyon.temperature = self.measured_outdoor_air_temperature[start_date:end_date].resample(dt).interpolate()
        if self.street_canyon.humidity is not None:
            self.street_canyon.humidity = pd.concat([self.street_canyon.humidity, self.measured_outdoor_air_humidity[start_date:end_date].resample(dt).interpolate()])
        else:
            self.street_canyon.humidity = self.measured_outdoor_air_humidity[start_date:end_date].resample(dt).interpolate()

    def get_previous_error_temperature(self, start_date, end_date, dt):
        """
        Previous error made on temperature
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        return math.sqrt(mean_squared_error(self.street_canyon.temperature.values, self.measured_outdoor_air_temperature[start_date:end_date].resample(dt).interpolate().values))

    def get_current_error_temperature(self, start_date, end_date, dt):
        """
        Current error made on temperature
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        return self.get_previous_error_temperature(start_date, end_date, dt)

    def get_previous_error_humidity(self, start_date, end_date, dt):
        """
        Previous error made on humidity
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        return math.sqrt(mean_squared_error(self.street_canyon.humidity.values, self.measured_outdoor_air_humidity[start_date:end_date].resample(dt).interpolate().values))

    def get_current_error_humidity(self, start_date, end_date, dt):
        """
        Current error made on humidity
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        return self.get_previous_error_humidity(start_date, end_date, dt)

    def update_previous_solution(self):
        """
        Update previous solution found by the data driven model
        """
        pass

    def get_solution(self):
        """
        :return: dictionary showing information about solution found by the data driven UCM
        """
        return dict()


class LinearStateSpaceUrbanCanopyModel(DataDrivenUrbanCanopyModel):
    """
    Class representing a data driven urban canopy model.

    Attributes:
        street_canyon: street canyon being modelled by the urban canopy model.
        street_canyon_loader: loader of the street canyon.
        training_split_ratio: ratio between the size of the training set and the total data set over the period of simulation.
        n_processes: number of parallel processes to be used to speed up the training phase of the data driven urban canopy model.
        previous_chtcs: previously found convective heat transfer coefficients.
        current_chtcs: currently found convective heat transfer coefficients.
    """

    def __init__(self, street_canyon_loader, training_split_ratio = 0.0, n_processes = 2):
        """
        :param urban_microclimate_file: file containing details of the data driven urban canopy model.
        :param training_split_ratio: ratio between the size of the training set and the total data set over the period of simulation
        :param max_iter: maximum number of iterations to achieve convergence
        """
        DataDrivenUrbanCanopyModel.__init__(self, street_canyon_loader, training_split_ratio)
        self.n_processes = n_processes
        self.previous_chtcs = None
        self.current_chtcs = None


    def get_input_vectors(self, start_date, end_date, dt):
        """
        :param street_canyon: state of the street canyon before training and testing
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        :return: input vectors of the linear state space
        """
        input_vectors = []
        for sw in self.street_canyon.surrounding_walls:
            input_vectors.append(sw.get_surface_temperature().resample(dt).interpolate()[start_date:end_date].values.tolist())
        input_vectors.append(self.street_canyon.atmosphere.temperature.resample(dt).interpolate()[start_date:end_date].values.tolist())
        for p in self.street_canyon.pavements:
            input_vectors.append(p.get_surface_temperature().resample(dt).interpolate()[start_date:end_date].values.tolist())
        for v in self.street_canyon.vegetation:
            input_vectors.append(v.get_surface_temperature().resample(dt).interpolate()[start_date:end_date].values.tolist())
        for wh in self.street_canyon.waste_heat_sources_to_street_canyon:
            input_vectors.append(wh.get_sensible_heat().resample(dt).interpolate()[start_date:end_date].values.tolist())
        for t in self.street_canyon.traffic:
            input_vectors.append(t.get_sensible_heat().resample(dt).interpolate()[start_date:end_date].values.tolist())
        input_vectors.append(self.street_canyon.atmosphere.humidity.resample(dt).interpolate()[start_date:end_date].values.tolist())
        sea_level_pressure = 1013.25 * units.hPa
        for p in self.street_canyon.pavements:
            pavement_saturated_mixing_ratio = saturation_mixing_ratio(sea_level_pressure, p.temperature.resample(dt).interpolate()[start_date:end_date].values * units.degC)
            pavement_humidity = specific_humidity_from_mixing_ratio(pavement_saturated_mixing_ratio)
            input_vectors.append(pavement_humidity.m.tolist())
        for v in self.street_canyon.vegetation:
            vegetation_saturated_mixing_ratio = saturation_mixing_ratio(sea_level_pressure, v.temperature.resample(dt).interpolate()[start_date:end_date].values * units.degC)
            vegetation_humidity = specific_humidity_from_mixing_ratio(vegetation_saturated_mixing_ratio)
            input_vectors.append(vegetation_humidity.m.tolist())
        for wh in self.street_canyon.waste_heat_sources_to_street_canyon:
            input_vectors.append(wh.get_latent_heat().resample(dt).interpolate()[start_date:end_date].values.tolist())
        for t in self.street_canyon.traffic:
            input_vectors.append(t.get_latent_heat().resample(dt).interpolate()[start_date:end_date].values.tolist())
        return np.asarray(input_vectors)

    def get_state_matrix(self, h):
        """
        :param h: vector of convective heat transfer coefficients.
        :return: state matrix of the linear state space model.
        """
        sensible_area_vector = []
        latent_area_vector = []
        for sw in self.street_canyon.surrounding_walls:
            sensible_area_vector.append(sw.get_area().m)
            latent_area_vector.append(0.0)
        sensible_area_vector.append(self.street_canyon.get_surface().get_area().m)
        latent_area_vector.append(self.street_canyon.get_surface().get_area().m)
        for p in self.street_canyon.pavements:
            sensible_area_vector.append(p.get_area().m)
            latent_area_vector.append(p.get_area().m)
        for v in self.street_canyon.vegetation:
            sensible_area_vector.append(v.get_area().m)
            latent_area_vector.append(v.get_area().m)
        sensible_area_vector = np.transpose(np.asarray(sensible_area_vector))
        latent_area_vector = np.transpose(np.asarray(latent_area_vector))
        A = np.zeros(shape=(2, 2))
        A[0, 0] = np.dot(h, sensible_area_vector)
        A[1, 1] = np.dot(h, latent_area_vector)
        return - A / (self.street_canyon.get_volume().m * dry_air_density_stp.m * dry_air_spec_heat_press.m)

    def get_input_matrix(self, h):
        """
        :param h: vector of convective heat transfer coefficients.
        :return: state matrix of the linear state space model.
        """
        n_surrounding_walls = len(self.street_canyon.surrounding_walls)
        n_pavements = len(self.street_canyon.pavements)
        n_vegetation = len(self.street_canyon.vegetation)
        n_waste_heat_sources = len(self.street_canyon.waste_heat_sources_to_street_canyon)
        n_traffic = len(self.street_canyon.traffic)
        N = n_surrounding_walls + 2 * n_pavements + 2 * n_vegetation + 2 * n_waste_heat_sources + 2 * n_traffic + 2
        B = np.zeros(shape=(2, N))
        latent_offset = n_surrounding_walls + n_pavements + n_vegetation + n_waste_heat_sources + n_traffic + 1
        counter = 0
        for sw in self.street_canyon.surrounding_walls:
            B[0, counter] = h[counter] * sw.get_area().m
            counter += 1
        B[0, counter] = h[counter] * self.street_canyon.get_surface().get_area().m
        B[1, latent_offset] = h[counter] * self.street_canyon.get_surface().get_area().m
        counter += 1
        latent_counter = 1
        for p in self.street_canyon.pavements:
            B[0, counter] = h[counter] * p.get_area().m
            B[1, latent_counter + latent_offset] = h[counter] * p.get_area().m
            counter += 1
            latent_counter += 1
        for v in self.street_canyon.vegetation:
            B[0, counter] = h[counter] * v.get_area().m
            B[1, latent_counter + latent_offset] = h[counter] * v.get_area().m
            counter += 1
            latent_counter += 1
        for wh in self.street_canyon.waste_heat_sources_to_street_canyon:
            B[0, counter] = 1
            B[1, latent_counter + latent_offset] = dry_air_spec_heat_press.m / water_heat_vaporization.m
            counter += 1
            latent_counter += 1
        for t in self.street_canyon.traffic:
            B[0, counter] = 1
            B[1, latent_counter + latent_offset] = dry_air_spec_heat_press.m / water_heat_vaporization.m
            counter += 1
            latent_counter += 1
        return B / (self.street_canyon.get_volume().m * dry_air_density_stp.m * dry_air_spec_heat_press.m)

    def get_state_outputs(self, h, start_date, end_date, dt):
        """
        :param h: vector of convective heat transfer coefficients.
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        :return: state variables
        """
        A = self.get_state_matrix(h)
        B = self.get_input_matrix(h)
        U = np.transpose(self.get_input_vectors(start_date, end_date, dt))
        C = np.identity(2)
        D = np.zeros(shape=B.shape)
        sys = sig.StateSpace(A, B, C, D)
        sys_d = sys.to_discrete(dt=dt.seconds, method='backward_diff')
        x0 = np.asarray([25.0, 0.01])
        t, Y, X = sig.dlsim(sys_d, u=U, x0=x0)
        Y = np.transpose(Y)
        return Y

    def train(self, start_date, end_date, dt):
        """
        Train the data driven urban canopy model
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        n_surrounding_walls = len(self.street_canyon.surrounding_walls)
        n_pavements = len(self.street_canyon.pavements)
        n_vegetation = len(self.street_canyon.vegetation)
        N = n_surrounding_walls + n_pavements + n_vegetation + 1
        lb = np.zeros(N)
        ub = np.ones(N) * 500
        if self.previous_chtcs is None:
            self.previous_chtcs = np.random.rand(N) * 500
        pool = multiprocessing.Pool(self.n_processes)
        runner = StarmapParallelization(pool.starmap)
        problem = self.MultiObjectiveProblem(n_var=N, n_obj=2, lb=lb, ub=ub, umm=self.copy(), start_date=start_date,
                                             end_date=end_date, dt=dt, elementwise_runner=runner)
        algorithm = NSGA2(pop_size=40, n_offsprings=10, sampling=FloatRandomSampling(),
                          crossover=SBX(prob=0.9, eta=15), mutation=PM(eta=20),
                          eliminate_duplicates=True)
        termination = get_termination("n_gen", 40)
        results = minimize(problem, algorithm, termination, seed=1, save_history=True, verbose=True)
        self.current_chtcs = results.X[np.argmin(results.F[:, 0]), :]
        if self.get_previous_error_temperature(start_date, end_date, dt) < self.get_current_error_temperature(start_date, end_date, dt):
            Y = self.get_state_outputs(self.previous_chtcs, start_date, end_date, dt)
        else:
            Y = self.get_state_outputs(self.current_chtcs, start_date, end_date, dt)
        self.street_canyon.temperature = pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=Y[0, :])
        self.street_canyon.humidity = pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=Y[1, :])


    def test(self, start_date, end_date, dt):
        """
        Test the data driven urban canopy model
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        Y = self.get_state_outputs(self.current_chtcs, start_date, end_date, dt)
        if self.street_canyon.temperature is not None:
            self.street_canyon.temperature = pd.concat([self.street_canyon.temperature, pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=Y[0, :])])
        else:
            self.street_canyon.temperature = pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=Y[0, :])
        if self.street_canyon.humidity is not None:
            self.street_canyon.humidity = pd.concat([self.street_canyon.humidity, pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=Y[1, :])])
        else:
            self.street_canyon.humidity = pd.Series(index=pd.date_range(start=start_date, end=end_date, freq=dt), data=Y[1, :])

    def get_previous_error_temperature(self, start_date, end_date, dt):
        """
        Previous error made on temperature
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        Y = self.get_state_outputs(self.previous_chtcs, start_date, end_date, dt)
        return math.sqrt(mean_squared_error(Y[0, :], self.measured_outdoor_air_temperature[start_date:end_date].resample(dt).interpolate().values))

    def get_current_error_temperature(self, start_date, end_date, dt):
        """
        Current error made on temperature
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        Y = self.get_state_outputs(self.current_chtcs, start_date, end_date, dt)
        return math.sqrt(mean_squared_error(Y[0, :], self.measured_outdoor_air_temperature[start_date:end_date].resample(dt).interpolate().values))

    def get_previous_error_humidity(self, start_date, end_date, dt):
        """
        Previous error made on humidity
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        Y = self.get_state_outputs(self.previous_chtcs, start_date, end_date, dt)
        return math.sqrt(mean_squared_error(Y[1, :], self.measured_outdoor_air_humidity[start_date:end_date].resample(dt).interpolate().values)) * 1e3

    def get_current_error_humidity(self, start_date, end_date, dt):
        """
        Current error made on humidity
        :param start_date: date to start simulation
        :param end_date: date to end simulation
        :param dt: timestamp of simulation
        """
        Y = self.get_state_outputs(self.current_chtcs, start_date, end_date, dt)
        return math.sqrt(mean_squared_error(Y[1, :], self.measured_outdoor_air_humidity[start_date:end_date].resample(dt).interpolate().values)) * 1e3

    def update_previous_solution(self):
        """
        Update previous solution found by the data driven model
        """
        self.previous_chtcs = self.current_chtcs

    def get_solution(self):
        """
        :return: dictionary showing information about solution found by the data driven UCM
        """
        return {'CHTCs': self.current_chtcs}

    def copy(self):
        """
        Copy of the linear state space urban microclimate model
        :return: copy of the linear state space urban microclimate model
        """
        instance = LinearStateSpaceUrbanCanopyModel(self.street_canyon_loader)
        instance.pool_bems = []
        instance.street_canyon_loader = None
        instance.street_canyon = self.street_canyon
        instance.measured_outdoor_air_temperature = self.measured_outdoor_air_temperature
        instance.measured_outdoor_air_humidity = self.measured_outdoor_air_humidity
        return instance

    class MultiObjectiveProblem(ElementwiseProblem):
        """
        Class stating the multi objective problem we would like to optimise to find convective heat transfer coefficients.

        Attributes:
            umm: the linear state space urban microclimate model to optimize
            start_date: date to start simulation
            end_date: date to end simulation
            dt: timestamp of simulation
        """

        def __init__(self, n_var, n_obj, lb, ub, umm, start_date, end_date, dt, elementwise_runner):
            """
            :param n_var: number of variables to optimize
            :param n_obj: number of objectives to optimize
            :param lb: lower bounds of each variable
            :param ub: upper bounds of each variable
            :param umm: urban microclimate to optimize
            :param start_date: date to start simulation
            :param end_date: date to end simulation
            :param dt: timestamp of simulation
            """
            ElementwiseProblem.__init__(self, n_var=n_var, n_obj=n_obj, xl=lb, xu=ub, elementwise_runner=elementwise_runner)
            self.umm = umm
            self.start_date = start_date
            self.end_date = end_date
            self.dt = dt

        def _evaluate(self, x, out, *args, **kwargs):
            """
            :param x: list of heat transfer coefficients to optimize
            :param out: objectives to optimize
            """
            Y = self.umm.get_state_outputs(x, self.start_date, self.end_date, self.dt)
            out["F"] = [math.sqrt(mean_squared_error(Y[0, :], self.umm.measured_outdoor_air_temperature[self.start_date:self.end_date].resample(self.dt).interpolate().values)),
                        math.sqrt(mean_squared_error(Y[1, :], self.umm.measured_outdoor_air_humidity[self.start_date:self.end_date].resample(self.dt).interpolate().values)) * 1e3]




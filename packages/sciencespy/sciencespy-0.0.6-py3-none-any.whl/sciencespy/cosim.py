"""
Module to perform co-simulations between building energy models and urban microclimate models.

Delft University of Technology
Dr. Miguel Martin
"""
from abc import ABCMeta, abstractmethod
import configparser
import parseidf
from datetime import datetime, timedelta
import shutil
import re
import os
import math
import numpy as np
from metpy.units import units
from metpy.calc import relative_humidity_from_specific_humidity
from pathlib import Path
from sklearn.metrics import mean_squared_error
import pickle
import platform

from sciencespy.bem import *
from sciencespy.umm import *
from sciencespy.utils import *

class MementoBuilding():
    """
    Class used to save the internal state of a building to be compared for convergence analysis during co-simulations.

    Attributes:
        building_name: name of the building whose state is saved in the memento
        average_sensible_cooling_load: average sensible cooling load of the building
        average_latent_cooling_load: average sensible cooling load of the building
    """

    def __init__(self, building_name, average_sensible_cooling_load, average_latent_cooling_load):
        self.building_name = building_name
        self.average_sensible_cooling_load = average_sensible_cooling_load
        self.average_latent_cooling_load = average_latent_cooling_load

class OriginatorBuilding():
    """
    Class representing the originator of building to save its state in as a memento

    Attributes:
        building: building being managed by the originator
    """

    def __init__(self, building):
        """
        :param building: building being managed by the originator
        """
        self.building = building

    def save_to_memento(self):
        """
        Save the internal state of the building into a memento
        """
        return MementoBuilding(self.building.name,
                               self.building.get_sensible_cooling_load(),
                               self.building.get_latent_cooling_load())

class ManagerMementos():
    """
    Class to manage a list of mementos for different objects that can be saved during co-simulation.

    Attributes:
        building_mementos: list of mementos for buildings being simulated
    """

    def __init__(self):
        self.building_mementos = []

    def add_building_memento(self, bulding_memento):
        """
        Add a building memento
        :param bulding_memento: building memento to be added
        """
        self.building_mementos.append(bulding_memento)

    def get_building_memento(self, building_name):
        """
        Get a building memento saved in the manager.
        :param building_name: name of the building
        :return: memento corresponding to the building
        """
        for m in self.building_mementos:
            if m.building_name == building_name:
                return m

    def is_empty(self):
        """
        Check if the manager of memento is empty
        """
        return (self.building_mementos == [])
    def clearall(self):
        """
        Clear all the mementos
        """
        self.building_mementos = []

class ManagerOriginators():
    """
    Class to manage orginators of objects being processed during co-simulations.

    Attribute:
        manager_mementos: manager of mementos
        building_originators: list of building originators
    """

    def __init__(self, manager_mementos):
        """
        :param manager_mementos: manager of mementos
        """
        self.manager_mementos = manager_mementos
        self.building_originators = []

    def add_building_originator(self, building_originator):
        """
        Add building originator
        :param building_originator: building originator to be added.
        """
        self.building_originators.append(building_originator)

    def save_originators_to_mementos(self):
        """
        Save all originators in the manage of mementos
        """
        for bo in self.building_originators:
            self.manager_mementos.add_building_memento(bo.save_to_memento())

class CosimulationEngine():
    """
    Class representing the co-simulation engine between building energy models and urban microclimate models.

    Attributes:
        cfg_file: file containing configuration of the cosimulation engine
        max_iter: maximum number of iterations to achieve convergence
        bems: list of building energy models
        umms: list of urban microclimate models
        start_date: starting date of cosimulation
        end_date: ending date of cosimulation
        timestep: time resolution of cosimulation (in seconds)
        manager_originators: manager of originators of objects being processed during co-simulations
        manager_mementos: manager of mementos of objects being processed during co-simulations
        current_iteration: current iteration of the coupling
    """

    __metaclass__ = ABCMeta

    def __init__(self, cfg_file, max_iter = 100):
        self.cfg_file = cfg_file
        self.max_iter = max_iter
        self.bems = []
        self.umms = []
        self.start_date = None
        self.end_date = None
        self.timestep = None
        self.manager_mementos = ManagerMementos()
        self.manager_originators = ManagerOriginators(self.manager_mementos)
        self.current_iteration = 0

    def cosimulate(self):
        """
        Co-simulate building energy models and urban microclimate models
        """
        self.configure_cosimulation_engine()
        self.start_date = self.get_start_date()
        self.end_date = self.get_end_date()
        self.timestep = self.get_timestep()
        if len(self.bems) == 0:
            self.bems = self.load_bems()
        if len(self.umms) == 0:
            self.umms = self.load_umms()
        self.run_coupled_scheme()
        self.current_iteration = 1
        while not self.is_convergence_achieved() and self.current_iteration < self.max_iter:
            self.run_coupled_scheme()
            self.current_iteration += 1
        self.report_outputs()

    @abstractmethod
    def configure_cosimulation_engine(self):
        """
        Configure the cosimulation engine.
        """
        pass

    @abstractmethod
    def get_start_date(self):
        """
        :return: starting date of cosimulation
        """
        pass

    @abstractmethod
    def get_end_date(self):
        """
        :return: ending date of cosimulation
        """
        pass

    @abstractmethod
    def get_timestep(self):
        """
        :return: time resolution of cosimulation (in seconds)
        """
        pass

    @abstractmethod
    def load_bems(self):
        """
        Load the list of building energy models.
        """
        pass

    @abstractmethod
    def load_umms(self):
        """
        Load the list of urban microclimate models.
        """
        pass

    @abstractmethod
    def is_convergence_achieved(self):
        """
        Check if convergence of cosimulation is achieved.
        """
        pass

    @abstractmethod
    def run_coupled_scheme(self):
        """
        Run one iteration of the coupled scheme.
        """
        pass

    @abstractmethod
    def report_outputs(self):
        """
        Report outputs of the cosimulation.
        """
        pass


class CosimulationEnergyPlusDataDriven(CosimulationEngine):
    """
    Class representing the co-simulation engine between EnergyPlus models and data driven urban canopy models.

    Attributes:
        cfg_file: file containing configuration of the cosimulation engine
        max_iter: maximum number of iterations to achieve convergence
        bems: list of building energy models
        umms: list of urban microclimate models
        start_date: starting date of cosimulation
        end_date: ending date of cosimulation
        timestep: time resolution of cosimulation (in seconds)
        manager_originators: manager of originators of objects being processed during co-simulations
        manager_mementos: manager of mementos of objects being processed during co-simulations
        current_iteration: current iteration of the coupling
        neighborhood_file: file containing information of the neighborhood to be considered for cosimulation
        weather_file: file containing original weather conditions as collected from a rural station.
        ddm: data driven model to be connected to EnergyPlus
        training_split_ratio: ratio between the size of the training set and the total data set over the period of simulation.
        bems_dir: directory in which building energy models are stored
        weather_stations_dir: directory in which data collected by weather stations are stored
        lst_dir: directory in which data of the land surface temperature are stored
        climate_model_dir: directory in which data generated by the climate model are stored
        building_energy_dir: directory in which files resulting from building energy simulations are stored
        idf_objects: IDF objects containing information about the neighborhood to be cosimulated
        sensible_cooling_load_tolerance: tolerance for the average sensible cooling load to achieve convergence
        latent_cooling_load_tolerance: tolerance for the average sensible cooling load to achieve convergence
        error_function: method used to determine whether convergence is achieved by the coupled scheme.
        n_processes: number of processes to speed up the training phase if it can be parallelized.
    """

    __metaclass__ = ABCMeta

    def __init__(self, cfg_file, neighborhood_file, weather_file, max_iter = 100, ddm = 'dummy', training_split_ratio = 0.0,
                 error_function = RootMeanSquareError(), n_processes=2):
        CosimulationEngine.__init__(self, cfg_file, max_iter)
        self.neighborhood_file = neighborhood_file
        self.weather_file = weather_file
        self.ddm = ddm
        self.training_split_ratio = training_split_ratio
        self.iteration_table = []
        self.error_function = error_function
        self.n_processes = n_processes

    def configure_cosimulation_engine(self):
        """
        Configure the cosimulation engine.
        """
        config = configparser.ConfigParser()
        config.read(self.cfg_file)
        self.bems_dir = config['DATASTORAGE']['BEMS_DIR']
        self.weather_stations_dir = config['DATASTORAGE']['WEATHER_STATIONS_DIR']
        self.lst_dir = config['DATASTORAGE']['LST_DIR']
        self.climate_model_dir = config['DATASTORAGE']['CLIMATE_MODEL_DIR']
        self.building_energy_sim_dir = config['SIMULATIONSTORAGE']['BUILDING_ENERGY_SIM_DIR']
        self.simulation_output_dir = config['SIMULATIONSTORAGE']['SIM_OUTPUT_DIR']
        with open(self.neighborhood_file, 'r') as f:
            self.idf_objects = parseidf.parse(f.read())
        self.sensible_cooling_load_tolerance = float(self.idf_objects['CONVERGENCE'][0][1])
        self.latent_cooling_load_tolerance = float(self.idf_objects['CONVERGENCE'][0][2])

    def get_start_date(self):
        """
        :return: starting date of cosimulation
        """
        return datetime(int(self.idf_objects['RUNPERIOD'][0][3]),
                        int(self.idf_objects['RUNPERIOD'][0][1]),
                        int(self.idf_objects['RUNPERIOD'][0][2]), 1, 0, 0)

    def get_end_date(self):
        """
        :return: ending date of cosimulation
        """
        return datetime(int(self.idf_objects['RUNPERIOD'][0][6]),
                        int(self.idf_objects['RUNPERIOD'][0][4]),
                        int(self.idf_objects['RUNPERIOD'][0][5]), 0, 0, 0)

    def get_timestep(self):
        """
        :return: time resolution of cosimulation (in seconds)
        """
        return timedelta(seconds = int(3600.0 / float(self.idf_objects['RUNPERIOD'][0][7])))

    def load_bems(self):
        """
        Load the list of building energy models.
        """
        n_buildings = len(self.idf_objects['BUILDING'])
        bems = []
        for n in range(n_buildings):
            building_name = self.idf_objects['BUILDING'][n][1]
            x = float(self.idf_objects['BUILDING'][n][2])
            y = float(self.idf_objects['BUILDING'][n][3])
            if platform.system() == 'Windows':
                bem = EnergyPlusModel(IDFBuildingLoader(self.bems_dir + '\\' + building_name + '.idf', x=x, y=y))
            elif platform.system() == 'Linux':
                bem = EnergyPlusModel(IDFBuildingLoader(self.bems_dir + '/' + building_name + '.idf', x=x, y=y))
            bem.building = bem.building_loader.load()
            bems.append(bem)
        return bems

    def load_umms(self):
        """
        Load the list of urban microclimate models.
        """
        n_street_canyons = len(self.idf_objects['STREETCANYON'])
        umms = []
        for n in range(n_street_canyons):
            street_canyon_name = self.idf_objects['STREETCANYON'][n][1]
            surrounding_building_names = []
            m_surrounding_walls_group = len(self.idf_objects['SURROUNDINGWALLS'])
            for m in range(m_surrounding_walls_group):
                if self.idf_objects['SURROUNDINGWALLS'][m][1] == self.idf_objects['STREETCANYON'][n][3]:
                    r_surrounding_walls_attached_street_canyon = len(self.idf_objects['SURROUNDINGWALLS'][m]) - 2
                    for r in range(r_surrounding_walls_attached_street_canyon):
                        q_surrounding_walls = len(self.idf_objects['SURROUNDINGWALLS:BUILDING'])
                        for q in range(q_surrounding_walls):
                            if self.idf_objects['SURROUNDINGWALLS:BUILDING'][q][1] == self.idf_objects['SURROUNDINGWALLS'][m][r + 2]:
                                surrounding_building_names.append(self.idf_objects['SURROUNDINGWALLS:BUILDING'][q][2])
            bems_pool = EnergyPlusSimulationPool(EPWDataLoader(self.weather_file, year=self.start_date.year), output_dir=self.building_energy_sim_dir)
            for sbn in surrounding_building_names:
                for bem in self.bems:
                    if bem.building.name == sbn:
                        bems_pool.pool.append(bem)
            bems_pool.run()
            for bem in bems_pool.pool:
                self.manager_originators.add_building_originator(OriginatorBuilding(bem.building))
            street_canyon_loader = IDFStreetCanyonLoader(street_canyon_name,
                                                         self.neighborhood_file,
                                                         bems_pool,
                                                         atmosphere_dir=self.climate_model_dir,
                                                         pavement_temperature_dir=self.lst_dir,
                                                         weather_data_dir=self.weather_stations_dir)
            if self.ddm == 'lss':
                umm = None
                if self.training_split_ratio > 0.0:
                    umm = LinearStateSpaceUrbanCanopyModel(street_canyon_loader, training_split_ratio=self.training_split_ratio, n_processes=self.n_processes)
                else:
                    umm = LinearStateSpaceUrbanCanopyModel(street_canyon_loader, n_processes=self.n_processes)
                    if platform.system() == 'Windows':
                        with open(self.simulation_output_dir + '\\' + street_canyon_name + '_solution.pkl', 'rb') as fp:
                            solution_dictionary = pickle.load(fp)
                    elif platform.system() == 'Linux':
                        with open(self.simulation_output_dir + '/' + street_canyon_name + '_solution.pkl', 'rb') as fp:
                            solution_dictionary = pickle.load(fp)
                    umm.current_chtcs = solution_dictionary['CHTCs']
                umms.append(umm)
            else:
                umms.append(DummyDataDrivenUrbanCanopyModel(street_canyon_loader, training_split_ratio=self.training_split_ratio))

        return umms

    def is_convergence_achieved(self):
        """
        Check if convergence of cosimulation is achieved.
        """
        if self.manager_mementos.is_empty():
            return False
        else:
            errors_sensible_cooling_load = []
            errors_latent_cooling_load = []
            for umm in self.umms:
                for bem in umm.street_canyon_loader.bems_pool.pool:
                    building_name = bem.building.name
                    errors_sensible_cooling_load.append(self.error_function.err(bem.building.get_sensible_cooling_load().values,
                                                                  self.manager_mementos.get_building_memento(building_name).average_sensible_cooling_load.values))
                    errors_latent_cooling_load.append(self.error_function.err(bem.building.get_latent_cooling_load().values,
                                                                self.manager_mementos.get_building_memento(building_name).average_latent_cooling_load.values))
            mean_error_sensible_cooling_load = np.mean(errors_sensible_cooling_load)
            mean_error_latent_cooling_load = np.mean(errors_latent_cooling_load)
            print('--> Convergence sensible cooling load: ' + str(mean_error_sensible_cooling_load))
            print('--> Convergence latent cooling load: ' + str(mean_error_latent_cooling_load))
            self.iteration_table.append([self.current_iteration, mean_error_sensible_cooling_load, mean_error_latent_cooling_load])
            return (mean_error_sensible_cooling_load < self.sensible_cooling_load_tolerance) and \
                   (mean_error_latent_cooling_load < self.latent_cooling_load_tolerance)


    def report_outputs(self):
        """
        Report outputs of the cosimulation.
        """
        frame = {}
        building_names = []
        for umm in self.umms:
            frame[umm.street_canyon.name + ': Outdoor air temperature'] = umm.street_canyon.temperature.resample(self.timestep).mean().interpolate()[self.start_date:self.end_date]
            frame[umm.street_canyon.name + ': Outdoor air humidity'] = umm.street_canyon.humidity.resample(self.timestep).mean().interpolate()[self.start_date:self.end_date]
            bems = umm.street_canyon_loader.bems_pool.pool
            for bem in bems:
                if bem.building.name not in building_names:
                    frame[bem.building.name + ': Sensible heat load'] = bem.building.get_sensible_cooling_load().resample(self.timestep).mean().interpolate()[self.start_date:self.end_date]
                    frame[bem.building.name + ': Latent heat load'] = bem.building.get_latent_cooling_load().resample(self.timestep).mean().interpolate()[self.start_date:self.end_date]
                    building_names.append(bem.building.name)
        dataframe = pd.DataFrame(frame)
        fn = Path(self.neighborhood_file).stem
        if platform.system() == 'Windows':
            dataframe.to_csv(self.simulation_output_dir + '\\' + fn + '_output.csv', index_label = 'Date/Time')
        elif platform.system() == 'Linux':
            dataframe.to_csv(self.simulation_output_dir + '/' + fn + '_output.csv', index_label='Date/Time')
        n_iter = [row[0] for row in self.iteration_table]
        data = [row[1:3] for row in self.iteration_table]
        dataframe = pd.DataFrame(data, columns=['mean_error_sensible_load', 'mean_error_latent_load'], index=n_iter)
        if platform.system() == 'Windows':
            dataframe.to_csv(self.simulation_output_dir + '\\' + fn + '_convergence.csv', index_label='n_iter')
        elif platform.system() == 'Linux':
            dataframe.to_csv(self.simulation_output_dir + '/' + fn + '_convergence.csv', index_label='n_iter')
        if self.training_split_ratio > 0.0:
            for umm in self.umms:
                solution_dictionary = umm.get_solution()
                if platform.system() == 'Windows':
                    with open(self.simulation_output_dir + '\\' + umm.street_canyon.name + '_solution.pkl', 'wb') as fp:
                        pickle.dump(solution_dictionary, fp)
                elif platform.system() == 'Linux':
                    with open(self.simulation_output_dir + '/' + umm.street_canyon.name + '_solution.pkl', 'wb') as fp:
                        pickle.dump(solution_dictionary, fp)


class ExclusiveCosimulationEnergyPlusDataDriven(CosimulationEnergyPlusDataDriven):
    """
    Class representing the exclusive co-simulation engine between EnergyPlus models and data driven urban canopy models.

    Attributes:
        cfg_file: file containing configuration of the cosimulation engine
        bems: list of building energy models
        umms: list of urban microclimate models
        start_date: starting date of cosimulation
        end_date: ending date of cosimulation
        timestep: time resolution of cosimulation (in seconds)
        manager_originators: manager of originators of objects being processed during co-simulations
        manager_mementos: manager of mementos of objects being processed during co-simulations
        neighborhood_file: file containing information of the neighborhood to be considered for cosimulation
        weather_file: file containing original weather conditions as collected from a rural station
        training_split_ratio: ratio between the size of the training set and the total data set over the period of simulation.
        bems_dir: directory in which building energy models are stored
        weather_stations_dir: directory in which data collected by weather stations are stored
        lst_dir: directory in which data of the land surface temperature are stored
        climate_model_dir: directory in which data generated by the climate model are stored
        local_climate_dir: directory in which predictions of the local climate are stored
        building_energy_dir: directory in which files resulting from building energy simulations are stored
        idf_objects: IDF objects containing information about the neighborhood to be cosimulated
        sensible_cooling_load_tolerance: tolerance for the average sensible cooling load to achieve convergence
        latent_cooling_load_tolerance: tolerance for the average sensible cooling load to achieve convergence
        error_function: method used to determine whether convergence is achieved by the coupled scheme.
        n_processes: number of processes to speed up the training phase if it can be parallelized.
    """

    def __init__(self, cfg_file, neighborhood_file, weather_file, max_iter = 100, ddm = 'dummy', training_split_ratio = 0.0, error_function = RootMeanSquareError(), n_processes = 2):
        CosimulationEnergyPlusDataDriven.__init__(self, cfg_file, neighborhood_file, weather_file, max_iter, ddm, training_split_ratio, error_function, n_processes)

    def run_coupled_scheme(self):
        """
        Run one iteration of the coupled scheme.
        """
        self.manager_mementos.clearall()
        self.manager_originators.save_originators_to_mementos()
        for umm in self.umms:
            umm.run(self.start_date, self.end_date, self.timestep)
            local_climate_timestamps = umm.street_canyon_loader.bems_pool.weather_data.timestamps
            dt = local_climate_timestamps[1] - local_climate_timestamps[0]
            period = pd.date_range(start=self.start_date, end=self.end_date, freq=dt)
            index_period = np.where(local_climate_timestamps.isin(period))[0]
            local_climate_outdoor_air_temperature = umm.street_canyon_loader.bems_pool.weather_data.outdoor_air_temperature
            local_climate_outdoor_air_relative_humidity = umm.street_canyon_loader.bems_pool.weather_data.outdoor_air_relative_humidity
            local_climate_outdoor_air_pressure = umm.street_canyon_loader.bems_pool.weather_data.outdoor_air_pressure
            predicted_outdoor_air_temperature = umm.street_canyon.temperature.resample(dt).mean().interpolate()
            predicted_outdoor_air_specific_humidity = umm.street_canyon.humidity.resample(dt).mean().interpolate()
            predicted_outdoor_air_pressure = local_climate_outdoor_air_pressure[index_period]
            local_climate_outdoor_air_temperature[index_period] = predicted_outdoor_air_temperature.values * units.degC
            predicted_outdoor_air_relative_humidity = relative_humidity_from_specific_humidity(
                                                            predicted_outdoor_air_pressure,
                                                            predicted_outdoor_air_temperature.values * units.degC,
                                                            predicted_outdoor_air_specific_humidity.values).to('percent')
            local_climate_outdoor_air_relative_humidity[index_period] = predicted_outdoor_air_relative_humidity
            umm.street_canyon_loader.bems_pool.weather_data.set_outdoor_air_temperature(local_climate_outdoor_air_temperature)
            umm.street_canyon_loader.bems_pool.weather_data.set_outdoor_air_relative_humidity(local_climate_outdoor_air_relative_humidity)
            is_bems_simulation_over = False
            while not is_bems_simulation_over:
                try:
                    umm.street_canyon_loader.bems_pool.run()
                    is_bems_simulation_over = True
                except PermissionError:
                    pass







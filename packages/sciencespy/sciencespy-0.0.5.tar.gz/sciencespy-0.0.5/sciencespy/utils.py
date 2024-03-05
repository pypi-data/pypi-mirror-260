"""
Module dedicated to utility functions and classes that are transversal to the SCIENCES library.

Delft University of Technology
Dr. Miguel Martin
"""

from abc import ABCMeta, abstractmethod

import numpy as np
from sklearn.metrics import root_mean_squared_error

class ErrorFunction():
    """
    Class with which the error between two numerical vectors can be calculated.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_name(self):
        """
        :return: name of the error function.
        """
        pass

    @abstractmethod
    def err(self, vec1, vec2):
        """
        :param vec1: first numerical vector.
        :param vec2: second numerical vector.
        :return: error between two numerical vectors.
        """
        pass

class RootMeanSquareError(ErrorFunction):

    def get_name(self):
        """
        :return: name of the error function.
        """
        return 'RMSE'

    def err(self, vec1, vec2):
        """
        :param vec1: first numerical vector.
        :param vec2: second numerical vector.
        :return: error between two numerical vectors.
        """
        return root_mean_squared_error(vec1, vec2)

class CoefficientOfVariationOfRootMeanSquareError(RootMeanSquareError):

    def get_name(self):
        """
        :return: name of the error function.
        """
        return 'CV' + RootMeanSquareError.get_name(self)

    def err(self, vec1, vec2):
        """
        :param vec1: first numerical vector.
        :param vec2: second numerical vector.
        :return: error between two numerical vectors.
        """
        RMSE = RootMeanSquareError.err(self, vec1, vec2)
        return 100 * (RMSE / np.mean(vec2))

class NormalizeMeanBiasError(ErrorFunction):

    def get_name(self):
        """
        :return: name of the error function.
        """
        return "NMBE"

    def err(self, vec1, vec2):
        """
        :param vec1: first numerical vector.
        :param vec2: second numerical vector.
        :return: error between two numerical vectors.
        """
        return 100 * (np.mean(vec1) - np.mean(vec2)) / np.mean(vec2)
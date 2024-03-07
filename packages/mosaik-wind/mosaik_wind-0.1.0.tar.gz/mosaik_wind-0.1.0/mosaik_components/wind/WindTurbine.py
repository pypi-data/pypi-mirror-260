"""
@author: original from Fernando Penaherrera and modified by Christoph Stucke and Malte Trauernicht

"""
import pandas as pd
import numpy as np


class WindTurbine(object):
    """
    Model of a simple wind turbine with a given power curve.
    This data is for a low wind speed turbine which peaks at 6m/s
    """

    def __init__(self, max_power=0.1, path=''):
        """
        Constructor
        """
        self.max_power = max_power
        self.num_of_entries = 0
        self.data_path = path
        self._power_curve_data = self.get_power_curve()

    def get_power_curve(self):
        """
        Get the data for the shape of the power curve.
        Normalizes the info and escalates to the rated power.
        """
        power_curve_data = pd.read_csv(self.data_path)
        self.num_of_entries = len(power_curve_data)
        max_rated_power = power_curve_data["power_factor"].max()
        power_curve_data["power"] = power_curve_data["power_factor"] / max_rated_power * self.max_power
        return power_curve_data

    def power_out(self, wind_speed):
        """
        Simple interpolation function to calculate the instant power @ wind_speed
        """
        x = self._power_curve_data["wind_speed"]
        y = self._power_curve_data["power"]
        y_new = np.interp(wind_speed, x, y)
        return y_new

    def __repr__(self):
        """
        Print the turbine properties
        """
        a = "Wind turbine" + "\n"
        b = "Max Power: {} MW".format(self.max_power) + "\n"
        return a + b

    def get_num_of_entries(self):
        return self.num_of_entries


if __name__ == '__main__':
    wt = WindTurbine(max_power=0.15)
    for i in range(0, 40):
        print(i, wt.power_out(i))

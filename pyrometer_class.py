"""
Module for managing operations of a Micro Epsilon Infrared Pyrometer.

This module contains the `PyrometerObject` class which encapsulates various
pyrometer operations including temperature readings, managing rangefinder laser control,
and tracking the running average and maximum temperature.
"""

from threading import Thread
from time import time, sleep
from serial_class import serial_channels
from logmanager import logger
from app_control import settings


class PyrometerObject:
    """
    This class is responsible for managing and interacting with a pyrometer device, which is used
    to measure temperature and control a laser. It handles acquiring temperature data, maintaining
    a moving average for temperature readings, resetting temperature limits, and managing laser
    operations including a timeout mechanism for the laser.

    The primary purpose of this class is to facilitate data acquisition, analysis, and control
    mechanisms for the pyrometer system by utilizing predefined settings and external communication
    modules for device interaction. It simplifies pyrometer operations through its interface
    methods, ensuring accurate and efficient functioning in its operational environment.
    """
    def __init__(self):
        """
        Represents an entity for managing temperature and laser state attributes.

        This class is responsible for storing and managing temperature-related
        values and laser state information. It initializes its attributes based
        on predefined settings.
        """
        self._serial_channel = 'Pyrometer'
        self._average_temp = settings['pyro-min-temp']
        self._max_temp = settings['pyro-min-temp']
        self._average_max_temp = settings['pyro-min-temp']
        self._current_temp = settings['pyro-min-temp']
        self._temperature_sequence = [settings['pyro-min-temp']] * settings['pyro-running-average']
        self._laser_state = 0
        self._laser_max_time = settings['laser-maxtime']

    def temperature(self):
        """
        Gets the current temperature and pyrometer laser state from the serial
        channel's listener values.

        This method processes a list of pyrometer values to identify and retrieve
        the current temperature and laser state.

        :return: A tuple containing the current temperature and pyrometer laser
                 state as binary values.
        :rtype: tuple
        """
        pyro_values = serial_channels['pyrometer'].listener_values()
        current_temperature = 0
        current_laser_state = 0
        for value in pyro_values:
            if value['name'] == 'temperature':
                current_temperature  = value['binary']
            if value['name'] == 'pyrometer laser':
                current_laser_state = value['binary']
        return current_temperature, current_laser_state

    def update_moving_average(self):
        """
        Updates the running average temperature and maintains tracking of the maximum average
        temperature observed. The function adjusts the list of temperature readings depending
        on the current temperature value and predetermined settings. It also calculates a new
        average temperature from the updated list and compares it with the maximum average
        temperature recorded so far.
        """
        if self.value <= settings['pyro-min-temp']:
            self._temperature_sequence = [settings['pyro-min-temp']] * settings['pyro-running-average']
        elif self.value > (self._average_temp + 20):  # speed up getting to average while sample is heating
            self._temperature_sequence = [self.value] * settings['pyro-running-average']
        else:
            self._temperature_sequence.append(self.value)
            self._temperature_sequence.pop(0)
        self._average_temp = int(sum(self._temperature_sequence) / len(self._temperature_sequence))
        self._average_max_temp = max(self._average_temp, self._average_max_temp)

    def reset_max(self, item, command):
        """
        Resets the maximum and average maximum temperature to a predefined minimum value and updates
        the temperature.

        :return: The current temperature of the PyroClass after resetting maximum values
        :rtype: Any
        """
        logger.info('PyroClass max temp reset')
        self._max_temp = settings['pyro-min-temp']
        self._average_max_temp = settings['pyro-min-temp']
        return self.get_temperatures(item, command)

    def laser_on_off(self, item, command):
        """
        Controls the laser of the pyrometer by turning it on or off based on the
        provided command. When the laser is turned on, a timer thread is initiated
        to handle turning it off after a certain duration set in the settings file.
        """
        if command == 1:
            serial_channels['pyrometer'].api_command(item, 'pyrolaser-on')
            self._laser_state = 1
            logger.info('PyroClass Rangefinder laser is on')
            timerthread = Thread(target=self.laser_off_timer)
            timerthread.name = 'pyro-rangefinder-off-timer-thread'
            timerthread.start()
        else:
            serial_channels['pyrometer'].api_command(item, 'pyrolaser-off')
            self._laser_state = 0
            logger.info('PyroClass Rangefinder laser is off')
        return self.get_temperatures(item, command)

    def laser_off_timer(self):
        """
        Sets a timer to automatically turn off the laser after a specified maximum time is reached.

        This method checks if the laser is currently on. If the laser is on, it calculates
        a future time based on the current time and the maximum allowed time. The laser
        will then be turned off after the calculated duration has passed.
        """
        off_time = time() + self._laser_max_time
        while self._laser_state == 1:
            if time() > off_time:
                self.laser_on_off('autolaseroff', 0)
                logger.info('PyroClass Rangefinder laser has been turned off due to timeout')
            sleep(1)

    def get_temperatures(self, item, command):
        """
        Retrieve temperature-related data.

        This function gathers various temperature readings and additional state data,
        returning them in a structured dictionary. The returned data includes information
        on current temperature, average temperature, maximum recorded temperature,
        average maximum recorded temperature, and the state of teh rangefinder laser on the pyrometer.
        """
        values = {'temperature': self._current_temp, 'averagetemp': self._average_temp, 'maxtemp': self._max_temp,
                  'averagemaxtemp': self._average_max_temp, 'pyrolaser': self._laser_state}
        return {'item': item, 'command': command, 'values': values}


pyrometer = PyrometerObject()

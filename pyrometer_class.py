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
        self._default_poll_interval = 5
        self._poll_interval =  self._default_poll_interval
        self._laser_max_time = settings['laser-maxtime']
        timerthread = Thread(target=self.pyrometer_updater)
        timerthread.name = 'pyro reader thread'
        timerthread.start()

    def pyrometer_updater(self):
        """
        Continuously updates pyrometer data and moving average based on a defined polling interval.
        """
        while True:
            sleep_counter = 0
            self.read_pyrometer_data()
            self.update_moving_average()
            while sleep_counter < self._poll_interval:
                sleep_counter += 1
                sleep(1)

    def read_pyrometer_data(self):
        """
        Calculates the temperature and laser state from the pyrometer data. The method processes
        the serial listener values associated with the pyrometer channel. It extracts and decodes
        the temperature and laser state values from the corresponding data entries and updates the class.
        """
        pyro_values = serial_channels['pyrometer'].listener_values()
        for value in pyro_values:
            if value['name'] == 'temperature':
                try:
                    binary_1 = value['value'].encode('iso-8859-1')
                    self._current_temp  = ((binary_1[0] * 256 + binary_1[1]) - 1000) / 10
                except IndexError:
                    self._current_temp = settings['pyro-min-temp']
            if value['name'] == 'pyrometer laser':
                try:
                    binary_1 = value['value'].encode('iso-8859-1')
                    self._laser_state = int(binary_1[0])
                except IndexError:
                    self._laser_state = 0

    def update_moving_average(self):
        """
        Updates the running average temperature and maintains tracking of the maximum average
        temperature observed. The function adjusts the list of temperature readings depending
        on the current temperature value and predetermined settings. It also calculates a new
        average temperature from the updated list and compares it with the maximum average
        temperature recorded so far.
        """
        self._max_temp = max(self._max_temp, self._current_temp)
        if self._current_temp  <= settings['pyro-min-temp']:
            self._temperature_sequence = [settings['pyro-min-temp']] * settings['pyro-running-average']
        elif self._current_temp  > (self._average_temp + 20):  # speed up getting to average while sample is heating
            self._temperature_sequence = [self._current_temp ] * settings['pyro-running-average']
        else:
            self._temperature_sequence.append(self._current_temp)
            self._temperature_sequence.pop(0)
        self._average_temp = float(sum(self._temperature_sequence) / len(self._temperature_sequence))
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
        average maximum recorded temperature, and the state of the rangefinder laser on the pyrometer.
        """
        values = {'temperature': self._current_temp, 'averagetemp': self._average_temp, 'maxtemp': self._max_temp,
                  'averagemaxtemp': self._average_max_temp, 'pyrolaser': self._laser_state}
        return {'item': item, 'command': command, 'values': values}

    def change_poll_interval(self, value):
        """
        Updates the poll interval to the specified value. Entering 0 returns to the default value
        """
        if value > 0:
            self._poll_interval = value
        else:
            self._poll_interval = self._default_poll_interval

pyrometer = PyrometerObject()

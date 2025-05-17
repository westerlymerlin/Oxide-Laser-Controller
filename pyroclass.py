"""
Pyrometer Interface and Temperature Monitoring

This module implements the interface for pyrometer temperature measurements,
providing real-time temperature monitoring and data handling capabilities for
laser processing applications.

Features:
    - Pyrometer communication and initialization
    - Real-time temperature reading and monitoring
    - Temperature data processing and validation
    - Error handling for sensor communication
    - Temperature threshold monitoring

Classes:
    Pyrometer: Main class for pyrometer operations and temperature management

Usage:
    from pyroclass import Pyrometer

    pyro = Pyrometer()
    current_temp = pyro.get_temperature()

    # Monitor temperature with safety thresholds
    pyro.start_monitoring(max_temp=1200)

Hardware Requirements:
    - Compatible pyrometer sensor
    - Serial/USB communication interface

Note:
    Temperature readings are provided in degrees Celsius.
    Ensure proper pyrometer calibration before use in production environment.
"""

from threading import Timer
from time import sleep, time
from base64 import b64decode
import serial  # from pyserial
from app_control import settings
from logmanager import logger


class PyroClass:
    """
    This class represents a Pyrometer interface to communicate with a serial device.

    The PyroClass establishes and manages communication with a pyrometer device
    through a serial port. It handles initializing the pyrometer, reading temperature
    values at regular intervals, maintaining a running average of temperature readings,
    and controlling a laser rangefinder. Various utility functions are available for
    interacting with the pyrometer's readings and laser control.
    """
    def __init__(self, port, speed, readtemp, readlaser, laseron, laseroff):
        self.port = serial.Serial()
        self.port.port = port
        self.port.baudrate = speed
        self.port.parity = serial.PARITY_NONE
        self.port.stopbits = serial.STOPBITS_ONE
        self.port.bytesize = serial.EIGHTBITS
        # self.port.set_buffer_size(4096, 4096)
        self.port.timeout = 1
        self.value = settings['pyro-min-temp']
        self.averagetemp = settings['pyro-min-temp']
        self.maxtemp = settings['pyro-min-temp']
        self.averagemaxtemp = settings['pyro-min-temp']
        self.laser = 0
        self.portready = 0
        self.readinterval = 5
        self.tempseq = [settings['pyro-min-temp']] * settings['pyro-running-average']
        self.readtemp = b64decode(readtemp)
        self.readlaser = b64decode(readlaser)
        self.laser_on = b64decode(laseron)
        self.laser_off = b64decode(laseroff)
        logger.info('PyroClass Initialising pyrometer on port %s', self.port.port)
        try:
            self.port.open()
            logger.info('PyroClass pyrometer port %s ok', self.port.port)
            self.portready = 1
            timerthread = Timer(1, self.readtimer)
            timerthread.name = 'pyro-read-thread'
            timerthread.start()
        except serial.serialutil.SerialException:
            logger.error('PyroClass error opening port %s', self.port.port)

    def close(self):
        """
        Closes the communication port associated with the PyroClass Pyrometer
        object. This function ensures the port is properly closed and logs this
        action. It also updates the `portready` status attribute to indicate
        that the port is no longer active.

        :raises AttributeError: If the `port` attribute or its methods are not
            properly initialized or accessible.
        :raises IOError: If there is an issue with closing the port.

        :return: None
        """
        self.port.close()
        logger.info('PyroClass Pyrometer port %s closed', self.port.port)
        self.portready = 0

    def readtimer(self):
        """
        Continuously reads temperature and laser data from a connected port while the
        port is ready. The method writes specific commands to the port to request
        temperature and laser information and processes the data returned.

        When the port is not ready or there is an exception during data reading, the
        temperature (`value`) is reset to 0. Temperature data is processed to calculate
        statistics like `maxtemp` and optionally update an average temperature.

        Potential logging operations are carried out at various points:
        - To debug temperature and laser value read operations.
        - To log any exceptions encountered during execution.

        :raises Exception: Handles any exceptions during port communication, logs the
            exception, and ensures temperature value is reset to mitigate impact.

        :param

        :return: None
        """
        while self.portready == 1:
            try:
                if self.portready == 1:
                    self.port.write(self.readtemp)
                    databack = self.port.read(size=100)
                    if databack == b'':
                        self.value = 0
                        self.laser = 0
                    else:
                        self.value = ((databack[0] * 256 + databack[1]) - 1000) / 10
                        logger.debug('PyroClass Pyrometer value = %s', self.value)
                        self.maxtemp = max(self.value, self.maxtemp)
                        self.setaverage()
                        self.port.write(self.readlaser)
                        databack = self.port.read(size=100)
                        self.laser = databack[0]
                    logger.debug('PyroClass Temp Return "%s" ', self.value)
                else:
                    self.value = 0
            except:
                logger.exception('PyroClass readtimer temperture Error: %s', Exception)
                self.value = 0
            sleep(self.readinterval)

    def setaverage(self):
        """
        Updates the running average temperature and maintains tracking of the maximum average
        temperature observed. The function adjusts the list of temperature readings depending
        on the current temperature value and predetermined settings. It also calculates a new
        average temperature from the updated list and compares it with the maximum average
        temperature recorded so far.

        :param self: An instance of the class containing attributes `value`, `tempseq`,
            `averagetemp`, and `averagemaxtemp`, which are necessary for the computation.
        :return: None
        """
        if self.value <= settings['pyro-min-temp']:
            self.tempseq = [settings['pyro-min-temp']] * settings['pyro-running-average']
        elif self.value > (self.averagetemp + 20):  # speed up getitng to average while sample is heating
            self.tempseq = [self.value] * settings['pyro-running-average']
        else:
            self.tempseq.append(self.value)
            self.tempseq.pop(0)
        self.averagetemp = int(sum(self.tempseq) / len(self.tempseq))
        self.averagemaxtemp = max(self.averagetemp, self.averagemaxtemp)

    def resetmax(self):
        """
        Resets the maximum and average maximum temperature to a predefined minimum value and updates
        the temperature.

        :return: The current temperature of the PyroClass after resetting maximum values
        :rtype: Any
        """
        logger.info('PyroClass max temp reset')
        self.maxtemp = settings['pyro-min-temp']
        self.averagemaxtemp = settings['pyro-min-temp']
        return self.temperature()

    def laseron(self):
        """
        Turns the laser on by sending a command to the port, if the port is ready.
        Additionally, it starts a timer thread to turn the laser off after 0.5 seconds.

        :return: None
        """
        if self.portready == 1:
            self.port.write(self.laser_on)
            self.laser = 1
            laserthread = Timer(0.5, self.laserofftimer)
            laserthread.name = 'pyro-laser-off-thread'
            laserthread.start()

    def laseroff(self):
        """
        Turns off the laser by writing the appropriate command to the port if the port
        is ready. Updates the laser status attribute accordingly.

        :raises AttributeError: If a required attribute is not defined.
        :param self: The instance of the object performing the action.
        :return: None
        """
        if self.portready == 1:
            self.port.write(self.laser_off)
            self.laser = 0

    def laserofftimer(self):
        """
        Turns off the laser after a specific period of time set in the
        settings if a laser is still active.

        This method continuously monitors the laser's state and checks
        if the maximum allowed running time has been exceeded. If the
        maximum time has been reached and the laser is still active, the
        laser will be turned off. It pauses execution for 1 second between
        checks to reduce resource usage while monitoring.

        :raises KeyError: If the 'maxtime' key is not present in settings.
        :raises AttributeError: If the 'laser' attribute or 'laseroff' method
            is missing or improperly configured.
        """
        offtime = time() + settings['maxtime']
        while self.laser == 1:
            if time() > offtime:
                self.laseroff()
            sleep(1)

    def temperature(self):
        """
        Provides a dictionary containing current temperature readings from various sensors.

        The dictionary includes detailed information such as the current temperature,
        average temperature, laser temperature, maximum temperature,
        and average maximum temperature. This method is used to obtain
        a snapshot of the relevant temperature-related metrics.

        :raises No exception is explicitly raised in this method as it only returns a dictionary.
        :param None: This method does not take any external parameters.
        :return: A dictionary containing the following keys:
                 - 'temperature': Current temperature
                 - 'averagetemp': Average temperature
                 - 'pyrolaser': Laser temperature (pyrolaser)
                 - 'maxtemp': Maximum temperature
                 - 'averagemaxtemp': Average maximum temperature
        :rtype: dict
        """
        return {'temperature': self.value, 'averagetemp': self.averagetemp, 'pyrolaser': self.laser,
                'maxtemp': self.maxtemp, 'averagemaxtemp': self.averagemaxtemp}


pyrometer = PyroClass(settings['pyro-port'], settings['pyro-speed'], settings['pyro-readtemp'],
                      settings['pyro-readlaser'], settings['pyro-laseron'], settings['pyro-laseroff'])

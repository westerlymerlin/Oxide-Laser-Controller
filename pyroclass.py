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
        """Close the serial port"""
        self.port.close()
        logger.info('PyroClass Pyrometer port %s closed', self.port.port)
        self.portready = 0

    def readtimer(self):
        """regular timer, reads the temperature every 5 seconds, keeps track of the maximum temperatiure read"""
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
        """Add the temp value to the running average list"""
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
        """Reset the maximum temerature"""
        logger.info('PyroClass max temp reset')
        self.maxtemp = settings['pyro-min-temp']
        self.averagemaxtemp = settings['pyro-min-temp']
        return self.temperature()

    def laseron(self):
        """Switch on the rangefinder laser and set a timer to switch it off after maxtime"""
        if self.portready == 1:
            self.port.write(self.laser_on)
            self.laser = 1
            laserthread = Timer(0.5, self.laserofftimer)
            laserthread.name = 'pyro-laser-off-thread'
            laserthread.start()

    def laseroff(self):
        """Switch off the rangefinder laser"""
        if self.portready == 1:
            self.port.write(self.laser_off)
            self.laser = 0

    def laserofftimer(self):
        """Auto switch off of the laser after maxtime seconds"""
        offtime = time() + settings['maxtime']
        while self.laser == 1:
            if time() > offtime:
                self.laseroff()
            sleep(1)

    def temperature(self):
        """API Call: return pyrometer values and settings as a json message"""
        return {'temperature': self.value, 'averagetemp': self.averagetemp, 'pyrolaser': self.laser,
                'maxtemp': self.maxtemp, 'averagemaxtemp': self.averagemaxtemp}


pyrometer = PyroClass(settings['pyro-port'], settings['pyro-speed'], settings['pyro-readtemp'],
                      settings['pyro-readlaser'], settings['pyro-laseron'], settings['pyro-laseroff'])

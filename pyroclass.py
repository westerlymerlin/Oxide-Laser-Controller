"""Pyro Class - controles the microepsilon pyrometer and rangefinder laser"""

from threading import Timer
from time import sleep, time
from base64 import b64decode
import serial  # from pyserial
from app_control import settings
from logmanager import logger


class PyroClass:
    """Pyrometer class, reads the temperature from the pyromers and controls the rangefinder laser"""
    def __init__(self, port, speed, readtemp, readlaser, laseron, laseroff):
        self.port = serial.Serial()
        self.port.port = port
        self.port.baudrate = speed
        self.port.parity = serial.PARITY_NONE
        self.port.stopbits = serial.STOPBITS_ONE
        self.port.bytesize = serial.EIGHTBITS
        # self.port.set_buffer_size(4096, 4096)
        self.port.timeout = 1
        self.value = 0
        self.laser = 0
        self.maxtemp = 0
        self.portready = 0
        self.readtemp = b64decode(readtemp)
        self.readlaser = b64decode(readlaser)
        self.laser_on = b64decode(laseron)
        self.laser_off = b64decode(laseroff)
        logger.info('Initialising pyrometer on port %s', self.port.port)
        try:
            self.port.open()
            logger.info('pyrometer port %s ok', self.port.port)
            self.portready = 1
            timerthread = Timer(1, self.readtimer)
            timerthread.name = 'pyro-read-thread'
            timerthread.start()
        except serial.serialutil.SerialException:
            logger.error('PyroClass error opening port %s', self.port.port)

    def close(self):
        """Close the serial port"""
        self.port.close()
        logger.info('Pyrometer port %s closed', self.port.port)
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
                        logger.debug('Pyrometer value = %s', self.value)
                        if self.value > self.maxtemp:
                            self.maxtemp = self.value
                            logger.info('Pyro readtimer: New Max Temp = %s', self.maxtemp)
                        self.port.write(self.readlaser)
                        databack = self.port.read(size=100)
                        self.laser = databack[0]
                    logger.debug('Temp Return "%s" ', self.value)
                else:
                    self.value = 0
            except:
                logger.exception('readtimer temperture Error: %s', Exception)
                self.value = 0
            sleep(5)

    def resetmax(self):
        """Reset the maximum temerature"""
        self.maxtemp = 0

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
        print(time(), offtime)
        while self.laser == 1:
            if time() > offtime:
                self.laseroff()
            sleep(1)



    def readmax(self):
        """Return maximum temperature read"""
        return self.maxtemp

    def read(self):
        """Return last temperature read"""
        return self.value

    def temperature(self):
        """API Call: return pyrometer values and settings as a json message"""
        return {'temperature': self.read(), 'laser': self.laser, 'maxtemp': self.readmax()}

    def httpstatus(self):
        """Return the temperature, rangerfik=nder laser and max temp, is called via the web page"""
        httpreturn = [['temperature', self.read()], ['rangerfinder laser', self.laser],
                      ['max temperature', self.readmax()]]
        return httpreturn

pyrometer = PyroClass(settings['pyro-port'], settings['pyro-speed'], settings['pyro-readtemp'],
                      settings['pyro-readlaser'], settings['pyro-laseron'], settings['pyro-laseroff'])

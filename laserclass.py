"""
Laser Class - manages the laser via  TTL signal and serial connections
"""
# pylint: disable=E1101
import os
from threading import Timer
from time import sleep
from base64 import b64decode
import serial  # from pyserial
from RPi import GPIO
from app_control import settings, writesettings
from logmanager import logger


class LaserClass:
    """LaserClass"""
    def __init__(self):
        self.frequency = settings['frequency']
        self.dutycycle = settings['power']
        self.laserstate = 0
        self.laserthread = 0
        self.maxtime = settings['maxtime']
        self.key_channel = 12
        self.door_channel = 16
        self.ttl_channel = 18
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.door_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Door Interlock
        GPIO.setup(self.key_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Key Switch
        GPIO.setup(self.ttl_channel, GPIO.OUT)
        self.pwm = GPIO.PWM(self.ttl_channel, settings['frequency'])
        logger.info('Laser Class initialised')

    def httpstatus(self):
        """Return the status (Firing), power and timeout values, is called via the web page"""
        if self.keyswitch():
            keyswitch = 'off'
        else:
            keyswitch = 'on'
        if self.doorinterlock():
            doorinterlock = 'open'
        else:
            doorinterlock = 'closed'
        httpreturn = [['Status', self.laserstate], ['Power (%)', settings['power']],
                      ['Auto off (s)', settings['maxtime']], ['Key Switch', keyswitch],
                      ['Door Interlock', doorinterlock]]
        return httpreturn

    def setpower(self, laserpower):
        """Set the laser power via the serial connection"""
        self.dutycycle = laserpower
        settings['power'] = laserpower
        writesettings()

    def setmaxtimeout(self, maxtime):
        """API call to set the maximum time that the laser can run"""
        self.maxtime = maxtime
        settings['maxtime'] = maxtime
        logger.info('Changing Laser Maximum on time to %s seconds', maxtime)
        writesettings()

    def keyswitch(self):
        """Check if the key switch is on (N/C contact)"""
        if GPIO.input(self.key_channel) == 1:
            return 1
        return 0

    def doorinterlock(self):
        """Check if the door interlock is engaged (N/O contact)"""
        if GPIO.input(self.door_channel) == 0:
            return 1
        return 0

    def alarmstatus(self):
        """Check if the key and door interlock is engaged"""
        if settings['testmode']:
            return 0
        return self.keyswitch() + self.doorinterlock()

    def laserstatus(self):
        """Return the laser (firning) status and the power setting"""
        return {'laser': self.laserstate, 'power': settings['power'], 'keyswitch': self.keyswitch(),
                'doorinterlock': self.doorinterlock()}

    def laser(self, state):
        """Switch on or off the laser, if laser is on then run a thread to switch off if max time is exceeded"""
        if state == 1:
            if self.alarmstatus() > 0:
                logger.warning('Laser was not switched on, key switch or door interlock was engaged')
                self.laserstate = 0
                return
            logger.info('Laser is on')
            self.pwm.start(self.dutycycle)
            self.laserstate = 1

            # Start a  timer for the laser, if the laser is not shutdown by PyMS then this timer will shut it down
            timerthread = Timer(settings['maxtime'], lambda: self.laser(2))
            timerthread.name = 'laser-off-timer-thread'
            timerthread.start()
        elif state == 2:
            logger.info('Laser Auto shut off')
            self.pwm.stop()
            self.laserstate = 0
        else:
            logger.info('Laser is off')
            self.laserstate = 0
            self.pwm.stop()




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
                        logger.info('Pyrometer value = %s', self.value)
                        self.maxtemp = max(self.maxtemp, self.value)
                        self.port.write(self.readlaser)
                        databack = self.port.read(size=100)
                        self.laser = databack[0]
                    logger.debug('Temp Return "%s" ', self.value)
                else:
                    self.value = 0
            except:
                logger.exception('Temperture Error: %s', Exception)
                self.value = 0
            sleep(5)

    def resetmax(self):
        """Reset the maximum temerature"""
        self.maxtemp = 0

    def laseron(self):
        """Switch on the rangefinder laser and set a timer to swiotch it off 60 seconds later"""
        if self.portready == 1:
            self.port.write(self.laser_on)
            databack = self.port.read(size=100)
            self.laser = 1
            laserthread = Timer(60, self.laseroff)
            laserthread.start()

    def laseroff(self):
        """Switch off the rangefinder laser"""
        if self.portready == 1:
            self.port.write(self.laser_off)
            databack = self.port.read(size=100)
            self.laser = 0

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


def parsecontrol(item, command):
    """Main API entrypoint, recieves an **item** and **command** parameter"""
    # print('%s : %s' % (item, command))
    try:
        if item == 'laser':
            if command == 'on':
                laser.laser(1)
                return laser.laserstatus()
            laser.laser(0)
            return laser.laserstatus()
        if item == 'setlaserpower':
            laser.setpower(command)
            return laser.laserstatus()
        if item == 'laseralarm':
            return laser.alarmstatus()
        if item == 'laserstatus':
            return laser.laserstatus()
        if item == 'setlasertimeout':
            laser.setmaxtimeout(command)
            return {'maxtime': settings['maxtime']}
        if item == 'restart':
            if command == 'pi':
                logger.warning('Restart command recieved: system will restart in 15 seconds')
                timerthread = Timer(15, reboot())
                timerthread.name = 'reboot-timer-thread'
                timerthread.start()
                return laser.laserstatus()
        return laser.laserstatus()
    except ValueError:
        logger.warning('incorrect json message')
        return laser.laserstatus()



def reboot():
    """API call to reboot the Raspberry Pi"""
    logger.warning('System is restarting now')
    os.system('sudo reboot')

logger.info("laser controller started")
pyrometer = PyroClass(settings['pyro-port'], settings['pyro-speed'], settings['pyro-readtemp'],
                      settings['pyro-readlaser'], settings['pyro-laseron'], settings['pyro-laseroff'])
laser = LaserClass()
logger.info("Laser controller ready")

"""
Laser Class - manages the laser via  TTL signal and serial connections
"""
# pylint: disable=E1101
import os
from time import sleep, time
from threading import Timer
from RPi import GPIO
from app_control import settings, writesettings, updatesetting
from pyroclass import pyrometer
from logmanager import logger
from camera import video_camera_instance_0


class LaserClass:
    """LaserClass"""
    def __init__(self):
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
        logger.info('LaserClass initialised')

    def setpower(self, laserpower):
        """Set the laser power via the serial connection"""
        self.dutycycle = laserpower
        settings['power'] = laserpower
        writesettings()

    def setmaxtimeout(self, maxtime):
        """API call to set the maximum time that the laser can run"""
        self.maxtime = maxtime
        settings['maxtime'] = maxtime
        logger.info('LaserClass Changing Laser Maximum on time to %s seconds', maxtime)
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
                'doorinterlock': self.doorinterlock(), 'autooff': self.maxtime}

    def laser(self, state):
        """Switch on or off the laser, if laser is on then run a thread to switch off if max time is exceeded"""
        if state == 1:
            if self.alarmstatus() > 0:
                logger.warning('LaserClass Laser was not switched on, key switch or door interlock was engaged')
                self.laserstate = 0
                return
            logger.info('LaserClass Switching laser on')
            pyrometer.readinterval = 1
            self.pwm.ChangeFrequency(settings['frequency'])
            self.pwm.start(self.dutycycle)
            self.laserstate = 1
            # Start a  timer for the laser, if the laser is not shutdown this timer will shut it down
            timerthread = Timer(0.5, self.laserofftimer)
            timerthread.name = 'laser-off-timer-thread'
            timerthread.start()
        else:
            pyrometer.readinterval = 5
            logger.info('LaserClass Laser is off')
            self.laserstate = 0
            self.pwm.stop()

    def laserofftimer(self):
        """Auto switch off of the laser after maxtime seconds"""
        offtime = time() + settings['maxtime']
        while self.laserstate == 1:
            if time() > offtime:
                self.laser(0)
            sleep(1)




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
        if item == 'gettemperature':
            return pyrometer.temperature()
        if item == 'resetmax':
            return pyrometer.resetmax()
        if item == 'pyrolaser':
            if command == 'on':
                pyrometer.laseron()
            else:
                pyrometer.laseroff()
            return pyrometer.temperature()
        if item == 'laseralarm':
            return laser.alarmstatus()
        if item == 'laserstatus':
            return laser.laserstatus()
        if item == 'setlasertimeout':
            laser.setmaxtimeout(command)
            return {'maxtime': settings['maxtime']}
        if item == 'restart':
            if command == 'pi':
                logger.warning('parsecontrol Restart command recieved: system will restart in 15 seconds')
                timerthread = Timer(15, reboot)
                timerthread.name = 'reboot-timer-thread'
                timerthread.start()
                return laser.laserstatus()
        if item == 'camera':
            return {'image': video_camera_instance_0.get_image()}
        if item == 'setting':
            logger.warning('parsecontrol Setting changed via api - %s', command)
            updatesetting(command)
            return settings
        return laser.laserstatus()
    except ValueError:
        logger.warning('parsecontrol incorrect json message')
        return laser.laserstatus()


def reboot():
    """API call to reboot the Raspberry Pi"""
    logger.warning('parsecontrol System is restarting now')
    os.system('sudo reboot')

laser = LaserClass()

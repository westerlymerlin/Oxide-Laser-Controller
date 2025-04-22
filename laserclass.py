"""
Laser Control System Implementation

This module provides a comprehensive interface for controlling and monitoring a laser system
through GPIO pins on a Raspberry Pi. It implements safety features including door interlocks,
key switch monitoring, and automatic timeout protection.

Key Features:
- Laser power control via PWM (Pulse Width Modulation)
- Safety interlocks monitoring (door and key switch)
- Automatic laser shutdown after configurable timeout
- Real-time status monitoring and reporting
- Temperature monitoring via pyrometer integration
- Settings persistence and management

Classes:
    LaserClass: Main class for laser control and monitoring

Functions:
    updatesetting: Updates system settings
    parsecontrol: Main API entry point for laser control
    reboot: System reboot functionality

Dependencies:
    - RPi.GPIO: For GPIO control
    - time: For timing operations
    - threading: For background monitoring
    - app_control: For settings management
    - pyroclass: For temperature monitoring
    - logmanager: For system logging
"""
# pylint: disable=E1101
import os
from time import sleep, time
from threading import Timer
from RPi import GPIO
from app_control import settings, writesettings
from pyroclass import pyrometer
from logmanager import logger


class LaserClass:
    """
    Manages the operation and monitoring of a laser control system.

    This class provides functionalities to set up and manage the laser’s
    interlocks, power settings, status monitoring, and auto shut-off features
    based on safety and operational constraints. It continuously monitors the
    external conditions such as door interlock and key state to ensure the
    laser operates only under permissible conditions.

    :ivar dutycycle: Represents the power setting for the laser in percentage.
    :ivar laserstate: Indicates whether the laser is currently firing (1 for on, 0 for off).
    :ivar maxtime: Maximum duration (in seconds) the laser can continuously run.
    :ivar key_channel: GPIO channel used for monitoring the key switch state.
    :ivar door_channel: GPIO channel used for monitoring the door interlock state.
    :ivar door_led_channel: GPIO channel controlling the indicator LED for the door state.
    :ivar enable_channel: GPIO channel used to enable or disable laser firing.
    :ivar ttl_channel: GPIO channel used for controlling the laser with pulse width modulation.
    :ivar laser_led_channel: GPIO channel controlling the indicator LED for the laser state.
    :ivar doorstate: Current state of the door interlock (1 for closed, 0 for open).
    :ivar keystate: Current state of the key switch (1 for on, 0 for off).
    :ivar laserenabled: Indicates whether the laser is enabled (1 for enabled, 0 for disabled).
    """
    def __init__(self):
        self.dutycycle = settings['power']
        self.laserstate = 0
        self.maxtime = settings['maxtime']
        self.key_channel = 12
        self.door_channel = 16
        self.door_led_channel = 24
        self.enable_channel = 21
        self.ttl_channel = 18
        self.laser_led_channel = 25
        self.doorstate = 0
        self.keystate = 0
        self.laserenabled = 0
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.door_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Door Interlock Reader
        GPIO.setup(self.door_led_channel, GPIO.OUT)  # Door LED
        GPIO.output(self.door_led_channel, 0)
        GPIO.setup(self.key_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Key Switch Reader
        GPIO.setup(self.enable_channel, GPIO.OUT)
        GPIO.output(self.enable_channel, 0)
        GPIO.setup(self.ttl_channel, GPIO.OUT)  # Laser PWM
        self.laser_pwm = GPIO.PWM(self.ttl_channel, settings['frequency'])
        GPIO.output(self.ttl_channel, 0)
        GPIO.setup(self.laser_led_channel, GPIO.OUT)  # Laser LED
        self.laserled_pwm = GPIO.PWM(self.laser_led_channel, 2)
        GPIO.output(self.laser_led_channel, 0)
        timerthread = Timer(0.5, self.interlockmonitor)
        timerthread.name = 'laser-interlock-monitor-thread'
        timerthread.start()
        logger.info('LaserClass initialised')

    def interlockmonitor(self):
        """Monitor the door interlock and switch off the laser if the door is open"""
        while True:
            if self.doorstate == GPIO.input(self.door_channel):
                self.doorstate = not GPIO.input(self.door_channel)
                GPIO.output(self.door_led_channel, self.doorstate)
                logger.info('LaserClass Door Interlock State = %i', self.doorstate)
            if self.keystate != GPIO.input(self.key_channel):
                self.keystate = GPIO.input(self.key_channel)
                logger.info('LaserClass Key Switch State = %i', self.keystate)
            if self.doorstate + self.keystate == 2:
                if self.laserenabled == 0:
                    self.laserenabled = 1
                    logger.info('LaserClass Laser is enabled')
                    GPIO.output(self.enable_channel, 1)
            else:
                if self.laserenabled == 1:
                    self.laserenabled = 0
                    logger.info('LaserClass Laser is disabled')
                    GPIO.output(self.enable_channel, 0)
            sleep(0.5)

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

    def laserstatus(self):
        """Return the laser (firning) status and the power setting"""
        return {'laser': self.laserstate, 'power': settings['power'], 'keyswitch': not self.keystate,
                'doorinterlock': not self.doorstate, 'autooff': self.maxtime, 'enabled': self.laserenabled}

    def laserhttpsstatus(self):
        """Return the laser (firning) status and the power setting"""
        if self.doorstate == 1:
            doorstatus = 'Door Closed'
        else:
            doorstatus = 'Door Open'
        if self.keystate == 1:
            keystatus = 'Key On'
        else:
            keystatus = 'Key Off'
        if self.laserstate == 1:
            laserstatus = 'Laser On'
        else:
            laserstatus = 'Laser Off'
        if self.laserenabled == 1:
            laserenabled = 'Enabled'
        else:
            laserenabled = 'Disabled'
        return {'laser': laserstatus, 'power': settings['power'], 'keyswitch': keystatus,
                'doorinterlock': doorstatus, 'autooff': self.maxtime, 'enabled': laserenabled}

    def laser(self, state):
        """Switch on or off the laser, if laser is on then run a thread to switch off if max time is exceeded"""
        if state == 1:
            if self.doorstate + self.keystate != 2:
                logger.warning('LaserClass Laser was not switched on, key switch or door interlock was engaged')
                self.laserstate = 0
                return
            logger.info('LaserClass Switching laser on')
            pyrometer.readinterval = 1
            self.laser_pwm.ChangeFrequency(settings['frequency'])
            self.laser_pwm.start(self.dutycycle)
            self.laserled_pwm.start(self.dutycycle)
            self.laserstate = 1
            # Start a  timer for the laser, if the laser is not shutdown this timer will shut it down
            timerthread = Timer(0.5, self.laserofftimer)
            timerthread.name = 'laser-off-timer-thread'
            timerthread.start()
        else:
            pyrometer.readinterval = 5
            logger.info('LaserClass Laser is off')
            self.laserstate = 0
            self.laser_pwm.stop()
            self.laserled_pwm.stop()

    def laserofftimer(self):
        """Auto switch off of the laser after maxtime seconds"""
        offtime = time() + settings['maxtime']
        while self.laserstate == 1:
            if time() > offtime:
                self.laser(0)
            sleep(1)




def updatesetting(newsetting): # must be a dict object
    """Update the settings with the new values"""
    if isinstance(newsetting, dict):
        for item in newsetting.keys():
            settings[item] = newsetting[item]
        writesettings()


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
            return laser.laserstatus()
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
        if item == 'updatesetting':
            logger.warning('parsecontrol Setting changed via api - %s', command)
            updatesetting(command)
            return settings
        if item == 'getsettings':
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

"""
Module for controlling and monitoring a LaserTree K60 450nm laser system.

This module interacts with GPIO channels on a Raspberry Pi to manage the laser system,
including interlocks for door and key switch states. It contains utility to monitor
hardware statuses and perform necessary operations, such as enabling and disabling
the laser based on safety conditions.

The laser power is managed by pulse width modulation (PWM) output on a digital channel.
The laser is automatically turned off after a specified timeout period if it is not
shut down by API control.
"""
from threading import Thread
from time import time, sleep
from digital_class import digital_channels
from serial_class import serial_channels
from logmanager import logger
from app_control import settings, writesettings


class LaserObject:
    """
    Handles laser operations, safety interlocks, and status monitoring.

    This class provides the necessary functionality for laser management, including
    power control, safety interlock monitoring, and operational status updates. It
    interfaces with hardware and software components to ensure safety compliance
    and controlled operation of the laser.
    """
    def __init__(self):
        """
        Initializes an instance of the class.

        This constructor method sets up internal variables and configurations required
        for the operation of the associated hardware or simulation. The attributes
        include various channel assignments and state indicators, ensuring all
        necessary initialization details are handled.

        """
        self._laser_pwm_ch = 9
        self._door_led_ch = 11
        self._laser_warning_ch = 12
        self._key_switch_ch = 13
        self._door_switch_ch = 14
        self._laser_enable_ch = 16
        self._laser_state = 0
        self._laser_enabled = 0
        self._key_state = 0
        self._door_state = 0
        self._laser_max_time = settings['laser-maxtime']
        self.interlock_monitor_thread = Thread(target=self.interlock_monitor)
        self.interlock_monitor_thread.name = 'Laser safety interlock monitor thread'
        self.interlock_monitor_thread.start()

    def check_door_state(self):
        """Returns a 0 for door closed and 1 for door open alarm, door switch will ground te GPIO pin so will generate
         a 0 for closed and a 1 for open. Sets the door LED to show it is closed (on) or open (off)."""
        door_state = digital_channels[self._door_switch_ch].read()
        if self._door_state != door_state:
            self._door_state = door_state
            digital_channels[self._door_led_ch].write(self._door_state)
            logger.info('LaserClass Door State has changed to = %i', self._door_state)
        return self._door_state

    def check_key_state(self):
        """Returns a 1 for key switch closed and 0 for key switch open"""
        key_state = int(not digital_channels[self._key_switch_ch].read())  # Invert the key switch state
        if self._key_state != key_state:
            self._key_state = key_state
            logger.info('LaserClass Key State has changed to = %i', self._key_state)
        return self._key_state

    def interlock_monitor(self):
        """
        Monitors the state of the door and key inputs, and controls the laser enable
        state based on their statuses. This method performs continuous checks and
        updates the states accordingly by interacting with GPIO channels. Both door
        and key states should be 0 (not alarming) for the laser to be enabled.
        """
        while True:
            if self.check_door_state() + self.check_key_state() == 0:
                if self._laser_enabled == 0:
                    self._laser_enabled = 1
                    logger.info('LaserClass Laser is enabled')
                    digital_channels[self._laser_enable_ch].write(self._laser_enabled)
            else:
                if self._laser_enabled == 1:
                    self._laser_enabled = 0
                    logger.info('LaserClass Laser is disabled')
                    digital_channels[self._laser_enable_ch].write(self._laser_enabled)
            sleep(0.5)

    def laser_status(self, item, command, exception=None):
        """Returns the current laser power level."""
        if exception:
            return {'item': item, 'command': command, 'exception': exception,
                    'values': {'laser': digital_channels[self._laser_pwm_ch].read(),
                    'laser_enabled': self._laser_enabled, 'power': digital_channels[self._laser_pwm_ch].pwm,
                    'door': self._door_state, 'key': self._key_state, 'laser_maxtime': self._laser_max_time}}
        return {'item': item, 'command': command, 'values': {'laser': digital_channels[self._laser_pwm_ch].read(),
                                                                  'laser_enabled': self._laser_enabled,
                                                                  'power': digital_channels[self._laser_pwm_ch].pwm,
                                                                  'door': self._door_state, 'key': self._key_state,
                                                             'laser_maxtime': self._laser_max_time}}

    def set_laser_power(self, item, command):
        """Sets the laser power level based on the given value."""
        if command > 100:
            command = 100
        elif command < 0:
            command = 0
        digital_channels[self._laser_pwm_ch].change_setting('pwm', command)
        logger.info('LaserClass Laser power level set to %i', command)
        return self.laser_status(item, command)

    def laser_set_maxtime(self, item, command):
        """Sets the laser timeout time based on the given value."""
        if command > 900:
            command = 900
        elif command < 60:
            command = 60
        self._laser_max_time = command
        settings['laser-maxtime'] = command
        writesettings()
        logger.info('LaserClass Laser timeout set to %i', command)
        return self.laser_status(item, command)

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
                self.laser_on_off('auto-laser-off', 0)
                logger.info('LaserClass Laser has been turned off due to timeout')
            sleep(1)

    def laser_on_off(self, item, command):
        """
        Handles the operation of a laser based on the given state. The method accordingly
        ensures the required conditions are met for turning the laser on. If the state
        is turned on, timers are initialized to regulate automatic shutdowns of the laser.
        If the state is turned off, the laser components and associated digital channels
        are duly deactivated.
        """
        if command == 1:
            if self.check_door_state() + self.check_key_state() != 2:
                logger.warning('LaserClass Laser was not switched on as key is off door open')
                self._laser_state = 0
                return self.laser_status(item, command, 'Key off or door open')
            logger.info('LaserClass Switching laser on')
            serial_channels['pyrometer'].change_poll_interval(1)
            digital_channels[self._laser_pwm_ch].write(settings['digital_on_command'])
            digital_channels[self._laser_warning_ch].write(settings['digital_on_command'])
            self._laser_state = 1
            # Start a  timer for the laser, if the laser is not shutdown this timer will shut it down
            timerthread = Thread(target=self.laser_off_timer)
            timerthread.name = 'laser-off-timer-thread'
            timerthread.start()
        else:
            serial_channels['pyrometer'].change_poll_interval(0)
            logger.info('LaserClass Laser is off')
            self._laser_state = 0
            digital_channels[self._laser_pwm_ch].write(settings['digital_off_command'])
            digital_channels[self._laser_warning_ch].write(settings['digital_off_command'])
        return self.laser_status(item, command)

    def http_status_data(self, item, command):
        """Returns a formatted dictionary of laser status data for the index page."""
        http_data = {'item': item, 'command': command, 'values': {}}
        if self._key_state == 0:
            http_data['values']['key'] = {'name': 'Key', 'direction': 'input', 'value': 'Key on', 'enabled': True}
        else:
            http_data['values']['key'] = {'name': 'Key', 'direction': 'input', 'value': 'Key off', 'enabled': True}
        if self._door_state == 0:
            http_data['values']['door'] = {'name': 'Door', 'direction': 'input', 'value': 'Closed', 'enabled': True}
        else:
            http_data['values']['door'] = {'name': 'Door', 'direction': 'input', 'value': 'Open', 'enabled': True}
        if self._laser_enabled == 1:
            if self._laser_state == 1:
                http_data['values']['laser'] = {'name': 'Laser', 'direction': 'output pwm', 'value': 'Firing', 'enabled': True}
            else:
                http_data['values']['laser'] = {'name': 'Laser', 'direction': 'output', 'value': 'Standby', 'enabled': True}
        else:
            http_data['values']['laser'] = {'name': 'Laser', 'direction': 'output', 'value': 'Power off', 'enabled': True}
        http_data['values']['power'] = {'name': 'Laser Power', 'direction': 'setting',
                                             'value': '%s %%' % digital_channels[self._laser_pwm_ch].pwm, 'enabled': True}
        return http_data

laser = LaserObject()

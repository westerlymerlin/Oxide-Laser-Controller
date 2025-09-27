"""
Raspberry Pi GPIO Digital I/O Control Module

This module provides a comprehensive interface for configuring and interacting with
Raspberry Pi GPIO pins. It abstracts the hardware-level details of GPIO operations
into a user-friendly class-based API, supporting both input and output operations.

Key features:
- ChannelObject class for configuring and interacting with individual GPIO channels
- Support for reading digital input values from GPIO pins
- Support for writing digital output values to GPIO pins
- Helper functions for checking digital key format and converting values
- System-wide digital channel initialization and management

The module integrates with the application's settings and logging systems to provide
consistent behavior and traceable operations across the entire application.

Dependencies:
    RPi.GPIO: For hardware-level GPIO control
    logmanager: For logging GPIO operations and errors
    app_control: For accessing application-wide settings
"""

from RPi import GPIO
from logmanager import logger
from app_control import settings, writesettings

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class ChannelObject:
    """
    Represents a GPIO channel object for controlling and reading GPIO pins.

    This class provides functionality to configure a GPIO channel for input or
    output and read/write digital values. It also maintains details about the
    channel, such as its current state, direction, and description.
    """

    def __init__(self, channel_settings, channel_id):
        """
        Initializes a new instance of the GPIO configuration class.

        This constructor sets up the configuration for a General Purpose Input/Output
        (GPIO) pin, including its pin number, direction, whether it is enabled, and
        additional descriptive attributes. These parameters define the behavior and
        the state of the GPIO pin.
        """
        self.digital_id = channel_id
        self.gpio = channel_settings['gpio']
        self.direction = channel_settings['direction']
        self.enabled = channel_settings['enabled']
        self.name = channel_settings['name']
        self._running = 0  # used for PWM
        self.excluded = channel_settings['excluded']
        try:
            self.pwm = channel_settings['pwm']
        except KeyError:
            self.change_setting('pwm', 0)
        try:
            self.frequency = channel_settings['frequency']
        except KeyError:
            self.change_setting('frequency', 100)
        if self.direction == 'input':
            GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        elif self.direction == 'output pwm':
            GPIO.setup(self.gpio, GPIO.OUT)
            self.gpio_pwm = GPIO.PWM(self.gpio, channel_settings['frequency'])
        else:
            GPIO.setup(self.gpio, GPIO.OUT)

    def write(self, value):
        """
        Sets the digital channel to the specified value if it is enabled and configured
        as an output channel. The value controls the GPIO state based on predefined
        commands. Invalid values or improper configurations log warnings and result
        in no changes.

        :param value: The command to set the digital channel's GPIO (e.g., digital_on
                      or digital_off commands).
        :type value: str
        :return: The current state of the GPIO after attempting to set it, or -1 if
                 the operation fails due to a disabled channel, input configuration,
                 or invalid value.
        :rtype: int
        """
        if not self.enabled:
            logger.warning('Cannot set digital channel "%s" as it is disabled', self.name)
            return '', 'Cannot set digital channel %s as it is disabled' % self.name
        if self.direction == 'input':
            logger.warning('Cannot set digital channel "%s" as it is an input channel', self.name)
            return GPIO.input(self.gpio), 'Cannot set digital channel %s as it is an input channel' % self.name
        if value == settings['digital_on_command']:
            if int(self.excluded) > 0:
                if digital_channels[int(self.excluded)].read() == 1:
                    logger.warning('Cannot set digital channel "%s" as it is excluded partner is %s',
                                   self.name, digital_value(1))
                    return (GPIO.input(self.gpio), 'Cannot set digital channel %s as it is excluded partner is %s'
                            % (self.name, digital_value(1)))
            if self.direction == 'output pwm':
                self.gpio_pwm.ChangeFrequency(self.frequency)
                self.gpio_pwm.start(self.pwm)
                self._running = True
            else:
                GPIO.output(self.gpio, 1)
        elif value == settings['digital_off_command']:
            if self.direction == 'output pwm':
                self.gpio_pwm.stop()
                self._running = False
            else:
                GPIO.output(self.gpio, 0)
        else:
            logger.warning('Invalid value "%s" for digital channel "%s"', value, self.name)
            return 'Invalid value %s for digital channel %s' % (value, self.name)
        logger.info('Digital Channel "%s" set to "%s"', self.name, value)
        return ''

    def read(self):
        """
        Reads the current state of the GPIO pin.

        This method reads and returns the current logical state of the specified
        GPIO pin. It uses the GPIO library to retrieve the input value, which
        indicates whether the pin is logically HIGH or LOW.

        :return: Logical state of the GPIO pin as returned by the GPIO library
        :rtype: int or bool
        """
        if self.direction == 'output pwm':
            return self._running
        return GPIO.input(self.gpio)

    def change_setting(self, setting, value):
        """
        Updates a specific setting for the current instance and persists the change.

        This method modifies the attribute of the current instance with the provided
        `setting` and `value`. It also updates the corresponding setting in the global
        `settings` dictionary, ensuring that the digital channel's configuration is
        consistently maintained. Finally, the settings are saved via the writesettings()
        function, and a log entry is created indicating the updated settings.
        """
        if setting in['pwm', 'frequency']:
            value = float(value)
        if setting in ['GPIO']:
            value = int(value)
        setattr(self, setting, value)
        digital_prefix = '%d' % (self.digital_id)
        settings['digital_channels'][digital_prefix][setting] = value
        writesettings()
        logger.info('Digital channel %s setting %s updated', self.name, setting)

    def info(self):
        """
        Constructs and returns a dictionary containing detailed information about the
        current object instance.

        The returned dictionary includes the identifier, name, direction, status of
        the object (enabled/disabled), and its current value. If the direction is set
        to 'output pwm', additional fields like pwm and frequency are also included.
        """
        dataval= {'%s' % settings['digital_prefix']: self.digital_id,
                  'name': self.name,
                  'direction': self.direction,
                  'enabled': self.enabled,
                  'value': digital_value(self.read())}
        if self.direction == 'output pwm':
            dataval['pwm'] = self.pwm
            dataval['frequency'] = self.frequency
        return dataval


def check_digital_key(item):
    """
    Check if the given item matches a digital key based on a predefined prefix.

    This function iterates through a range of identifiers and checks if the
    provided item matches a specific format comprising a digital prefix and an
    identifier value. If a match is found, it returns True. Otherwise, it
    returns False.

    :param item: The item to be checked against the digital key format.
    :type item: str
    :return: A boolean indicating whether the given item matches the expected digital key format.
    :rtype: bool
    """
    for item_id in range(16, 0, -1):
        digital_prefix = '%s%d' % (settings['digital_prefix'], item_id)
        if item[:len(digital_prefix)] == digital_prefix:
            return True
    return False


def digital_value(value):
    """
    Convert a digital input value to its corresponding system-defined digital representation.

    This function checks the given digital input value and returns the corresponding value
    from the system's settings. If the input value does not match predefined digital states,
    it will return 'error'.

    :param value: The digital input value to evaluate.
    :type value: int
    :return: The system-defined digital value corresponding to the input or 'error' if the input
             is invalid.
    :rtype: str
    """
    if value == 1:
        return settings['digital_on_value']
    if value == 0:
        return settings['digital_off_value']
    return 'error'


def digital_single_channel(item, command):
    """
    Executes a command to read or write the state of a single digital channel.

    This function processes the input channel and state, determines the operation
    to perform, and either reads the current channel state or updates the channel's
    state based on the provided command. The function then returns the updated or
    read channel state in a predefined format.
    """
    error_message = ''
    if item[-4:] == '-pwm':
        channel = int(item[len(settings['digital_prefix']):-4])
        task = 'pwm'
    elif item[-10:] == '-frequency':
        channel = int(item[len(settings['digital_prefix']):-10])
        task = 'frequency'
    else:
        channel = int(item[len(settings['digital_prefix']):])
        if command in [settings['digital_on_command'], settings['digital_off_command']]:
            task= 'write'
        else:
            task = 'read'
    if task in ['pwm', 'frequency']:
        if digital_channels[channel].direction == 'output pwm':
            digital_channels[channel].change_setting(task, command)
        else:
            error_message = 'Cannot set %s for digital channel %s as it is not an output PWM channel' % (task, item)
    if task == 'write':
        error_message = digital_channels[channel].write(command)
    if error_message != '':
        return {'item': item, 'command': command, 'exception': error_message, 'values':
            {'%s%d' % (settings['digital_prefix'], channel): digital_channels[channel].info()}}
    return {'item': item, 'command': command, 'values': digital_channels[channel].info()}


def digital_all_values(item, command):
    """
    Generates a json representation of digital values for configured digital channels.

    This function iterates through a predefined range of digital channel IDs, retrieves
    their respective metadata and status, and returns a dictionary containing the
    digital channel attributes.

    :return: A dictionary representing the digital channels' values, where the keys
             are prefixed with the configured digital prefix, and the values contain
             the channel's ID, name, direction, status, and whether it is enabled.
    :rtype: dict
    """
    returned_data = {}
    for item_id in range(1, 17):
        if digital_channels[item_id].enabled:
            returned_data['%s%d' % (settings['digital_prefix'], item_id)] = digital_channels[item_id].info()
    return {'item': item, 'command': command, 'values': returned_data}


# setup digital channels
digital_channels = {}
for i in range(1, 17):
    digital_channels[i] = ChannelObject(settings['digital_channels'][str(i)], i)

"""
Serial Communication Management Module

This module provides comprehensive serial (RS232/RS485) communication functionality
for device control and data acquisition. It supports both interactive command-response
communication and passive listener modes for continuous data monitoring.

Key Features:
    - Multi-port serial connection management with configurable parameters
    - Interactive mode for command-response protocols
    - Listener mode for passive data acquisition with configurable polling
    - Base64 encoding/decoding for message storage and transmission
    - Automatic message parsing and value extraction
    - Thread-safe operations with built-in retry mechanisms
    - Dynamic port discovery and configuration management

Classes:
    SerialConnection: Main class for managing individual serial port connections

Functions:
    Configuration Management:
        - update_serial_channel: Create or update serial channel settings
        - delete_serial_channel: Remove serial channel configuration
        - update_serial_message: Add or modify message definitions
        - delete_serial_message: Remove message definitions
        - serial_port_info: Retrieve detailed port configuration

    Utility Functions:
        - str_encode/str_decode: Base64 string encoding/decoding
        - serial_ports: Auto-discover available serial ports
        - serial_http_data: Aggregate data from all configured channels

Communication Modes:
    Interactive: Send commands and read responses with configurable timing
    Listener: Continuously monitor incoming data and extract specific values

Dependencies:
    - pyserial: Core serial communication
    - threading: Background data acquisition
    - base64: Message encoding/storage
    - app_control: Configuration management
    - logmanager: Activity logging

Usage:
    The module automatically initializes all configured serial channels on import.
    Channels can be managed through the configuration functions, and data can be
    accessed via the serial_http_data() function or individual channel instances.
"""
from ast import literal_eval
from time import sleep
from threading import Timer
from base64 import b64decode, b64encode
from datetime import datetime
import glob
import sys
import serial  # from pyserial
from logmanager import logger
from app_control import settings, writesettings, friendlyname, jscriptname


def str_encode(string):
    """
    Encodes a given string to its Base64 representation.

    This function takes a string and encodes it using Base64. The encoding
    is performed by first converting the string to its byte representation
    in UTF-8, then applying Base64 encoding to it, and finally decoding
    the resulting bytes back into a string.
    """
    return b64encode(string).decode('utf-8')


def str_decode(string):
    """
    Decodes a Base64 encoded string into a UTF-8 string.

    This function takes a string that is Base64 encoded, decodes it from
    Base64, and then decodes the resulting bytes into a UTF-8 string.
    """
    return b64decode(string)


def update_serial_channel(newsettings):
    """
    Updates the serial channel settings with given new settings.

    This function updates the configuration for a serial channel with the provided
    settings. If the serial channel with the same port already exists, it retains
    existing messages while updating other parameters. Otherwise, it adds a new
    serial channel to the configuration. The updated configuration is sorted by
    the 'api-name' field before saving.
    """
    serial_channel_list = []
    serial_channel= {'api-name': friendlyname(newsettings['api-name']), 'port': newsettings['port'],
                     'mode': newsettings['mode'], 'baud': int(newsettings['baud']),
                     'poll_interval': int(newsettings['poll_interval']), 'messages': []}
    if len(settings['serial_channels']) == 0:
        settings['serial_channels'] = [serial_channel]
        writesettings()
        return serial_channel
    for conn in settings['serial_channels']:
        if conn['port'] == newsettings['port']:
            serial_channel['messages'] = conn['messages']
        else:
            serial_channel_list.append(conn)
    serial_channel_list.append(serial_channel)
    serial_channel_list.sort(key=lambda x: x['api-name'])
    settings['serial_channels'] = serial_channel_list
    writesettings()
    logger.info('Serial Class: serial channel %s updated', newsettings['port'])
    return serial_channel


def delete_serial_channel(port_id):
    """
    Delete a serial communication channel matching the specified port.

    This function takes in a port identifier and removes the corresponding serial
    communication channel from the current settings. If a match is found for the
    provided port, the channel is excluded, the updated list is saved back to the
    settings, and a confirmation is logged. The function also returns the modified
    list of channels.
    """
    serial_channel_list = []
    for conn in settings['serial_channels']:
        if conn['port'] != port_id:
            serial_channel_list.append(conn)
    settings['serial_channels'] = serial_channel_list
    writesettings()
    logger.info('Serial Class: serial channel %s deleted', port_id)
    return serial_channel_list


def update_serial_message(newsettings):
    """
    Update and manage the serial message structure and settings.

    This function takes a new set of serial message settings, encodes required
    settings, updates the corresponding serial channel messages based on the
    port, and writes the updated settings. It logs actions performed and
    manages the organization of messages for a serial channel.
    """
    print(newsettings['string1'], newsettings['string2'])
    try:
        string1 = literal_eval(newsettings['string1'])
    except (ValueError, SyntaxError):
        string1 = literal_eval("b'%s'" %newsettings['string1'])
    try:
        string2 = literal_eval(newsettings['string2'])
    except (ValueError, SyntaxError):
        string2 = literal_eval("b'%s'" %newsettings['string2'])
    newmessages = [{'name': newsettings['name'], 'string1': str_encode(string1),
                    'string2': str_encode(string2), 'start': int(newsettings['start']),
                    'length': int(newsettings['length']), 'api-command': friendlyname(newsettings['api-command'])}]
    for conn in settings['serial_channels']:
        if conn['port'] == newsettings['port']:
            for message in conn['messages']:
                if message['name'] != newsettings['name']:
                    newmessages.append(message)
            newmessages.sort(key=lambda x: x['name'])
            conn['messages'] = newmessages
    writesettings()
    logger.info('Serial Class: serial message %s added to %s', newsettings['name'], newsettings['port'])
    return newmessages


def delete_serial_message(newsettings):
    """
    Deletes a specific serial message from the configuration of a serial port.

    This function iterates through the existing serial channels to remove a
    message that matches the name and port specified in the provided settings.
    After performing the deletion, the updated settings are saved, and an
    informational log message is generated.
    """
    newmessages = []
    for conn in settings['serial_channels']:
        if conn['port'] == newsettings['port']:
            for message in conn['messages']:
                if message['name'] != newsettings['name']:
                    newmessages.append(message)
            conn['messages'] = newmessages
    writesettings()
    logger.info('Serial Class: serial message %s deleted from %s', newsettings['name'], newsettings['port'])
    return newmessages


def serial_port_info(port_id):
    """
    Retrieve detailed information about a serial port configuration.

    The function gathers and returns information about a serial port, such as its
    API-friendly name, mode, baud rate, polling interval, and associated messages.
    If the port is found in the existing serial channel settings, detailed
    configuration for the port is retrieved; otherwise, default settings are used.
    """
    serial_details = {'api-name': friendlyname(port_id), 'port': port_id, 'mode': 'interactive',
                      'baud': 9600, 'poll_interval': 10, 'messages':[], 'configured': False}
    for conn in settings['serial_channels']:
        if conn['port'] == port_id:
            serial_details['mode'] = conn['mode']
            serial_details['baud'] = conn['baud']
            serial_details['api-name'] = conn['api-name']
            serial_details['poll_interval'] = conn['poll_interval']
            messages=[]
            for message in conn['messages']:
                messages.append({'api-command': message['api-command'], 'name': message['name'], 'string1': str_decode(message['string1']),
                                 'string2': str_decode(message['string2']), 'start': message['start'],
                                 'length': message['length']})
            serial_details['configured'] = True
            serial_details['messages'] = messages
    return serial_details


def serial_ports():
    """ Lists serial port names available on the system

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        detected_ports = ['COM%s' % (i + 1) for i in range(8)]
        return detected_ports # # work around for testing on windows
    if sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        detected_ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        detected_ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for serial_port in detected_ports:
        try:
            s = serial.Serial(serial_port)
            s.close()
            result.append(serial_port)
        except (OSError, serial.SerialException):
            pass
    return result


class SerialConnection:
    """
    Handles serial communication by initializing, configuring, and managing the serial
    port connection. Provides functionality to interact with devices using a specific
    communication protocol and read messages based on predefined listener configurations.

    Designed for applications requiring consistent serial port communication, with support
    for interactive and non-interactive (listener) modes. The class allows users to automate
    polling of devices and processing of incoming data based on predefined configurations.
    """
    def __init__(self, device):
        self._portready = False
        self._baudrate = device['baud']
        self._port = device['port']
        self.port = None
        self._mode = device['mode']
        self._active = False
        self._name = device['api-name']
        if self._mode == 'interactive':
            self._readbuffer = 256
        else:
            self._readbuffer = 1024
        self._default_poll_interval = device['poll_interval']
        self._poll_interval =  self._default_poll_interval
        self._listener_messages = []
        self._api_messages = []
        self._listener_values = []
        for message in device['messages']:
            if message['api-command'] == '':
                self._listener_messages.append({'name': message['name'], 'string1': message['string1'],
                                                'string2': message['string2'], 'start': message['start'],
                                                'length': message['length']})
                self._listener_values.append({'name': message['name'], 'port': self._port, 'value': '0',
                                              'portstatus': '%s Not Ready' % self._port, "read_time": "01-01-1979 00:00:00"})
            else:
                self._api_messages.append({'name': message['name'], 'string1': message['string1'],
                                           'string2': message['string2'], 'start': message['start'],
                                           'length': message['length'], 'api-command': message['api-command']})
        self.init_port()

    def init_port(self):
        """
        Initialize the serial port with specified parameters. This method attempts to
        establish a connection to the serial port using the given port and baud rate.
        Upon successful initialization, the input buffer is reset and the port is
        marked as ready. If the connection fails, the port is marked as not ready.
        """
        try:
            self.port = serial.Serial(self._port, self._baudrate, timeout=1)
            self.port.reset_input_buffer()
            self._portready = True
            print('Serial Class: %s connected' % self._port)
            logger.info('Serial Class: %s connected', self._port)
            if len(self._listener_messages) > 0:
                reader_thread = Timer(1, self.listener_timer)
                reader_thread.name = 'Serial listener %s' % self._name
                reader_thread.start()
        except serial.SerialException:
            self._portready = False
            logger.error('Serial Class: %s not connected', self._port)

    def name(self):
        """
        Retrieves the value of the name attribute.
        """
        return self._name

    def listener_timer(self):
        """
        Reads data from a serial port in a loop with a specified polling interval. The behavior
        differs based on the mode of operation ('listener' or otherwise). If in 'listener' mode,
        it processes incoming data to extract specific substrings based on predefined message definitions.
        """
        while True:
            try:
                retrycounter = 0
                while self._active:
                    sleep(0.1)
                    retrycounter += 1
                    if retrycounter > 10:
                        logger.warning('Serial Class: Listener waiting for more than 1s for port %s to become free on', self._port)
                        break
                self._active = True
                listener_values = []
                self.port.reset_input_buffer()
                if self._mode == 'interactive':
                    for item in self._listener_messages:
                        self.port.write(b64decode(item['string1']))
                        sleep(0.5)
                        databack = str(self.port.read(size=self._readbuffer), 'utf-8')
                        if item['string2']:
                            self.port.write(b64decode(item['string2']))
                            sleep(0.5)
                            databack = str(self.port.read(size=self._readbuffer), 'utf-8')
                        listener_values.append({'name': item['name'], 'port': self._port,
                                                'value': databack[item['start']:item['length']],
                                                'portstatus': '%s (%s)' %(self._name, self._port),
                                                "read_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                else:
                    databack = str(self.port.read(size=self._readbuffer), 'utf-8')
                    for item in self._listener_messages:
                        name = item['name']
                        findstring = str_decode(item['string1']).decode('utf-8')
                        length = item['length']
                        position = databack.find(findstring)
                        if position > -1:
                            listener_values.append({'name': name,  'port': self._port,
                                          'value': databack[position + len(findstring):position + len(findstring) + length - 1],
                                                'portstatus': '%s (%s)' %(self._name, self._port),
                                                "read_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                        else:
                            listener_values.append({'name': name, 'port': self._port,
                                                    'value': '', 'portstatus': '%s (%s)' %(self._name, self._port),
                                                    "read_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                logger.debug('Serial Class: Serial Return "%s" from %s', self._listener_values, self._port)
                self._active = False
                if len(listener_values) > 0:
                    logger.debug('Serial Class: Listener Return "%s" from %s', listener_values, self._port)
                    self._listener_values = listener_values
            except serial.SerialException :
                self._active = False
                logger.exception('Serial Class: Listener Read Error on %s: %s', self._port, Exception)
            sleep_counter = 0
            while sleep_counter < self._poll_interval:
                sleep_counter += 1
                sleep(1)

    def api_command(self, item, command):
        """
        Executes a specified API command by sending encoded data via a serial port and reads back the
        response. The method will match the provided command with predefined messages, decode the
        associated strings, and send them sequentially through the serial port. It returns the result of
        the operation.

        The method handles errors related to the serial port and returns a descriptive error message if
        a SerialException occurs or if the serial port is not ready.
        """
        try:
            for message_item in self._api_messages:
                if message_item['api-command'] == command:
                    self.port.write(b64decode(message_item['string1']))
                    sleep(0.5)
                    databack = str(self.port.read(size=self._readbuffer), 'utf-8')
                    if message_item['string2']:
                        self.port.write(b64decode(message_item['string2']))
                        sleep(0.5)
                        databack = str(self.port.read(size=self._readbuffer), 'utf-8')
                    return {'item': item,'command': command, 'values': databack}
            return {'item': item, 'command': command, 'values': '', 'exception': 'Command not found'}
        except serial.SerialException :
            logger.exception('Serial Class: API Command Error on %s: %s', self._port, Exception)
            return {'item': item, 'command': command, 'values': '', 'exception': 'Serial Port Error or not ready'}

    def listener_values(self):
        """
        Retrieves the current listener values.

        This method provides access to the internal state of listener values used
        in the class.
        """
        return self._listener_values

    def change_poll_interval(self, value):
        """
        Updates the poll interval to the specified value. Entering 0 returns to the default value
        """
        if value > 0:
            self._poll_interval = value
        else:
            self._poll_interval = self._default_poll_interval



def serial_http_data(item, command):
    """
    Collects and aggregates all listener values from all channels into a single dictionary for the index page.

    This function iterates through all the channels in `serial_channels` and processes their
    listener values, creating a unified dictionary where each key is constructed using the port
    and name of the message, and the corresponding value is the message itself.
    """
    serial_data = {}
    for channel in serial_channels.values():
        for message in channel.listener_values():
            serial_data['%s%s' %(jscriptname(message['port']), jscriptname(message['name']))] = message
    return {'item': item, 'command': command, 'values': serial_data}


def serial_api_parser(item, command):
    """
    Parses a serial API command and matches it to a corresponding serial channel.
    Executes the parsed command or retrieves a channel-specific listener status.
    """
    for channel in serial_channels.values():
        if item[:len(channel.name())] == channel.name():
            if item == channel.name() + 'status':
                return {'item': item, 'command': command, 'values': channel.listener_values()}
            return channel.api_command(item, command)
    return {'item': item, 'command': command, 'values': '', 'exception': 'Command not found'}


# setup the serial channels
serial_channels = {}
for port in settings['serial_channels']:
    serial_channels[port['api-name']] = SerialConnection(port)


def serial_api_checker(item):
    """
    Checks whether the given item matches the name of any serial channel.

    This function iterates over all available serial channels and checks if the
    provided item's prefix matches the name of any channel. If a match is found,
    the function returns True, otherwise it returns False.
    """

    for channel in serial_channels.values():
        if item[:len(channel.name())] == channel.name():
            return True
    return False


if __name__ == '__main__':
    sleep(1)
    from json import dumps
    print(dumps({'serial_status': serial_http_data(False, False)}))

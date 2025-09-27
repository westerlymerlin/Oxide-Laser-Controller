"""
Application control and configuration management for the Raspberry Pi control system.

This module manages core application configuration, settings, and version information
for the Flask-based control system. It handles loading and maintaining application-wide
settings that define crucial operational parameters.

Attributes:
    VERSION (str): The current version of the application
    settings (dict): Application-wide configuration dictionary containing:
        - app-name (str): Application identifier used in logging and display
        - api-key (str): Authentication key for API access control
        - cputemp (str): File path for CPU temperature readings
        - logfilepath (str): Path to application log file
        - gunicornpath (str): Base directory for Gunicorn log files

Note:
    This module is a central configuration point for the application and should
    be imported by other modules that need access to global settings or version
    information.

"""

import random
import json
from base64 import b64decode, b64encode
from datetime import datetime
from custom_settings import custom_settings

VERSION = '1.6.0'
API_KEY=''

def initialise():
    """Setup the settings dict structure with default values"""
    isettings = {'LastSave': '01/01/2000 00:00:01',
                 'api-key': 'Y2hhbmdlLW1l',
                 'oled_enabled': False,
                 'oled_address': 0x3C,
                 'oled_height': 64,
                 'oled_width': 128,
                 'app-name': 'TST Controller',
                 'cputemp': '/sys/class/thermal/thermal_zone0/temp',
                 'gunicornpath': './logs/',
                 'logappname': 'TST-Control',
                 'logfilepath': './logs/app.log',
                 'loglevel': 'INFO',
                 'digital_prefix': 'digital',
                 'digital_on_value': '1',
                 'digital_on_command': '1',
                 'digital_off_value': '0',
                 'digital_off_command': '0',
                 'digital_channels': {
                 '1': {'name': 'Digital 1', 'gpio': 26, 'direction': 'output', 'enabled': True, 'excluded': '0',
                        'pwm': 50, 'frequency': 500},
                 '2': {'name': 'Digital 2', 'gpio': 19, 'direction': 'output', 'enabled': True, 'excluded': '0',
                        'pwm': 50, 'frequency': 500},
                 '3': {'name': 'Digital 3', 'gpio': 13, 'direction': 'output', 'enabled': True, 'excluded': '0',
                       'pwm': 50, 'frequency': 500},
                 '4': {'name': 'Digital 4', 'gpio': 11, 'direction': 'output', 'enabled': True, 'excluded': '0',
                        'pwm': 50, 'frequency': 500},
                 '5': {'name': 'Digital 5', 'gpio': 9, 'direction': 'output', 'enabled': True, 'excluded': '0',
                        'pwm': 50, 'frequency': 500},
                 '6': {'name': 'Digital 6', 'gpio': 22, 'direction': 'output', 'enabled': True, 'excluded': '0',
                        'pwm': 50, 'frequency': 500},
                 '7': {'name': 'Digital 7', 'gpio': 27, 'direction': 'output', 'enabled': True, 'excluded': '0',
                        'pwm': 50, 'frequency': 500},
                 '8': {'name': 'Digital 8', 'gpio': 17, 'direction': 'output', 'enabled': True, 'excluded': '0',
                        'pwm': 50, 'frequency': 500},
                 '9': {'name': 'Digital 9', 'gpio': 18, 'direction': 'output', 'enabled': True, 'excluded': '0',
                        'pwm': 50, 'frequency': 500},
                 '10': {'name': 'Digital 10', 'gpio': 23, 'direction': 'output', 'enabled': True, 'excluded': '0',
                        'pwm': 50, 'frequency': 500},
                 '11': {'name': 'Digital 11', 'gpio': 24, 'direction': 'output', 'enabled': True, 'excluded': '0',
                        'pwm': 50, 'frequency': 500},
                 '12': {'name': 'Digital 12', 'gpio': 25, 'direction': 'output', 'enabled': True, 'excluded': '0',
                        'pwm': 50, 'frequency': 500},
                 '13': {'name': 'Digital 13', 'gpio': 12, 'direction': 'output', 'enabled': True, 'excluded': '0',
                        'pwm': 50, 'frequency': 500},
                 '14': {'name': 'Digital 14', 'gpio': 16, 'direction': 'output', 'enabled': True, 'excluded': '0',
                        'pwm': 50, 'frequency': 500},
                 '15': {'name': 'Digital 15', 'gpio': 20, 'direction': 'output', 'enabled': True, 'excluded': '0',
                        'pwm': 50, 'frequency': 500},
                 '16': {'name': 'Digital 16', 'gpio': 21, 'direction': 'output', 'enabled': True, 'excluded': '0',
                        'pwm': 50, 'frequency': 500}},
                 'analogue_prefix': 'analogue',
                 'analogue_installed': False,
                 'analogue_i2c': 0x48,
                 'analogue_channels': {
                 '1': {'name': 'Analogue 1', 'pin': 0, 'enabled': False},
                 '2': {'name': 'Analogue 2', 'pin': 1, 'enabled': False},
                 '3': {'name': 'Analogue 3', 'pin': 2, 'enabled': False},
                 '4': {'name': 'Analogue 4', 'pin': 3, 'enabled': False}},
                 'serial_channels': []
                 }
    isettings.update(custom_settings)
    return isettings


def generate_api_key(key_len):
    """generate a new random api-key"""
    allowed_characters = "ABCDEFGHJKLMNPQRSTUVWXYZ-+~abcdefghijkmnopqrstuvwxyz123456789"
    return ''.join(random.choice(allowed_characters) for _ in range(key_len))


def writesettings():
    """Write settings to a json file"""
    settings['LastSave'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    with open('settings.json', 'w', encoding='utf-8') as outfile:
        json.dump(settings, outfile, indent=4, sort_keys=True)

def readsettings():
    """Read the json file"""
    try:
        with open('settings.json', 'r', encoding='utf-8') as json_file:
            jsettings = json.load(json_file)
            return jsettings
    except FileNotFoundError:
        print('File not found')
        return {}

def loadsettings():
    """Replace the default settings with those from the json files, if a setting is not in the json file (e.g. it is a
     new feature setting) then retain the default value and write that to the json file. If the api-key is the default
    value then generate a new key and save it."""
    global settings, API_KEY
    settingschanged = False
    fsettings = readsettings()
    for item in settings.keys():
        try:
            settings[item] = fsettings[item]
        except KeyError:
            print('settings[%s] Not found in json file using default' % item)
            settingschanged = True
    API_KEY = b64decode(settings['api-key']).decode('utf-8')
    if API_KEY == 'change-me':  # the default value which needs changing
        settings['api-key'] = b64encode(generate_api_key(128).encode('utf-8')).decode('utf-8')
        API_KEY = b64decode(settings['api-key']).decode('utf-8')
        settingschanged = True
    if settingschanged:
        writesettings()

def friendlyname(sourcename: str) -> str:
    """
    Replaces invalid characters in a string with hyphens to create a valid
    friendly file file or host name. Invalid characters include file system restricted
    characters such as '/', '\', ':', '*', '?', '<', '>', '"', '&', '%', '#', '$',
    "'", ',' and '.', which could cause issues in file or directory names. Multiple
    replacement hyphens caused due to consecutive invalid characters are also
    collapsed to a single hyphen. Spaces are also removed to allow this function to generate hostnames.

    :param sourcename: A string containing the original directory name, which
        potentially includes invalid characters that need to be replaced.
    :type sourcename: str

    :return: A sanitized directory name with invalid characters replaced and
        multiple hyphens collapsed into one.
    :rtype: str
    """
    if len(sourcename) == 0:
        return ''
    invalid_chars = ['/', '\\', ':', '*', '?', '<', '>', '"', '&', '%', '#', '$', "'", ',', '.', ' ']
    for invalid_char in invalid_chars:
        sourcename = sourcename.replace(invalid_char, '-')
    # Remove double dash characters
    while '--' in sourcename:
        sourcename = sourcename.replace('--', '-')
    # Remove leading or training -
    if sourcename[0] == '-':
        sourcename = sourcename[1:]
    if sourcename[-1] == '-':
        sourcename = sourcename[:-1]
    return sourcename.lower()

def jscriptname(sourcename: str) -> str:
    """
    Processes a source name string by removing invalid characters and converting it
    to lowercase. This function ensures the input string conforms to a format
    suitable for use in contexts where certain characters are not allowed.

    :param sourcename: Input string to be processed. It may contain
        potentially invalid characters.
    :type sourcename: str
    :return: A clean and lowercase version of the input string with invalid
        characters removed.
    :rtype: str
    """
    if len(sourcename) == 0:
        return ''
    invalid_chars = ['/', '\\', ':', '-', '*', '?', '<', '>', '"', '&', '%', '#', '$', "'", ',', '.', ' ']
    for invalid_char in invalid_chars:
        sourcename = sourcename.replace(invalid_char, '')
    return sourcename.lower()

settings = initialise()
loadsettings()

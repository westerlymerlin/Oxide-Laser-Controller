"""
A module for storing and managing configuration or custom settings.

This module provides a dictionary named `custom_settings` that can be
used to define and store custom configuration or settings. These settings
can be used across different parts of an application.

Attributes:
    custom_settings (dict): A dictionary to hold custom configuration
    settings, which can be set and accessed dynamically within the
    application.
"""

custom_settings = {
    'digital_channels': {
        '1': {
            'name': 'not configured',
            'gpio': 26,
            'direction': 'input',
            'enabled': False,
            'excluded': '0',
            'pwm': 50,
            'frequency': 500
        },
        '2': {
            'name': 'not configured',
            'gpio': 19,
            'direction': 'input',
            'enabled': False,
            'excluded': '0',
            'pwm': 50,
            'frequency': 500
        },
        '3': {
            'name': 'not configured',
            'gpio': 13,
            'direction': 'input',
            'enabled': False,
            'excluded': '0',
            'pwm': 50,
            'frequency': 500
        },
        '4': {
            'name': 'not configured',
            'gpio': 11,
            'direction': 'input',
            'enabled': False,
            'excluded': '0',
            'pwm': 50,
            'frequency': 500
        },
        '5': {
            'name': 'not configured',
            'gpio': 9,
            'direction': 'input',
            'enabled': False,
            'excluded': '0',
            'pwm': 50,
            'frequency': 500
        },
        '6': {
            'name': 'not configured',
            'gpio': 22,
            'direction': 'input',
            'enabled': False,
            'excluded': '0',
            'pwm': 50,
            'frequency': 500
        },
        '7': {
            'name': 'not configured',
            'gpio': 27,
            'direction': 'input',
            'enabled': False, 'excluded': '0',
            'pwm': 50,
            'frequency': 500
        },
        '8': {
            'name': 'not configured',
            'gpio': 17,
            'direction': 'input',
            'enabled': False,
            'excluded': '0',
            'pwm': 50,
            'frequency': 500
        },
        '9': {
            'name': 'Laser Driver',
            'gpio': 18,
            'direction': 'output pwm',
            'enabled': True,
            'excluded': '0',
            'pwm': 5,
            'frequency': 500
        },
        '10': {
            'name': 'not configured',
            'gpio': 23,
            'direction': 'output',
            'enabled': False,
            'excluded': '0',
            'pwm': 50,
            'frequency': 500
        },
        '11': {
            'name': 'Door LED',
            'gpio': 24,
            'direction': 'output',
            'enabled': True,
            'excluded': '0',
            'pwm': 50,
            'frequency': 500
        },
        '12': {
            'name': 'Laser Warning LED',
            'gpio': 25,
            'direction': 'output pwm',
            'enabled': True,
            'excluded': '0',
            'pwm': 25,
            'frequency': 2
        },
        '13': {
            'name': 'Key Switch',
            'gpio': 12,
            'direction': 'input',
            'enabled': True,
            'excluded': '0',
            'pwm': 50,
            'frequency': 500
        },
        '14': {
            'name': 'Door Switch',
            'gpio': 16,
            'direction': 'input',
            'enabled': True,
            'excluded': '0',
            'pwm': 50,
            'frequency': 500
        },
        '15': {
            'name': 'not configured',
            'gpio': 20,
            'direction': 'input',
            'enabled': False,
            'excluded': '0',
            'pwm': 50,
            'frequency': 500
        },
        '16': {
            'name': 'Laser Enable',
            'gpio': 21,
            'direction': 'output',
            'enabled': True,
            'excluded': '0',
            'pwm': 50,
            'frequency': 500
        }
    },
    'serial_channels': [
        {
        'api-name': 'pyrometer',
        'baud': 115200,
        'messages': [
            {
            'api-command': '',
            'length': 0,
            'name': 'Pyrometer laser',
            'start': 0,
            'string1': 'JQ==',
            'string2': ''
            },
            {
                'api-command': 'pyrolaser-off',
                'length': 0,
                'name': 'pyrometer laser off',
                'start': 0,
                'string1': 'pQCl',
                'string2': ''
            },
            {
                'api-command': 'pyrolaser-on',
                'length': 0,
                'name': 'pyro laser off',
                'start': 0,
                'string1': 'pQGk',
                'string2': ''
            },
            {
                'api-command': '',
                'length': 0,
                'name': 'temperature',
                'start': 0,
                'string1': 'AQ==',
                'string2': ''
            }
        ],
        'mode': 'interactive',
        'poll_interval': 5,
        'port': '/dev/ttyUSB0'
        }
    ],
    'camera-qty': 2,
    'camera0': {
        'cameraBrightness': 128,
        'cameraContrast': 148,
        'cameraFPS': 5,
        'cameraGain': 0,
        'cameraGamma': 4,
        'cameraHeight': 640,
        'cameraHue': -40,
        'cameraID': 0,
        'cameraSaturation': 90,
        'cameraSharpness': 15,
        'cameraWidth': 480
        },
    'camera1': {
        'cameraBrightness': 64,
        'cameraContrast': 32,
        'cameraFPS': 5,
        'cameraGain': 50,
        'cameraGamma': 100,
        'cameraHeight': 640,
        'cameraHue': 0,
        'cameraID': 2,
        'cameraSaturation': 64,
        'cameraSharpness': 0,
        'cameraWidth': 480
        },
    'pyro-running-average': 5,
    'pyro-min-temp': 385,
    'laser-maxtime': 300,
    'app-name': 'Laser Controller'
}

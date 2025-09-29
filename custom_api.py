"""
A module for managing custom API commands and parsing incoming commands.

This module defines a mechanism to handle custom commands that are listed in
the `custom_api` list. If the commands are unknown or errors are encountered
during the parsing process, appropriate error logging and responses are
generated.
"""

from logmanager import logger
from laser_class import laser
from pyrometer_class import pyrometer


custom_api = ['digitalstatus', 'xserialstatus', 'laser_status', 'laser', 'set_laser_power', 'set_laser_timeout','get_temperature', 'reset_max','pyro_laser']

def custom_parser (item, command):
    """custom api commands, the items must be listed in the custom_api list for these to be called"""
    try:
        if item == 'laser':
            return laser.laser_on_off(item, command)
        if item == 'laser_status':
            return laser.laser_status(item, command)
        if item == 'set_laser_power':
            return laser.set_laser_power(item, command)
        if item == 'set_laser_timeout':
            return laser.laser_set_maxtime(item, command)
        if item == 'digitalstatus':
            return laser.http_status_data(item, command)
        if item == 'get_temperature':
            return pyrometer.get_temperatures(item, command)
        if item == 'reset_max':
            return pyrometer.reset_max(item, command)
        if item == 'pyro_laser':
            return pyrometer.laser_on_off(item, command)
        logger.warning('unknown item %s command %s', item, command)
        return {'error': 'unknown custom api command'}
    except ValueError:
        logger.error('Custom API Parser incorrect json message, value error')
        return {'error': 'bad value in json message custom api'}
    except IndexError:
        logger.error('Custom API Parser incorrect json message, index error')
        return {'error': 'Bad index in json message custom api'}

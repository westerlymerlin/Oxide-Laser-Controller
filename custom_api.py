"""
A module for managing custom API commands and parsing incoming commands.

This module defines a mechanism to handle custom commands that are listed in
the `custom_api` list. If the commands are unknown or errors are encountered
during the parsing process, appropriate error logging and responses are
generated.
"""

from logmanager import logger
from laser_class import laser


custom_api = ['digitalstatus', 'laserstatus', 'laser', 'setlaserpower', 'setlasertimeout','gettemperature', 'resetmax','pyrolaser']

def custom_parser (item, command):
    """custom api commands, the items must be listed in the custom_api list for these to be called"""
    try:
        if item == 'laser':
            return laser.laser_on_off(item, command)
        if item == 'laserstatus':
            return laser.laser_status(item, command)
        if item == 'setlaserpower':
            return laser.set_laser_power(item, command)
        if item == 'setlasertimeout':
            return laser.laser_set_maxtime(item, command)
        if item == 'digitalstatus':
            return laser.http_status_data(item, command)
        logger.warning('unknown item %s command %s', item, command)
        return {'error': 'unknown custom api command'}
    except ValueError:
        logger.error('Custom API Parser incorrect json message, value error')
        return {'error': 'bad value in json message custom api'}
    except IndexError:
        logger.error('Custom API Parser incorrect json message, index error')
        return {'error': 'Bad index in json message custom api'}

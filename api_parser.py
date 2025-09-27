"""
API Parser Module

This module provides functionality for parsing and handling API control commands
related to application settings.

The module serves as an interface between API requests and the application's
configuration system, validating inputs and handling potential errors during
the parsing process.

Functions:
    parsecontrol: Process API control commands and return appropriate responses

Dependencies:
    app_control: For accessing and writing application settings
    logmanager: For logging activities and errors
"""

from app_control import settings
from config_class import (set_appname, get_netifo, set_netinfo, updatesetting, restart_services,
                          set_analogue_settings, set_digital_settings)
from digital_class import digital_all_values, check_digital_key, digital_single_channel
from analogue_class import analogue_all_values, check_analogue_key, analogue_single_channel
from serial_class import (update_serial_channel, update_serial_message, delete_serial_message,
                          serial_http_data, serial_api_checker, serial_api_parser)
from logmanager import logger
from custom_api import custom_api, custom_parser

# pylint: disable=too-many-return-statements
def parsecontrol(item, command):
    """
    Processes the given command for a specific item and returns the result of the operation.

    The function identifies the type of item and executes the corresponding command or operation.
    Based on the provided item and command data, it processes actions such as setting
    channel states, retrieving or setting network information, updating settings, managing OLED status,
    and much more. If an unknown item or command is provided, it logs the issue and responds
    with an error message.
    """
    try:
        if item in custom_api:
            return custom_parser(item, command)
        if item == 'serialstatus':
            return serial_http_data(False, False)
        if item == 'digitalstatus':
            return digital_all_values(False, False)
        if item == 'analoguestatus':
            return analogue_all_values(False, False, command)
        if check_digital_key(item):  # read status of a digital channel
            return digital_single_channel(item, command)
        if item == '%sstatus' % settings['digital_prefix']:
            return digital_all_values(item, command)
        if check_analogue_key(item):  # read status of an analogue channel
            return analogue_single_channel(item, command)
        if item == '%sstatus' % settings['analogue_prefix']:
            return analogue_all_values(item, command)
        if serial_api_checker(item):
            return serial_api_parser(item, command)
        if item == 'getnetinfo':
            return get_netifo()
        if item == 'update_serial_channel':
            return update_serial_channel(command)
        if item == 'update_serial_message':
            return update_serial_message(command)
        if item == 'delete_serial_message':
            return delete_serial_message(command)
        if item == 'setnetinfo':
            mode = command['ipv4.method']
            ip_addr = command['IP4.ADDRESS']
            nwclass = command['IP4.SUBNET']
            df_gw = command['IP4.GATEWAY']
            dns_server = command['IP4.DNS']
            return set_netinfo(mode, ip_addr, nwclass, df_gw, dns_server)
        if item == 'setappname':
            return set_appname(command)
        if item == 'set_oled':
            if 'oled-enabled' in command.keys():
                updatesetting({'oled_enabled': True})
            else:
                updatesetting({'oled_enabled': False})
            restart_services()
            return {'success': 'services restarted'}
        if item == 'updatesetting':
            updatesetting(command)
            restart_services()
            return settings
        if item == 'getsettings':
            return settings
        if item == 'analogue_settings':
            return set_analogue_settings(command)
        if item == 'digital_settings':
            return set_digital_settings(command)
        logger.warning('unknown item %s command %s', item, command)
        return {'error': 'unknown api command'}
    except ValueError:
        logger.error('API Parser incorrect json message, value error')
        return {'error': 'bad value in json message'}
    except IndexError:
        logger.error('API Parser incorrect json message, index error')
        return {'error': 'Bad index in json message'}

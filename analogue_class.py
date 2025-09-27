"""
Initializes and manages analogue-to-digital converter functionality.

This module provides functions to initialize and configure the analogue-to-digital
converter (ADC) interface, fetch individual or collective input channel values, and
validate analogue channel keys. The module ensures compatibility with ADC devices
by dynamically checking their presence and functionality at runtime.
"""
from app_control import settings
from logmanager import logger
if settings['analogue_installed']:
    import board
    from adafruit_ads1x15.ads1115 import ADS1115
    from adafruit_ads1x15.analog_in import AnalogIn



analogue_channels={}
for interface in range(1, 5):
    analogue_channels[interface] = settings['analogue_channels'][str(interface)]

ADC_DEVICE = None

def init_analogue():
    """
    Initializes the analogue interface by setting up the I2C connection and
    checking for the presence of the analogue to digital converter (ADC).

    This function determines if the analogue interface is installed and operational.
    It scans for connected I2C devices and logs whether the analogue to digital
    converter (ADC) is successfully connected at the specified address.
    If the ADC is not found, the 'analogue_installed' setting is updated to False,
    and a warning is logged.

    """
    if settings['analogue_installed']:
        global ADC_DEVICE
        i2c = board.I2C()
        output = i2c.scan()
        if len(output) > 0:
            logger.info('i2c device found at address: %s', output)
            if settings['analogue_i2c'] in output:
                ADC_DEVICE = ADS1115(i2c, address=settings['analogue_i2c'])
                logger.info('Analogue to digital convertor connected')
                return
        settings['analogue_installed'] = False
        logger.warning('Analogue to digital convertor not found')


def check_analogue_key(item):
    """
    Check if the given item matches a digital key based on a predefined prefix.

    This function iterates through a range of identifiers and checks if the
    provided item matches a specific format comprising a digital prefix and an
    identifier value. If a match is found, it returns True. Otherwise, it
    returns False.

    """
    for item_id in range(1, 5):
        if item == '%s%d' % (settings['analogue_prefix'], item_id):
            return True
    return False

def analogue_single_channel(item, command):
    """
    Executes a single analogue channel operation by evaluating the provided channel and command. This function
    validates if the analogue-to-digital converter is installed and performs the necessary operation to fetch
    the voltage value from the specified channel.

    Warns if the analogue-to-digital converter is not installed, or if the specified channel is not enabled.
    Returns the operation status with voltage information where applicable.
    """
    if not settings['analogue_installed']:
        logger.warning('Analogue to digital convertor not installed')
        return {'status': 'error'}
    intchannel = int(item[len(settings['analogue_prefix']):])
    if analogue_channels[intchannel]['enabled']:
        #pylint: disable=used-before-assignment
        chan = AnalogIn(ADC_DEVICE, analogue_channels[intchannel]['pin'])
        voltage = chan.voltage
        return {'item': item, 'command': command, 'values': {'%s%d' % (settings['analogue_prefix'], intchannel):
                                                                 {'value': voltage,
                                                                  '%s' % settings['analogue_prefix']: intchannel }}}
    logger.warning('Analogue channel %d not enabled',intchannel)
    return {'item': item, 'command': command, 'values': {'%s%d' % (settings['analogue_prefix'], intchannel):
                                                             {'value': '',}}, 'exception': 'Channel not enabled'}


def analogue_all_values(item, command, log_error=True):
    """
    Retrieve current analogue input values for all configured channels.

    This function checks if the analogue-to-digital converter (ADC) is installed,
    and if it is, gathers the voltage readings from enabled analogue channels.
    If a channel is disabled, its status will be set to -1. If the ADC is not installed,
    the function logs a warning and returns a status indicating its unavailability.
    """
    if not settings['analogue_installed']:
        if log_error:
            logger.warning('Analogue to digital convertor not installed')
        return {'item': item, 'command': command, 'values': '', 'exception': 'ADC not installed'}
    values = {}
    for i in range(1, 5):
        if analogue_channels[i]['enabled']:
            chan = AnalogIn(ADC_DEVICE, analogue_channels[i]['pin'])
            voltage = chan.voltage
            values['%s%d' % (settings['analogue_prefix'], i)] = {'value': voltage, '%s' % settings['analogue_prefix']: i,
                                                             'enabled': analogue_channels[i]['enabled'],
                                                             'name': analogue_channels[i]['name']}
    return {'item': item, 'command': command, 'values': values}

init_analogue()

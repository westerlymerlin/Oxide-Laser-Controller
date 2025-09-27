"""
OLED Display Module for Raspberry Pi

This module provides functionality to display system information on an OLED display
connected to a Raspberry Pi via I2C. It shows the application name, version number,
and network interface information (IP addresses and subnet masks).

Dependencies:
- Adafruit SSD1306 library
- PIL (Python Imaging Library)
- board module
- config_class module for IP address retrieval
- app_control module for application settings

Hardware:
- Designed for a 0.91" OLED display (128x64 pixels) with SSD1306 controller
- Uses I2C interface with address 0x3C

Usage:
    from oledclass import set_oled
    set_oled()  # Updates the OLED display with current system information
"""

from config_class import get_netifo
from app_control import settings, VERSION
from logmanager import logger
if settings['oled_enabled']:
    import board
    from PIL import Image, ImageDraw, ImageFont
    import adafruit_ssd1306

def set_oled():
    """
    Sets up and initializes an OLED display and configures it to show text
    output, such as the application name, its version, and IP address information.
    """
    if settings['oled_enabled']:  # skip if oled is not enabled
        try:
            i2c = board.I2C()
            oled = adafruit_ssd1306.SSD1306_I2C(settings['oled_width'], settings['oled_height'], i2c, addr=settings['oled_address'])
        except ValueError:
            logger.error('OLED display not found at %s', settings['oled_address'])
            return
        except NameError:
            logger.info('Board libary not loaded - OLED not available ')
            return

        # Create blank image for drawing.
        # Make sure to create image with mode '1' for 1-bit color.
        image = Image.new("1", (oled.width, oled.height))

        # Get drawing object to draw on image.
        draw = ImageDraw.Draw(image)

        # Load default font.
        font = ImageFont.load_default(11)

        # Draw Text Image
        netif = get_netifo()
        if len(settings['app-name']) > 16:
            text = settings['app-name'][:15] + '...'
        else :
            text = settings['app-name']
        text = text + '\nVER: ' + VERSION
        try:
            text = text + '\n%s: %s' % (netif['connection.interface-name'],
                                    netif['IP4.ADDRESS[1]'].split('/', maxsplit=1)[0])
        except KeyError:
            text = text + '\nNo network connection'
        draw.text( (1, 1), text, font=font, fill=255)

        # Display image
        oled.image(image)
        oled.show()

if __name__ == "__main__":
    set_oled()

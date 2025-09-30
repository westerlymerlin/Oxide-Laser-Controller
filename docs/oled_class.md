# None

<a id="oled_class"></a>

# oled\_class

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

<a id="oled_class.get_netifo"></a>

## get\_netifo

<a id="oled_class.settings"></a>

## settings

<a id="oled_class.VERSION"></a>

## VERSION

<a id="oled_class.logger"></a>

## logger

<a id="oled_class.set_oled"></a>

#### set\_oled

```python
def set_oled()
```

Sets up and initializes an OLED display and configures it to show text
output, such as the application name, its version, and IP address information.


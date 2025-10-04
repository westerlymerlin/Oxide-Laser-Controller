# Module Documentation


This document contains the documentation for all the modules in this project.

---

## Contents


[analogue_class](./analogue_class.md)  
Initializes and manages analogue-to-digital converter functionality.

This module provides functions to initialize and configure the analogue-to-digital
converter (ADC) interface, fetch individual or collective input channel values, and
validate analogue channel keys. The module ensures compatibility with ADC devices
by dynamically checking their presence and functionality at runtime.

[api_parser](./api_parser.md)  
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

[app](./app.md)  
Flask web application for Raspberry Pi system monitoring and control.

This module provides a web interface and API endpoints for monitoring and controlling
a Raspberry Pi system. It includes features for:
- System status monitoring (CPU temperature, running threads)
- Log viewing (Application, Gunicorn, System logs)
- RESTful API endpoints with authentication
- Real-time status updates via JavaScript

The application runs on Gunicorn when deployed on Raspberry Pi and includes
various endpoints for both web interface and programmatic access.

Routes:
    / : Main status page
    /statusdata : JSON endpoint for live status updates
    /api : Protected API endpoint for system control
    /pylog : Application log viewer
    /guaccesslog : Gunicorn access log viewer
    /guerrorlog : Gunicorn error log viewer
    /syslog : System log viewer

Authentication:
    API endpoints require a valid API key passed in the 'Api-Key' header.

[app_control](./app_control.md)  
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

[camera_class](./camera_class.md)  
A module for managing video camera streams and configurations.

This module provides the `VideoCameraObject` class, which implements functionalities for initializing video
camera streams, obtaining frames, and encoding them for streaming. The module leverages `cv2` for video
capture and incorporates adjustable properties for various camera settings such as resolution, FPS,
brightness, contrast, and more. Logging is used for monitoring camera actions and configurations.

[config_class](./config_class.md)  
Application Configuration

This module provides utilities for managing system configuration, network settings, and application naming.
It serves as the core configuration interface for the Raspberry Pi control application, handling both
network interfaces and application identity management.

Key Features:
    - Network configuration: Get and set network interface settings (DHCP/static)
    - IP address validation: Verify IP addresses and network class formats
    - Application naming: Manage application names with automatic sanitization
    - System hostname: Update system hostname based on application name

Functions:
    friendlydirname(sourcename): Sanitizes strings by removing invalid characters
    get_netifo(): Retrieves network configuration information
    validate_ipaddress(ip_str): Validates IPv4 address format
    validate_class(class_str): Validates network class (1-32)
    set_netinfo(mode, ip_addr, nwclass, df_gw, dns_server): Configures network interface
    set_appname(name): Updates application name in settings and system hostname

Dependencies:
    subprocess: For executing system commands
    re: For regex pattern matching
    app_control: For settings management
    logmanager: For logging configuration changes

[custom_api](./custom_api.md)  
A module for managing custom API commands and parsing incoming commands.

This module defines a mechanism to handle custom commands that are listed in
the `custom_api` list. If the commands are unknown or errors are encountered
during the parsing process, appropriate error logging and responses are
generated.

[custom_settings](./custom_settings.md)  
A module for storing and managing configuration or custom settings.

This module provides a dictionary named `custom_settings` that can be
used to define and store custom configuration or settings. These settings
can be used across different parts of an application.

Attributes:
    custom_settings (dict): A dictionary to hold custom configuration
    settings, which can be set and accessed dynamically within the
    application.

[digital_class](./digital_class.md)  
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

[laser_class](./laser_class.md)  
Module for controlling and monitoring a LaserTree K60 450nm laser system.

This module interacts with GPIO channels on a Raspberry Pi to manage the laser system,
including interlocks for door and key switch states. It contains utility to monitor
hardware statuses and perform necessary operations, such as enabling and disabling
the laser based on safety conditions.

The laser power is managed by pulse width modulation (PWM) output on a digital channel.
The laser is automatically turned off after a specified timeout period if it is not
shut down by API control.

[logmanager](./logmanager.md)  
Logging Configuration and Management

This module provides centralized logging configuration and management for the application.
Configures logging formats, handlers, and log file management to ensure consistent
logging across all application components.

Features:
    - Standardized log formatting
    - File-based logging with rotation
    - Log level management
    - Thread-safe logging operations

Exports:
    logger: Configured logger instance for use across the application

Usage:
    from logmanager import logger

    logger.info('Operation completed successfully')
    logger.warning('Resource threshold reached')
    logger.error('Failed to complete operation')

Log Format:
    Timestamps, log levels, and contextual information are automatically included
    in each log entry for effective debugging and monitoring.

Log Files:
    Logs are stored with automatic rotation to prevent excessive disk usage
    while maintaining historical records.

Author: Gary Twinn

[oled_class](./oled_class.md)  
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

[pyrometer_class](./pyrometer_class.md)  
Module for managing operations of a Micro Epsilon Infrared Pyrometer.

This module contains the `PyrometerObject` class which encapsulates various
pyrometer operations including temperature readings, managing rangefinder laser control,
and tracking the running average and maximum temperature.

[serial_class](./serial_class.md)  
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

Usage:
    The module automatically initializes all configured serial channels on import.
    Channels can be managed through the configuration functions, and data can be
    accessed via the serial_http_data() function or individual channel instances.


---


  
-------
#### Copyright (C) 2025 Gary Twinn  

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.  
  
You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.  
  
  ##### Author: Gary Twinn  
  
 -------------
  

# Module Documentation


This document contains the documentation for all the modules in the **Oxide Line Laser Controller** version 1.5.1 application.

---

## Contents


[app](./app.md)  
Laser Processing System Main Application

This module serves as the main entry point and coordinator for the laser processing system,
integrating various components including laser control, temperature monitoring, camera
operations, and user interface management.

Core Components:
    - System initialization and shutdown procedures
    - Hardware component coordination (laser, pyrometer, camera)
    - Safety monitoring and emergency shutdown handling
    - User interface event handling
    - Settings management and validation
    - Process logging and monitoring

Application Flow:
    1. System initialization and hardware checks
    2. User interface setup
    3. Component coordination (laser, pyrometer, camera)
    4. Process monitoring and control
    5. Safe shutdown procedures

Dependencies:
    - laserclass: Laser control interface
    - pyroclass: Temperature monitoring
    - camera: Image capture and processing
    - app_control: Settings management
    - logmanager: System logging

Usage:
    python app.py

[app_control](./app_control.md)  
Application Settings Management

This module handles the application's configuration settings, providing functionality
to read, write, and manage persistent application settings. It maintains centralized
control over configuration parameters used across the application.

Exports:
    settings: Dictionary containing application configuration parameters
    writesettings(): Function to persist settings changes to storage

Usage:
    from app_control import settings, writesettings

    # Read settings
    current_power = settings['power']

    # Modify and persist settings
    settings['power'] = new_value
    writesettings()

[camera](./camera.md)  
Camera Control and Image Capture

This module provides functionality for controlling and capturing images from a camera device.
Handles camera setup, configuration, image acquisition, and cleanup operations.

Features:
    - Camera initialization and configuration
    - Image capture and storage
    - Camera parameter adjustments (exposure, resolution, etc.)
    - Resource management (proper camera shutdown)

Usage Example:
    from camera import Camera

    camera = Camera()
    camera.capture('image.jpg')
    camera.close()

The module is designed for use with hardware camera interfaces and ensures proper
resource handling for stable operation in long-running applications.

Dependencies:
    Hardware: Compatible camera device
    Software: Appropriate camera drivers/libraries

[laserclass](./laserclass.md)  
Laser Control System Implementation

This module provides a comprehensive interface for controlling and monitoring a laser system
through GPIO pins on a Raspberry Pi. It implements safety features including door interlocks,
key switch monitoring, and automatic timeout protection.

Key Features:
- Laser power control via PWM (Pulse Width Modulation)
- Safety interlocks monitoring (door and key switch)
- Automatic laser shutdown after configurable timeout
- Real-time status monitoring and reporting
- Temperature monitoring via pyrometer integration
- Settings persistence and management

Classes:
    LaserClass: Main class for laser control and monitoring

Functions:
    updatesetting: Updates system settings
    parsecontrol: Main API entry point for laser control
    reboot: System reboot functionality

Dependencies:
    - RPi.GPIO: For GPIO control
    - time: For timing operations
    - threading: For background monitoring
    - app_control: For settings management
    - pyroclass: For temperature monitoring
    - logmanager: For system logging

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

[pyroclass](./pyroclass.md)  
Pyrometer Interface and Temperature Monitoring

This module implements the interface for pyrometer temperature measurements,
providing real-time temperature monitoring and data handling capabilities for
laser processing applications.

Features:
    - Pyrometer communication and initialization
    - Real-time temperature reading and monitoring
    - Temperature data processing and validation
    - Error handling for sensor communication
    - Temperature threshold monitoring

Classes:
    Pyrometer: Main class for pyrometer operations and temperature management

Usage:
    from pyroclass import Pyrometer

    pyro = Pyrometer()
    current_temp = pyro.get_temperature()

    # Monitor temperature with safety thresholds
    pyro.start_monitoring(max_temp=1200)

Hardware Requirements:
    - Compatible pyrometer sensor
    - Serial/USB communication interface

Note:
    Temperature readings are provided in degrees Celsius.
    Ensure proper pyrometer calibration before use in production environment.


---


# UCL-Oxide-Laser-Controller

A Python application for controlling a LaserTree K60 Laser and micro-epsilon infrared pyrometer systems via HTTP API.

## Overview

This project provides a Flask-based API for precise control of laser and temperature measurement equipment used in oxide research. The system uses CH-340 USB to RS232 adapters for communication with the hardware devices.

## Documentation

- **Setup Instructions**: Detailed setup information is available in [manual.pdf](./manual.pdf)
- **API Reference**: Python module documentation in the [docs](./docs/readme.md) folder
- **Change Log**: View version history in [changelog.txt](./changelog.txt)

## System Architecture

The main application entry point is `app.py`, which implements the Flask application that manages the HTTP API.

## API Reference

The system accepts JSON commands via its HTTP interface:

| Command | Format | Description |
|---------|--------|-------------|
| Laser Control | `{"laser": "off"}` | Switch off the laser |
| | `{"laser": "on"}` | Switch on the laser |
| | `{"setlaserpower": nn.n}` | Set laser power to nn.n% |
| | `{"laserstatus": 1}` | Read laser status (returns power and firing state) |
| | `{"setlasertimeout": nnn}` | Change maximum laser firing time to nnn seconds (default: 300) |
| Temperature Monitoring | `{"gettemperature": 1}` | Return pyrometer temperature and maximum attained temperature |
| | `{"resetmax": 1}` | Reset the maximum pyrometer temperature reading |
| Rangefinder Control | `{"pyrolaser": "off"}` | Switch off the rangefinder laser |
| | `{"pyrolaser": "on"}` | Switch on the rangefinder laser |
| System Control | `{"restart": "pi"}` | Restart the Raspberry Pi after a 15 second delay |



# TST Base Controller Service

A Flask-based web application for Raspberry Pi that provides system monitoring, equipment control, and a RESTful API interface for scientific equipment management.

## Features

- **Web Interface**: Browser-based dashboard for system monitoring and configuration
- **RESTfull API**: JSON-based API with authentication for programmatic control
- **System Monitoring**: Real-time CPU temperature, thread monitoring, and system status
- **Equipment Control**: Digital and analogue device control via GPIO
- **OLED Display**: Shows system information including network address and software version
- **Log Management**: Comprehensive logging with web-based log viewers
- **Configuration Management**: Web-based configuration interface for system settings

## Documentation
- **User Manual**: [manual.pdf](./manual.pdf)
- **API Documentation**: [docs/readme.md](./docs/readme.md)
- **Change Log**: [changelog.txt](./changelog.txt)


### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api` | POST | Main API endpoint for equipment control |



### API Commands

Send JSON payloads with the following structure:
```
json { "item": "command_type", "command": "command_parameters" }
```

### Example Commands


#### Read Digital Channels:
``` 
json {
  "item": "digitalstatus",
  "command": false
}
```
#### Read Analogue Channels:
```
json {
  "item": "analoguestatus", 
  "command": false
}
```
## Configuration
The application supports web-based configuration for:
- Network settings
- OLED display settings
- Digital device settings
- Analogue device settings
- Log levels
- Application hostname

### Project Structure
``` 
├── app.py              # Main Flask application
├── app_control.py      # Application control logic
├── api_parser.py       # API command parsing
├── digital_class.py    # Digital GPIO control
├── analogue_class.py   # Analogue device control
├── oled_class.py       # OLED display management
├── logmanager.py       # Logging configuration
├── config_class.py     # Configuration management
├── templates/          # HTML templates
├── static/             # CSS, JS, and static assets
├── docs/               # Additional documentation
└── raspberry-pi/       # Raspberry Pi specific files
```


## Monitoring
The system provides comprehensive monitoring including:
- CPU temperature monitoring
- Active thread tracking
- Real-time status updates via JavaScript
- Multiple log file access (Application, Gunicorn, System)

## License
Copyright (C) 2025 Gary Twinn
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/).

## Author
**Dr Gary Twinn**  
GitHub: [github.com/westerlymerlin](https://github.com/westerlymerlin)



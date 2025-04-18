# UCL-Oxide-Laser-Controller


### Python project to control a LaserTree K60 Laser and a micro-epsilon infrared pyrometer, is controlled via an HTTP API

Functional description and setup instructions are available in the file: [README.pdf](./README.pdf)
It uses CH-340 USB to RS232 adapters for comms. 

Application dcumentaton can be found in [readme.pdf](./readme.pdf)

Python module documentation can be found in the folder: [docs](./docs/readme.md)

Change log can be found in the file [changelog.txt](./changelog.txt)

`app.py`			    Flask application that manages the API 

---


### JSON Commands
| Command                    | Description                                                                    |
|----------------------------|--------------------------------------------------------------------------------|
| `{"laser": "off"}`         | Switch off the laser                                                           |  
| `{"laser": "on"}`          | Switch on the laser                                                            |
| `{"setlaserpower": nn.n}`  | set the laser power to nn.n%                                                   | 
| `{"laserstatus": 1}`       | Read the laser status (returns power and if the laser is firing)               | 
| `{"setlasertimeout": nnn}` | change the default maximum time the laser can fire to nnn seconds (default is 300) | 
| `{'gettemperature', 1}` | Return the pyrometer temperature and maximum attained temperature              | 
| `{'resetmax', 1}` | Reset the maximum pyrometer temperature reading                                |  
| `{'pyrolaser', 'off'}` | Switch off the rangefinder laser                                               | 
| `{'pyrolaser', 'on'}` | Switch on the rangefinder laser                                                |
| `{"restart": "pi"}` | Restart the rsapberry pi after a 15 second delay                               |


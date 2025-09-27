# None

<a id="api_parser"></a>

# api\_parser

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

<a id="api_parser.settings"></a>

## settings

<a id="api_parser.set_appname"></a>

## set\_appname

<a id="api_parser.get_netifo"></a>

## get\_netifo

<a id="api_parser.set_netinfo"></a>

## set\_netinfo

<a id="api_parser.updatesetting"></a>

## updatesetting

<a id="api_parser.restart_services"></a>

## restart\_services

<a id="api_parser.set_analogue_settings"></a>

## set\_analogue\_settings

<a id="api_parser.set_digital_settings"></a>

## set\_digital\_settings

<a id="api_parser.digital_all_values"></a>

## digital\_all\_values

<a id="api_parser.check_digital_key"></a>

## check\_digital\_key

<a id="api_parser.digital_single_channel"></a>

## digital\_single\_channel

<a id="api_parser.analogue_all_values"></a>

## analogue\_all\_values

<a id="api_parser.check_analogue_key"></a>

## check\_analogue\_key

<a id="api_parser.analogue_single_channel"></a>

## analogue\_single\_channel

<a id="api_parser.update_serial_channel"></a>

## update\_serial\_channel

<a id="api_parser.update_serial_message"></a>

## update\_serial\_message

<a id="api_parser.delete_serial_message"></a>

## delete\_serial\_message

<a id="api_parser.serial_http_data"></a>

## serial\_http\_data

<a id="api_parser.serial_api_checker"></a>

## serial\_api\_checker

<a id="api_parser.serial_api_parser"></a>

## serial\_api\_parser

<a id="api_parser.logger"></a>

## logger

<a id="api_parser.custom_api"></a>

## custom\_api

<a id="api_parser.custom_parser"></a>

## custom\_parser

<a id="api_parser.parsecontrol"></a>

#### parsecontrol

```python
def parsecontrol(item, command)
```

Processes the given command for a specific item and returns the result of the operation.

The function identifies the type of item and executes the corresponding command or operation.
Based on the provided item and command data, it processes actions such as setting
channel states, retrieving or setting network information, updating settings, managing OLED status,
and much more. If an unknown item or command is provided, it logs the issue and responds
with an error message.


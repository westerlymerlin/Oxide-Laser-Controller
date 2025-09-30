# None

<a id="serial_class"></a>

# serial\_class

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

Dependencies:
    - pyserial: Core serial communication
    - threading: Background data acquisition
    - base64: Message encoding/storage
    - app_control: Configuration management
    - logmanager: Activity logging

Usage:
    The module automatically initializes all configured serial channels on import.
    Channels can be managed through the configuration functions, and data can be
    accessed via the serial_http_data() function or individual channel instances.

<a id="serial_class.literal_eval"></a>

## literal\_eval

<a id="serial_class.sleep"></a>

## sleep

<a id="serial_class.Timer"></a>

## Timer

<a id="serial_class.b64decode"></a>

## b64decode

<a id="serial_class.b64encode"></a>

## b64encode

<a id="serial_class.datetime"></a>

## datetime

<a id="serial_class.glob"></a>

## glob

<a id="serial_class.sys"></a>

## sys

<a id="serial_class.serial"></a>

## serial

<a id="serial_class.logger"></a>

## logger

<a id="serial_class.settings"></a>

## settings

<a id="serial_class.writesettings"></a>

## writesettings

<a id="serial_class.friendlyname"></a>

## friendlyname

<a id="serial_class.jscriptname"></a>

## jscriptname

<a id="serial_class.str_encode"></a>

#### str\_encode

```python
def str_encode(string)
```

Encodes a given string to its Base64 representation.

This function takes a string and encodes it using Base64. The encoding
is performed by first converting the string to its byte representation
in UTF-8, then applying Base64 encoding to it, and finally decoding
the resulting bytes back into a string.

<a id="serial_class.str_decode"></a>

#### str\_decode

```python
def str_decode(string)
```

Decodes a Base64 encoded string into a UTF-8 string.

This function takes a string that is Base64 encoded, decodes it from
Base64, and then decodes the resulting bytes into a UTF-8 string.

<a id="serial_class.update_serial_channel"></a>

#### update\_serial\_channel

```python
def update_serial_channel(newsettings)
```

Updates the serial channel settings with given new settings.

This function updates the configuration for a serial channel with the provided
settings. If the serial channel with the same port already exists, it retains
existing messages while updating other parameters. Otherwise, it adds a new
serial channel to the configuration. The updated configuration is sorted by
the 'api-name' field before saving.

<a id="serial_class.delete_serial_channel"></a>

#### delete\_serial\_channel

```python
def delete_serial_channel(port_id)
```

Delete a serial communication channel matching the specified port.

This function takes in a port identifier and removes the corresponding serial
communication channel from the current settings. If a match is found for the
provided port, the channel is excluded, the updated list is saved back to the
settings, and a confirmation is logged. The function also returns the modified
list of channels.

<a id="serial_class.update_serial_message"></a>

#### update\_serial\_message

```python
def update_serial_message(newsettings)
```

Update and manage the serial message structure and settings.

This function takes a new set of serial message settings, encodes required
settings, updates the corresponding serial channel messages based on the
port, and writes the updated settings. It logs actions performed and
manages the organization of messages for a serial channel.

<a id="serial_class.delete_serial_message"></a>

#### delete\_serial\_message

```python
def delete_serial_message(newsettings)
```

Deletes a specific serial message from the configuration of a serial port.

This function iterates through the existing serial channels to remove a
message that matches the name and port specified in the provided settings.
After performing the deletion, the updated settings are saved, and an
informational log message is generated.

<a id="serial_class.serial_port_info"></a>

#### serial\_port\_info

```python
def serial_port_info(port_id)
```

Retrieve detailed information about a serial port configuration.

The function gathers and returns information about a serial port, such as its
API-friendly name, mode, baud rate, polling interval, and associated messages.
If the port is found in the existing serial channel settings, detailed
configuration for the port is retrieved; otherwise, default settings are used.

<a id="serial_class.serial_ports"></a>

#### serial\_ports

```python
def serial_ports()
```

Lists serial port names available on the system

:raises EnvironmentError:
    On unsupported or unknown platforms
:returns:
    A list of the serial ports available on the system

<a id="serial_class.SerialConnection"></a>

## SerialConnection Objects

```python
class SerialConnection()
```

Handles serial communication by initializing, configuring, and managing the serial
port connection. Provides functionality to interact with devices using a specific
communication protocol and read messages based on predefined listener configurations.

Designed for applications requiring consistent serial port communication, with support
for interactive and non-interactive (listener) modes. The class allows users to automate
polling of devices and processing of incoming data based on predefined configurations.

<a id="serial_class.SerialConnection.__init__"></a>

#### \_\_init\_\_

```python
def __init__(device)
```

<a id="serial_class.SerialConnection.init_port"></a>

#### init\_port

```python
def init_port()
```

Initialize the serial port with specified parameters. This method attempts to
establish a connection to the serial port using the given port and baud rate.
Upon successful initialization, the input buffer is reset and the port is
marked as ready. If the connection fails, the port is marked as not ready.

<a id="serial_class.SerialConnection.name"></a>

#### name

```python
def name()
```

Retrieves the value of the name attribute.

<a id="serial_class.SerialConnection.listener_timer"></a>

#### listener\_timer

```python
def listener_timer()
```

Reads data from a serial port in a loop with a specified polling interval. The behavior
differs based on the mode of operation ('listener' or otherwise). If in 'listener' mode,
it processes incoming data to extract specific substrings based on predefined message definitions.

<a id="serial_class.SerialConnection.api_command"></a>

#### api\_command

```python
def api_command(item, command)
```

Executes a specified API command by sending encoded data via a serial port and reads back the
response. The method will match the provided command with predefined messages, decode the
associated strings, and send them sequentially through the serial port. It returns the result of
the operation.

The method handles errors related to the serial port and returns a descriptive error message if
a SerialException occurs or if the serial port is not ready.

<a id="serial_class.SerialConnection.listener_values"></a>

#### listener\_values

```python
def listener_values()
```

Retrieves the current listener values.

This method provides access to the internal state of listener values used
in the class.

<a id="serial_class.SerialConnection.change_poll_interval"></a>

#### change\_poll\_interval

```python
def change_poll_interval(value)
```

Updates the poll interval to the specified value. Entering 0 returns to the default value

<a id="serial_class.serial_http_data"></a>

#### serial\_http\_data

```python
def serial_http_data(item, command)
```

Collects and aggregates all listener values from all channels into a single dictionary for the index page.

This function iterates through all the channels in `serial_channels` and processes their
listener values, creating a unified dictionary where each key is constructed using the port
and name of the message, and the corresponding value is the message itself.

<a id="serial_class.serial_api_parser"></a>

#### serial\_api\_parser

```python
def serial_api_parser(item, command)
```

Parses a serial API command and matches it to a corresponding serial channel.
Executes the parsed command or retrieves a channel-specific listener status.

<a id="serial_class.serial_channels"></a>

#### serial\_channels

<a id="serial_class.serial_api_checker"></a>

#### serial\_api\_checker

```python
def serial_api_checker(item)
```

Checks whether the given item matches the name of any serial channel.

This function iterates over all available serial channels and checks if the
provided item's prefix matches the name of any channel. If a match is found,
the function returns True, otherwise it returns False.


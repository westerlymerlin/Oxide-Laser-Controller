# None

<a id="digital_class"></a>

# digital\_class

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

<a id="digital_class.GPIO"></a>

## GPIO

<a id="digital_class.logger"></a>

## logger

<a id="digital_class.settings"></a>

## settings

<a id="digital_class.writesettings"></a>

## writesettings

<a id="digital_class.ChannelObject"></a>

## ChannelObject Objects

```python
class ChannelObject()
```

Represents a GPIO channel object for controlling and reading GPIO pins.

This class provides functionality to configure a GPIO channel for input or
output and read/write digital values. It also maintains details about the
channel, such as its current state, direction, and description.

<a id="digital_class.ChannelObject.__init__"></a>

#### \_\_init\_\_

```python
def __init__(channel_settings, channel_id)
```

Initializes a new instance of the GPIO configuration class.

This constructor sets up the configuration for a General Purpose Input/Output
(GPIO) pin, including its pin number, direction, whether it is enabled, and
additional descriptive attributes. These parameters define the behavior and
the state of the GPIO pin.

<a id="digital_class.ChannelObject.write"></a>

#### write

```python
def write(value)
```

Sets the digital channel to the specified value if it is enabled and configured
as an output channel. The value controls the GPIO state based on predefined
commands. Invalid values or improper configurations log warnings and result
in no changes.

:param value: The command to set the digital channel's GPIO (e.g., digital_on
              or digital_off commands).
:type value: str
:return: The current state of the GPIO after attempting to set it, or -1 if
         the operation fails due to a disabled channel, input configuration,
         or invalid value.
:rtype: int

<a id="digital_class.ChannelObject.read"></a>

#### read

```python
def read()
```

Reads the current state of the GPIO pin.

This method reads and returns the current logical state of the specified
GPIO pin. It uses the GPIO library to retrieve the input value, which
indicates whether the pin is logically HIGH or LOW.

:return: Logical state of the GPIO pin as returned by the GPIO library
:rtype: int or bool

<a id="digital_class.ChannelObject.change_setting"></a>

#### change\_setting

```python
def change_setting(setting, value)
```

Updates a specific setting for the current instance and persists the change.

This method modifies the attribute of the current instance with the provided
`setting` and `value`. It also updates the corresponding setting in the global
`settings` dictionary, ensuring that the digital channel's configuration is
consistently maintained. Finally, the settings are saved via the writesettings()
function, and a log entry is created indicating the updated settings.

<a id="digital_class.ChannelObject.info"></a>

#### info

```python
def info()
```

Constructs and returns a dictionary containing detailed information about the
current object instance.

The returned dictionary includes the identifier, name, direction, status of
the object (enabled/disabled), and its current value. If the direction is set
to 'output pwm', additional fields like pwm and frequency are also included.

<a id="digital_class.check_digital_key"></a>

#### check\_digital\_key

```python
def check_digital_key(item)
```

Check if the given item matches a digital key based on a predefined prefix.

This function iterates through a range of identifiers and checks if the
provided item matches a specific format comprising a digital prefix and an
identifier value. If a match is found, it returns True. Otherwise, it
returns False.

:param item: The item to be checked against the digital key format.
:type item: str
:return: A boolean indicating whether the given item matches the expected digital key format.
:rtype: bool

<a id="digital_class.digital_value"></a>

#### digital\_value

```python
def digital_value(value)
```

Convert a digital input value to its corresponding system-defined digital representation.

This function checks the given digital input value and returns the corresponding value
from the system's settings. If the input value does not match predefined digital states,
it will return 'error'.

:param value: The digital input value to evaluate.
:type value: int
:return: The system-defined digital value corresponding to the input or 'error' if the input
         is invalid.
:rtype: str

<a id="digital_class.digital_single_channel"></a>

#### digital\_single\_channel

```python
def digital_single_channel(item, command)
```

Executes a command to read or write the state of a single digital channel.

This function processes the input channel and state, determines the operation
to perform, and either reads the current channel state or updates the channel's
state based on the provided command. The function then returns the updated or
read channel state in a predefined format.

<a id="digital_class.digital_all_values"></a>

#### digital\_all\_values

```python
def digital_all_values(item, command)
```

Generates a json representation of digital values for configured digital channels.

This function iterates through a predefined range of digital channel IDs, retrieves
their respective metadata and status, and returns a dictionary containing the
digital channel attributes.

:return: A dictionary representing the digital channels' values, where the keys
         are prefixed with the configured digital prefix, and the values contain
         the channel's ID, name, direction, status, and whether it is enabled.
:rtype: dict

<a id="digital_class.digital_channels"></a>

#### digital\_channels


# None

<a id="pyrometer_class"></a>

# pyrometer\_class

Module for managing operations of a Micro Epsilon Infrared Pyrometer.

This module contains the `PyrometerObject` class which encapsulates various
pyrometer operations including temperature readings, managing rangefinder laser control,
and tracking the running average and maximum temperature.

<a id="pyrometer_class.Thread"></a>

## Thread

<a id="pyrometer_class.time"></a>

## time

<a id="pyrometer_class.sleep"></a>

## sleep

<a id="pyrometer_class.serial_channels"></a>

## serial\_channels

<a id="pyrometer_class.logger"></a>

## logger

<a id="pyrometer_class.settings"></a>

## settings

<a id="pyrometer_class.PyrometerObject"></a>

## PyrometerObject Objects

```python
class PyrometerObject()
```

This class is responsible for managing and interacting with a pyrometer device, which is used
to measure temperature and control a laser. It handles acquiring temperature data, maintaining
a moving average for temperature readings, resetting temperature limits, and managing laser
operations including a timeout mechanism for the laser.

The primary purpose of this class is to facilitate data acquisition, analysis, and control
mechanisms for the pyrometer system by utilizing predefined settings and external communication
modules for device interaction. It simplifies pyrometer operations through its interface
methods, ensuring accurate and efficient functioning in its operational environment.

<a id="pyrometer_class.PyrometerObject.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

Represents an entity for managing temperature and laser state attributes.

This class is responsible for storing and managing temperature-related
values and laser state information. It initializes its attributes based
on predefined settings.

<a id="pyrometer_class.PyrometerObject.pyrometer_updater"></a>

#### pyrometer\_updater

```python
def pyrometer_updater()
```

Continuously updates pyrometer data and moving average based on a defined polling interval.

<a id="pyrometer_class.PyrometerObject.read_pyrometer_data"></a>

#### read\_pyrometer\_data

```python
def read_pyrometer_data()
```

Calculates the temperature and laser state from the pyrometer data. The method processes
the serial listener values associated with the pyrometer channel. It extracts and decodes
the temperature and laser state values from the corresponding data entries and updates the class.

<a id="pyrometer_class.PyrometerObject.update_moving_average"></a>

#### update\_moving\_average

```python
def update_moving_average()
```

Updates the running average temperature and maintains tracking of the maximum average
temperature observed. The function adjusts the list of temperature readings depending
on the current temperature value and predetermined settings. It also calculates a new
average temperature from the updated list and compares it with the maximum average
temperature recorded so far.

<a id="pyrometer_class.PyrometerObject.reset_max"></a>

#### reset\_max

```python
def reset_max(item, command)
```

Resets the maximum and average maximum temperature to a predefined minimum value and updates
the temperature.

:return: The current temperature of the PyroClass after resetting maximum values
:rtype: Any

<a id="pyrometer_class.PyrometerObject.laser_on_off"></a>

#### laser\_on\_off

```python
def laser_on_off(item, command)
```

Controls the laser of the pyrometer by turning it on or off based on the
provided command. When the laser is turned on, a timer thread is initiated
to handle turning it off after a certain duration set in the settings file.

<a id="pyrometer_class.PyrometerObject.laser_off_timer"></a>

#### laser\_off\_timer

```python
def laser_off_timer()
```

Sets a timer to automatically turn off the laser after a specified maximum time is reached.

This method checks if the laser is currently on. If the laser is on, it calculates
a future time based on the current time and the maximum allowed time. The laser
will then be turned off after the calculated duration has passed.

<a id="pyrometer_class.PyrometerObject.get_temperatures"></a>

#### get\_temperatures

```python
def get_temperatures(item, command)
```

Retrieve temperature-related data.

This function gathers various temperature readings and additional state data,
returning them in a structured dictionary. The returned data includes information
on current temperature, average temperature, maximum recorded temperature,
average maximum recorded temperature, and the state of the rangefinder laser on the pyrometer.

<a id="pyrometer_class.PyrometerObject.change_poll_interval"></a>

#### change\_poll\_interval

```python
def change_poll_interval(value)
```

Updates the poll interval to the specified value. Entering 0 returns to the default value

<a id="pyrometer_class.pyrometer"></a>

#### pyrometer


# None

<a id="pyroclass"></a>

# pyroclass

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

<a id="pyroclass.Timer"></a>

## Timer

<a id="pyroclass.sleep"></a>

## sleep

<a id="pyroclass.time"></a>

## time

<a id="pyroclass.b64decode"></a>

## b64decode

<a id="pyroclass.serial"></a>

## serial

<a id="pyroclass.settings"></a>

## settings

<a id="pyroclass.logger"></a>

## logger

<a id="pyroclass.PyroClass"></a>

## PyroClass Objects

```python
class PyroClass()
```

This class represents a Pyrometer interface to communicate with a serial device.

The PyroClass establishes and manages communication with a pyrometer device
through a serial port. It handles initializing the pyrometer, reading temperature
values at regular intervals, maintaining a running average of temperature readings,
and controlling a laser rangefinder. Various utility functions are available for
interacting with the pyrometer's readings and laser control.

<a id="pyroclass.PyroClass.__init__"></a>

#### \_\_init\_\_

```python
def __init__(port, speed, readtemp, readlaser, laseron, laseroff)
```

<a id="pyroclass.PyroClass.close"></a>

#### close

```python
def close()
```

Closes the communication port associated with the PyroClass Pyrometer
object. This function ensures the port is properly closed and logs this
action. It also updates the `portready` status attribute to indicate
that the port is no longer active.

:raises AttributeError: If the `port` attribute or its methods are not
    properly initialized or accessible.
:raises IOError: If there is an issue with closing the port.

:return: None

<a id="pyroclass.PyroClass.readtimer"></a>

#### readtimer

```python
def readtimer()
```

Continuously reads temperature and laser data from a connected port while the
port is ready. The method writes specific commands to the port to request
temperature and laser information and processes the data returned.

When the port is not ready or there is an exception during data reading, the
temperature (`value`) is reset to 0. Temperature data is processed to calculate
statistics like `maxtemp` and optionally update an average temperature.

Potential logging operations are carried out at various points:
- To debug temperature and laser value read operations.
- To log any exceptions encountered during execution.

:raises Exception: Handles any exceptions during port communication, logs the
    exception, and ensures temperature value is reset to mitigate impact.

:param

:return: None

<a id="pyroclass.PyroClass.setaverage"></a>

#### setaverage

```python
def setaverage()
```

Updates the running average temperature and maintains tracking of the maximum average
temperature observed. The function adjusts the list of temperature readings depending
on the current temperature value and predetermined settings. It also calculates a new
average temperature from the updated list and compares it with the maximum average
temperature recorded so far.

:param self: An instance of the class containing attributes `value`, `tempseq`,
    `averagetemp`, and `averagemaxtemp`, which are necessary for the computation.
:return: None

<a id="pyroclass.PyroClass.resetmax"></a>

#### resetmax

```python
def resetmax()
```

Resets the maximum and average maximum temperature to a predefined minimum value and updates
the temperature.

:return: The current temperature of the PyroClass after resetting maximum values
:rtype: Any

<a id="pyroclass.PyroClass.laseron"></a>

#### laseron

```python
def laseron()
```

Turns the laser on by sending a command to the port, if the port is ready.
Additionally, it starts a timer thread to turn the laser off after 0.5 seconds.

:return: None

<a id="pyroclass.PyroClass.laseroff"></a>

#### laseroff

```python
def laseroff()
```

Turns off the laser by writing the appropriate command to the port if the port
is ready. Updates the laser status attribute accordingly.

:raises AttributeError: If a required attribute is not defined.
:param self: The instance of the object performing the action.
:return: None

<a id="pyroclass.PyroClass.laserofftimer"></a>

#### laserofftimer

```python
def laserofftimer()
```

Turns off the laser after a specific period of time set in the
settings if a laser is still active.

This method continuously monitors the laser's state and checks
if the maximum allowed running time has been exceeded. If the
maximum time has been reached and the laser is still active, the
laser will be turned off. It pauses execution for 1 second between
checks to reduce resource usage while monitoring.

:raises KeyError: If the 'maxtime' key is not present in settings.
:raises AttributeError: If the 'laser' attribute or 'laseroff' method
    is missing or improperly configured.

<a id="pyroclass.PyroClass.temperature"></a>

#### temperature

```python
def temperature()
```

Provides a dictionary containing current temperature readings from various sensors.

The dictionary includes detailed information such as the current temperature,
average temperature, laser temperature, maximum temperature,
and average maximum temperature. This method is used to obtain
a snapshot of the relevant temperature-related metrics.

:raises No exception is explicitly raised in this method as it only returns a dictionary.
:param None: This method does not take any external parameters.
:return: A dictionary containing the following keys:
         - 'temperature': Current temperature
         - 'averagetemp': Average temperature
         - 'pyrolaser': Laser temperature (pyrolaser)
         - 'maxtemp': Maximum temperature
         - 'averagemaxtemp': Average maximum temperature
:rtype: dict

<a id="pyroclass.pyrometer"></a>

#### pyrometer


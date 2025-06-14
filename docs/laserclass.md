# None

<a id="laserclass"></a>

# laserclass

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

<a id="laserclass.os"></a>

## os

<a id="laserclass.sleep"></a>

## sleep

<a id="laserclass.time"></a>

## time

<a id="laserclass.Timer"></a>

## Timer

<a id="laserclass.GPIO"></a>

## GPIO

<a id="laserclass.settings"></a>

## settings

<a id="laserclass.writesettings"></a>

## writesettings

<a id="laserclass.pyrometer"></a>

## pyrometer

<a id="laserclass.logger"></a>

## logger

<a id="laserclass.LaserClass"></a>

## LaserClass Objects

```python
class LaserClass()
```

Manages the operation and monitoring of a laser control system.

This class provides functionalities to set up and manage the laser’s
interlocks, power settings, status monitoring, and auto shut-off features
based on safety and operational constraints. It continuously monitors the
external conditions such as door interlock and key state to ensure the
laser operates only under permissible conditions.

:ivar dutycycle: Represents the power setting for the laser in percentage.
:ivar laserstate: Indicates whether the laser is currently firing (1 for on, 0 for off).
:ivar maxtime: Maximum duration (in seconds) the laser can continuously run.
:ivar key_channel: GPIO channel used for monitoring the key switch state.
:ivar door_channel: GPIO channel used for monitoring the door interlock state.
:ivar door_led_channel: GPIO channel controlling the indicator LED for the door state.
:ivar enable_channel: GPIO channel used to enable or disable laser firing.
:ivar ttl_channel: GPIO channel used for controlling the laser with pulse width modulation.
:ivar laser_led_channel: GPIO channel controlling the indicator LED for the laser state.
:ivar doorstate: Current state of the door interlock (1 for closed, 0 for open).
:ivar keystate: Current state of the key switch (1 for on, 0 for off).
:ivar laserenabled: Indicates whether the laser is enabled (1 for enabled, 0 for disabled).

<a id="laserclass.LaserClass.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

<a id="laserclass.LaserClass.interlockmonitor"></a>

#### interlockmonitor

```python
def interlockmonitor()
```

Monitors the state of the door and key inputs, and controls the laser enable
state based on their statuses. This method performs continuous checks and
updates the states accordingly by interacting with GPIO channels.

<a id="laserclass.LaserClass.setpower"></a>

#### setpower

```python
def setpower(laserpower)
```

Set the laser power by adjusting the duty cycle and updating the system
settings. The laser power is applied by modifying the internal duty cycle
parameter and saved to persistent storage.

<a id="laserclass.LaserClass.setmaxtimeout"></a>

#### setmaxtimeout

```python
def setmaxtimeout(maxtime)
```

Sets the maximum timeout for the laser system. This determines the maximum time
the laser can remain active.

<a id="laserclass.LaserClass.laserstatus"></a>

#### laserstatus

```python
def laserstatus()
```

Retrieves the current laser status and returns it as a dictionary. The returned
status includes details about the laser power, keyswitch state, door interlock
state, automatic shut-off time, and whether the laser is enabled.

:return: A dictionary containing the following keys and their corresponding
         states:
         - 'laser': The current state of the laser.
         - 'power': The power settings of the laser.
         - 'keyswitch': The state of the keyswitch; True for off and False for
           on.
         - 'doorinterlock': The state of the door interlock; True for disengaged
           and False for engaged.
         - 'autooff': The maximum automatic shut-off time for the laser.
         - 'enabled': A boolean indicating whether the laser is enabled.
:rtype: dict

<a id="laserclass.LaserClass.laserhttpsstatus"></a>

#### laserhttpsstatus

```python
def laserhttpsstatus()
```

Generates and returns the current status of the laser system in a dictionary format.

This method determines the statuses of various components of the laser system,
including the door state, key switch, laser operation, and laser enablement. It
then combines these statuses along with configured power and auto-off time into
a single dictionary to provide a comprehensive system status.

<a id="laserclass.LaserClass.laser"></a>

#### laser

```python
def laser(state)
```

Controls the laser state by turning it on or off depending on the provided state
parameter and system conditions.

The method activates or deactivates the laser based on the `state` parameter and
internal conditions such as the door and key interlock states. When the laser is
turned on, it adjusts the pyrometer read interval, sets up and starts PWM for the
laser and laser LED, and initiates a timer to automatically turn off the laser if
not manually shut down. If the laser is turned off, it resets the pyrometer read
interval and stops the PWM signals.

:param state: Current desired state of the laser. It should be 1 to turn on the
              laser or any other value to turn it off.
:type state: int
:return: None

<a id="laserclass.LaserClass.laserofftimer"></a>

#### laserofftimer

```python
def laserofftimer()
```

Sets a timer to automatically turn off the laser after a specified maximum time is reached.

This method checks if the laser is currently on. If the laser is on, it calculates
a future time based on the current time and the maximum allowed time. The laser
will then be turned off after the calculated duration has passed.

<a id="laserclass.updatesetting"></a>

#### updatesetting

```python
def updatesetting(newsetting)
```

Update the settings with the new values

<a id="laserclass.parsecontrol"></a>

#### parsecontrol

```python
def parsecontrol(item, command)
```

Parses control commands and executes corresponding operations.

The function interprets a given `item` and `command`, then performs the specified
operation, which can range from laser control to fetching settings, depending upon
the `item` value. The operations may include laser power management, temperature
retrieval, laser status updates, system restarts, and more.

<a id="laserclass.reboot"></a>

#### reboot

```python
def reboot()
```

API call to reboot the Raspberry Pi

<a id="laserclass.laser"></a>

#### laser


# Contents for: laserclass

* [laserclass](#laserclass)
  * [os](#laserclass.os)
  * [sleep](#laserclass.sleep)
  * [time](#laserclass.time)
  * [Timer](#laserclass.Timer)
  * [GPIO](#laserclass.GPIO)
  * [settings](#laserclass.settings)
  * [writesettings](#laserclass.writesettings)
  * [pyrometer](#laserclass.pyrometer)
  * [logger](#laserclass.logger)
  * [LaserClass](#laserclass.LaserClass)
    * [\_\_init\_\_](#laserclass.LaserClass.__init__)
    * [interlockmonitor](#laserclass.LaserClass.interlockmonitor)
    * [setpower](#laserclass.LaserClass.setpower)
    * [setmaxtimeout](#laserclass.LaserClass.setmaxtimeout)
    * [laserstatus](#laserclass.LaserClass.laserstatus)
    * [laserhttpsstatus](#laserclass.LaserClass.laserhttpsstatus)
    * [laser](#laserclass.LaserClass.laser)
    * [laserofftimer](#laserclass.LaserClass.laserofftimer)
  * [updatesetting](#laserclass.updatesetting)
  * [parsecontrol](#laserclass.parsecontrol)
  * [reboot](#laserclass.reboot)
  * [laser](#laserclass.laser)

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

Monitor the door interlock and switch off the laser if the door is open

<a id="laserclass.LaserClass.setpower"></a>

#### setpower

```python
def setpower(laserpower)
```

Set the laser power via the serial connection

<a id="laserclass.LaserClass.setmaxtimeout"></a>

#### setmaxtimeout

```python
def setmaxtimeout(maxtime)
```

API call to set the maximum time that the laser can run

<a id="laserclass.LaserClass.laserstatus"></a>

#### laserstatus

```python
def laserstatus()
```

Return the laser (firning) status and the power setting

<a id="laserclass.LaserClass.laserhttpsstatus"></a>

#### laserhttpsstatus

```python
def laserhttpsstatus()
```

Return the laser (firning) status and the power setting

<a id="laserclass.LaserClass.laser"></a>

#### laser

```python
def laser(state)
```

Switch on or off the laser, if laser is on then run a thread to switch off if max time is exceeded

<a id="laserclass.LaserClass.laserofftimer"></a>

#### laserofftimer

```python
def laserofftimer()
```

Auto switch off of the laser after maxtime seconds

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

Main API entrypoint, recieves an **item** and **command** parameter

<a id="laserclass.reboot"></a>

#### reboot

```python
def reboot()
```

API call to reboot the Raspberry Pi

<a id="laserclass.laser"></a>

#### laser


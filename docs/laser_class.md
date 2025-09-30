# None

<a id="laser_class"></a>

# laser\_class

Module for controlling and monitoring a LaserTree K60 450nm laser system.

This module interacts with GPIO channels on a Raspberry Pi to manage the laser system,
including interlocks for door and key switch states. It contains utility to monitor
hardware statuses and perform necessary operations, such as enabling and disabling
the laser based on safety conditions.

The laser power is managed by pulse width modulation (PWM) output on a digital channel.
The laser is automatically turned off after a specified timeout period if it is not
shut down by API control.

<a id="laser_class.Thread"></a>

## Thread

<a id="laser_class.time"></a>

## time

<a id="laser_class.sleep"></a>

## sleep

<a id="laser_class.digital_channels"></a>

## digital\_channels

<a id="laser_class.serial_channels"></a>

## serial\_channels

<a id="laser_class.logger"></a>

## logger

<a id="laser_class.settings"></a>

## settings

<a id="laser_class.writesettings"></a>

## writesettings

<a id="laser_class.LaserObject"></a>

## LaserObject Objects

```python
class LaserObject()
```

Handles laser operations, safety interlocks, and status monitoring.

This class provides the necessary functionality for laser management, including
power control, safety interlock monitoring, and operational status updates. It
interfaces with hardware and software components to ensure safety compliance
and controlled operation of the laser.

<a id="laser_class.LaserObject.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

Initializes an instance of the class.

This constructor method sets up internal variables and configurations required
for the operation of the associated hardware or simulation. The attributes
include various channel assignments and state indicators, ensuring all
necessary initialization details are handled.

<a id="laser_class.LaserObject.check_door_state"></a>

#### check\_door\_state

```python
def check_door_state()
```

Returns a 1 for door closed and 0 for door open, door switch will ground te GPIO pin so will generate a 0
for closed and a 1 for open. Sets the door LED to show it is closed (on) or open (off).

<a id="laser_class.LaserObject.check_key_state"></a>

#### check\_key\_state

```python
def check_key_state()
```

Returns a 1 for key switch closed and 0 for key switch open

<a id="laser_class.LaserObject.interlock_monitor"></a>

#### interlock\_monitor

```python
def interlock_monitor()
```

Monitors the state of the door and key inputs, and controls the laser enable
state based on their statuses. This method performs continuous checks and
updates the states accordingly by interacting with GPIO channels.

<a id="laser_class.LaserObject.laser_status"></a>

#### laser\_status

```python
def laser_status(item, command)
```

Returns the current laser power level.

<a id="laser_class.LaserObject.set_laser_power"></a>

#### set\_laser\_power

```python
def set_laser_power(item, command)
```

Sets the laser power level based on the given value.

<a id="laser_class.LaserObject.laser_set_maxtime"></a>

#### laser\_set\_maxtime

```python
def laser_set_maxtime(item, command)
```

Sets the laser timeout time based on the given value.

<a id="laser_class.LaserObject.laser_off_timer"></a>

#### laser\_off\_timer

```python
def laser_off_timer()
```

Sets a timer to automatically turn off the laser after a specified maximum time is reached.

This method checks if the laser is currently on. If the laser is on, it calculates
a future time based on the current time and the maximum allowed time. The laser
will then be turned off after the calculated duration has passed.

<a id="laser_class.LaserObject.laser_on_off"></a>

#### laser\_on\_off

```python
def laser_on_off(item, command)
```

Handles the operation of a laser based on the given state. The method accordingly
ensures the required conditions are met for turning the laser on. If the state
is turned on, timers are initialized to regulate automatic shutdowns of the laser.
If the state is turned off, the laser components and associated digital channels
are duly deactivated.

<a id="laser_class.LaserObject.http_status_data"></a>

#### http\_status\_data

```python
def http_status_data(item, command)
```

Returns a formatted dictionary of laser status data for the index page.

<a id="laser_class.laser"></a>

#### laser


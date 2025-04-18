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

Laser Class - manages the laser via  TTL PWM

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

LaserClass

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


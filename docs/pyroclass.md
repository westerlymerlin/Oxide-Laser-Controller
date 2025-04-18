# Contents for: pyroclass

* [pyroclass](#pyroclass)
  * [Timer](#pyroclass.Timer)
  * [sleep](#pyroclass.sleep)
  * [time](#pyroclass.time)
  * [b64decode](#pyroclass.b64decode)
  * [serial](#pyroclass.serial)
  * [settings](#pyroclass.settings)
  * [logger](#pyroclass.logger)
  * [PyroClass](#pyroclass.PyroClass)
    * [\_\_init\_\_](#pyroclass.PyroClass.__init__)
    * [close](#pyroclass.PyroClass.close)
    * [readtimer](#pyroclass.PyroClass.readtimer)
    * [setaverage](#pyroclass.PyroClass.setaverage)
    * [resetmax](#pyroclass.PyroClass.resetmax)
    * [laseron](#pyroclass.PyroClass.laseron)
    * [laseroff](#pyroclass.PyroClass.laseroff)
    * [laserofftimer](#pyroclass.PyroClass.laserofftimer)
    * [temperature](#pyroclass.PyroClass.temperature)
  * [pyrometer](#pyroclass.pyrometer)

<a id="pyroclass"></a>

# pyroclass

Pyro Class - controles the microepsilon pyrometer and rangefinder laser

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

Pyrometer class, reads the temperature from the pyromers and controls the rangefinder laser

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

Close the serial port

<a id="pyroclass.PyroClass.readtimer"></a>

#### readtimer

```python
def readtimer()
```

regular timer, reads the temperature every 5 seconds, keeps track of the maximum temperatiure read

<a id="pyroclass.PyroClass.setaverage"></a>

#### setaverage

```python
def setaverage()
```

Add the temp value to the running average list

<a id="pyroclass.PyroClass.resetmax"></a>

#### resetmax

```python
def resetmax()
```

Reset the maximum temerature

<a id="pyroclass.PyroClass.laseron"></a>

#### laseron

```python
def laseron()
```

Switch on the rangefinder laser and set a timer to switch it off after maxtime

<a id="pyroclass.PyroClass.laseroff"></a>

#### laseroff

```python
def laseroff()
```

Switch off the rangefinder laser

<a id="pyroclass.PyroClass.laserofftimer"></a>

#### laserofftimer

```python
def laserofftimer()
```

Auto switch off of the laser after maxtime seconds

<a id="pyroclass.PyroClass.temperature"></a>

#### temperature

```python
def temperature()
```

API Call: return pyrometer values and settings as a json message

<a id="pyroclass.pyrometer"></a>

#### pyrometer


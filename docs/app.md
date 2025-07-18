# None

<a id="app"></a>

# app

Laser Processing System Main Application

This module serves as the main entry point and coordinator for the laser processing system,
integrating various components including laser control, temperature monitoring, camera
operations, and user interface management.

Core Components:
    - System initialization and shutdown procedures
    - Hardware component coordination (laser, pyrometer, camera)
    - Safety monitoring and emergency shutdown handling
    - User interface event handling
    - Settings management and validation
    - Process logging and monitoring

Application Flow:
    1. System initialization and hardware checks
    2. User interface setup
    3. Component coordination (laser, pyrometer, camera)
    4. Process monitoring and control
    5. Safe shutdown procedures

Dependencies:
    - laserclass: Laser control interface
    - pyroclass: Temperature monitoring
    - camera: Image capture and processing
    - app_control: Settings management
    - logmanager: System logging

Usage:
    python app.py

<a id="app.subprocess"></a>

## subprocess

<a id="app.enumerate_threads"></a>

## enumerate\_threads

<a id="app.Flask"></a>

## Flask

<a id="app.render_template"></a>

## render\_template

<a id="app.jsonify"></a>

## jsonify

<a id="app.request"></a>

## request

<a id="app.Response"></a>

## Response

<a id="app.logger"></a>

## logger

<a id="app.pyrometer"></a>

## pyrometer

<a id="app.parsecontrol"></a>

## parsecontrol

<a id="app.laser"></a>

## laser

<a id="app.settings"></a>

## settings

<a id="app.VERSION"></a>

## VERSION

<a id="app.video_camera_instance_0"></a>

## video\_camera\_instance\_0

<a id="app.video_camera_instance_1"></a>

## video\_camera\_instance\_1

<a id="app.app"></a>

#### app

<a id="app.read_log_from_file"></a>

#### read\_log\_from\_file

```python
def read_log_from_file(file_path)
```

Read a log from a file and reverse the order of the lines so newest is at the top

<a id="app.read_cpu_temperature"></a>

#### read\_cpu\_temperature

```python
def read_cpu_temperature()
```

Read the CPU temperature from the Raspberry Pi

<a id="app.threadlister"></a>

#### threadlister

```python
def threadlister()
```

Get a list of all threads running

<a id="app.index"></a>

#### index

```python
@app.route('/')
def index()
```

Main web status page, sets up the template for jscript on the page to retrieve status of the laser and the
images from the two cameras. also contains the list of threads and the software name and version.

<a id="app.api"></a>

#### api

```python
@app.route('/api', methods=['POST'])
def api()
```

API Endpoint for programatic access - needs request data to be posted in a json file and the api-key
in the header, if the api-key does not match it will return an error

<a id="app.statusdata"></a>

#### statusdata

```python
@app.route('/statusdata', methods=['GET'])
def statusdata()
```

Status data read by javascript on default website

<a id="app.video_feed0"></a>

#### video\_feed0

```python
@app.route('/VideoFeed0')
def video_feed0()
```

The image feed read by the browser for camera 0

<a id="app.video_feed1"></a>

#### video\_feed1

```python
@app.route('/VideoFeed1')
def video_feed1()
```

The image feed read by the browser camera 1

<a id="app.showplogs"></a>

#### showplogs

```python
@app.route('/pylog')
def showplogs()
```

Show the Application log

<a id="app.showgalogs"></a>

#### showgalogs

```python
@app.route('/guaccesslog')
def showgalogs()
```

"Show the Gunicorn Access Log

<a id="app.showgelogs"></a>

#### showgelogs

```python
@app.route('/guerrorlog')
def showgelogs()
```

"Show the Gunicorn Errors Log

<a id="app.showslogs"></a>

#### showslogs

```python
@app.route('/syslog')
def showslogs()
```

Show the last 2000 entries from the system log


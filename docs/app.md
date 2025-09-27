# None

<a id="app"></a>

# app

Flask web application for Raspberry Pi system monitoring and control.

This module provides a web interface and API endpoints for monitoring and controlling
a Raspberry Pi system. It includes features for:
- System status monitoring (CPU temperature, running threads)
- Log viewing (Application, Gunicorn, System logs)
- RESTful API endpoints with authentication
- Real-time status updates via JavaScript

The application runs on Gunicorn when deployed on Raspberry Pi and includes
various endpoints for both web interface and programmatic access.

Routes:
    / : Main status page
    /statusdata : JSON endpoint for live status updates
    /api : Protected API endpoint for system control
    /pylog : Application log viewer
    /guaccesslog : Gunicorn access log viewer
    /guerrorlog : Gunicorn error log viewer
    /syslog : System log viewer

Authentication:
    API endpoints require a valid API key passed in the 'Api-Key' header.

<a id="app.subprocess"></a>

## subprocess

<a id="app.enumerate_threads"></a>

## enumerate\_threads

<a id="app.Timer"></a>

## Timer

<a id="app.datetime"></a>

## datetime

<a id="app.Flask"></a>

## Flask

<a id="app.render_template"></a>

## render\_template

<a id="app.jsonify"></a>

## jsonify

<a id="app.request"></a>

## request

<a id="app.redirect"></a>

## redirect

<a id="app.session"></a>

## session

<a id="app.url_for"></a>

## url\_for

<a id="app.send_file"></a>

## send\_file

<a id="app.Response"></a>

## Response

<a id="app.authenticate"></a>

## authenticate

<a id="app.VERSION"></a>

## VERSION

<a id="app.API_KEY"></a>

## API\_KEY

<a id="app.settings"></a>

## settings

<a id="app.logger"></a>

## logger

<a id="app.set_oled"></a>

## set\_oled

<a id="app.parsecontrol"></a>

## parsecontrol

<a id="app.serial_ports"></a>

## serial\_ports

<a id="app.serial_port_info"></a>

## serial\_port\_info

<a id="app.video_camera_instance_0"></a>

## video\_camera\_instance\_0

<a id="app.video_camera_instance_1"></a>

## video\_camera\_instance\_1

<a id="app.app"></a>

#### app

<a id="app.YEAR"></a>

#### YEAR

<a id="app.oledthread"></a>

#### oledthread

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

Read the CPU temperature and returns in in Celsius

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

Main web status page

<a id="app.statusdata"></a>

#### statusdata

```python
@app.route('/statusdata', methods=['GET'])
def statusdata()
```

Status data read by javascript on default website so the page shows near live values

<a id="app.api"></a>

#### api

```python
@app.route('/api', methods=['POST'])
def api()
```

API Endpoint for programatic access - needs request data to be posted in a json file. Contains a check for a
valid API key.

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

<a id="app.login"></a>

#### login

```python
@app.route('/auth', methods=['GET', 'POST'])
def login()
```

Handles authentication by providing a login interface for users. It supports both GET
and POST methods. On successful authentication, the user is redirected to the "config"
page. If authentication fails, the user is informed about the failure and can attempt
to log in again.

<a id="app.config"></a>

#### config

```python
@app.route('/config', methods=['GET', 'POST'])
def config()
```

Handles the configuration for the application through GET and POST methods.

This function provides an endpoint for configuring various application settings.
For POST requests, it processes forms with specific keys to update corresponding
settings. For GET requests, it renders the configuration template with current
application version, settings, network information, and the current year.

<a id="app.config_serial"></a>

#### config\_serial

```python
@app.route('/serial', methods=['GET', 'POST'])
def config_serial()
```

Handles configuration and updates for a specific serial port.

Provides functionality to view and configure serial port settings,
as well as update or delete messages associated with the serial port.
The function supports GET and POST HTTP methods to retrieve serial
port-related pages or process submitted forms.

<a id="app.download_manual"></a>

#### download\_manual

```python
@app.route('/documentation')
def download_manual()
```

Handles the request to download the application's manual.

This function serves the PDF manual of the application as a downloadable
attachment. The manual file's name is retrieved from the application
settings and provided as the download name.

<a id="app.showplogs"></a>

#### showplogs

```python
@app.route('/pylog')
def showplogs()
```

Show the Application log web page

<a id="app.showgalogs"></a>

#### showgalogs

```python
@app.route('/guaccesslog')
def showgalogs()
```

"Show the Gunicorn Access Log web page

<a id="app.showgelogs"></a>

#### showgelogs

```python
@app.route('/guerrorlog')
def showgelogs()
```

"Show the Gunicorn Errors Log web page

<a id="app.showslogs"></a>

#### showslogs

```python
@app.route('/syslog')
def showslogs()
```

Show the last 2000 lines from the system log on a web page


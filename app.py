"""
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
"""
import subprocess
from threading import enumerate as enumerate_threads, Timer
from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect, session, url_for, send_file, Response
from simplepam import authenticate
from app_control import VERSION, API_KEY, settings
from logmanager import logger
from oled_class import set_oled
from api_parser import parsecontrol
from serial_class import serial_ports, serial_port_info
from camera_class import video_camera_instance_0, video_camera_instance_1

app = Flask(__name__)
app.secret_key = API_KEY
logger.info('Starting %s web app version %s', settings['app-name'], VERSION)
YEAR = datetime.now().year
oledthread = Timer(5, set_oled)
oledthread.start()


def read_log_from_file(file_path):
    """Read a log from a file and reverse the order of the lines so newest is at the top"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return list(reversed(lines))


def read_cpu_temperature():
    """Read the CPU temperature and returns in in Celsius"""
    with open(settings['cputemp'], 'r', encoding='utf-8') as f:
        log = f.readline()
    return round(float(log) / 1000, 1)



def threadlister():
    """Get a list of all threads running"""
    appthreads = []
    for appthread in enumerate_threads():
        appthreads.append([appthread.name, appthread.native_id])
    return appthreads


@app.route('/')
def index():
    """Main web status page"""
    return render_template('index.html', version=VERSION, settings=settings,
                           threads=threadlister(), year=YEAR,
                           digital_status=parsecontrol('digitalstatus', False),
                           analogue_status=parsecontrol('analoguestatus', False),
                           serial_status=parsecontrol('serialstatus', False))


@app.route('/statusdata', methods=['GET'])
def statusdata():
    """Status data read by javascript on default website so the page shows near live values"""
    ctrldata = {'cputemperature': read_cpu_temperature(),
                'digital_status': parsecontrol('digitalstatus', False),
                'analogue_status': parsecontrol('analoguestatus', False),
                'serial_status': parsecontrol('serialstatus', False)
                }
    return jsonify(ctrldata), 201


@app.route('/api', methods=['POST'])
def api():
    """API Endpoint for programatic access - needs request data to be posted in a json file. Contains a check for a
    valid API key."""
    try:
        logger.debug('API headers: %s', request.headers)
        logger.debug('API request: %s', request.json)
        if 'Api-Key' in request.headers.keys():  # check api key exists
            if request.headers['Api-Key'] == API_KEY:  # check for correct API key
                item = request.json['item']
                command = request.json['command']
                return jsonify(parsecontrol(item, command)), 201
            logger.warning('API: access attempt using an invalid token from %s', request.headers[''])
            return 'access token(s) unuthorised', 401
        logger.warning('API: access attempt without a token from  %s', request.headers['X-Forwarded-For'])
        return 'access token(s) incorrect', 401
    except KeyError:
        return "badly formed json message", 400


@app.route('/VideoFeed0')
def video_feed0():
    """The image feed read by the browser for camera 0"""
    return Response(video_camera_instance_0.mpeg_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/VideoFeed1')
def video_feed1():
    """The image feed read by the browser camera 1"""
    return Response(video_camera_instance_1.mpeg_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/auth', methods=['GET', 'POST'])
def login():
    """
    Handles authentication by providing a login interface for users. It supports both GET
    and POST methods. On successful authentication, the user is redirected to the "config"
    page. If authentication fails, the user is informed about the failure and can attempt
    to log in again.
    """
    if 'username' in session:
        return redirect(url_for('config'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate(str(username), str(password)):
            logger.info('login successful for %s', username)
            session['username'] = request.form['username']
            return redirect(url_for('config'))
        logger.warning('login failed for %s', username)
        return render_template('auth.html', version=VERSION, settings=settings, year=YEAR,
                                   loginfailed=True, username=request.form['username'])
    return render_template('auth.html', version=VERSION, settings=settings, year=YEAR,
                           loginfailed=False, username='')


@app.route('/config', methods=['GET', 'POST'])
def config():
    """
    Handles the configuration for the application through GET and POST methods.

    This function provides an endpoint for configuring various application settings.
    For POST requests, it processes forms with specific keys to update corresponding
    settings. For GET requests, it renders the configuration template with current
    application version, settings, network information, and the current year.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['form-name'] == 'hostname':
            parsecontrol('setappname', request.form['app-name'])
        elif request.form['form-name'] == 'netsettings':
            parsecontrol('setnetinfo', request.form)
        elif request.form['form-name'] == 'oled':
            parsecontrol('set_oled', request.form)
        elif request.form['form-name'] == 'analoguesettings':
            parsecontrol('analogue_settings', request.form)
        elif request.form['form-name'] == 'digitalsettings':
            parsecontrol('digital_settings', request.form)
        elif request.form['form-name'] == 'loglevel':
            parsecontrol('updatesetting', {'loglevel': request.form['loglevel']})
        else:
            logger.warning('config request: key not handled %s', request.form)
    set_oled()
    return render_template('config.html', apikey=API_KEY, version=VERSION, settings=settings,
                           netinfo=parsecontrol('getnetinfo', True), year=YEAR,
                           serial_ports=serial_ports())


@app.route('/serial', methods=['GET', 'POST'])
def config_serial():
    """
    Handles configuration and updates for a specific serial port.

    Provides functionality to view and configure serial port settings,
    as well as update or delete messages associated with the serial port.
    The function supports GET and POST HTTP methods to retrieve serial
    port-related pages or process submitted forms.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    port = request.args['port']
    if request.method == 'POST':
        if request.form['form-name'] == 'comsettings':
            parsecontrol('update_serial_channel', request.form)
        elif request.form['form-name'] == 'messageupdate':
            parsecontrol('update_serial_message', request.form)
        elif request.form['form-name'] == 'messagedelete':
            parsecontrol('delete_serial_message', request.form)
        else:
            logger.warning('serial request: key not handled %s', request.form)
    return render_template('serial.html', version=VERSION, settings=settings,
                           port=port, serial_port=serial_port_info(port), year=YEAR)


@app.route('/documentation')
def download_manual():
    """
    Handles the request to download the application's manual.

    This function serves the PDF manual of the application as a downloadable
    attachment. The manual file's name is retrieved from the application
    settings and provided as the download name.
    """
    return send_file('manual.pdf', download_name='%s.pdf' % settings['app-name'], as_attachment=True)


@app.route('/pylog')
def showplogs():
    """Show the Application log web page"""
    cputemperature = read_cpu_temperature()
    logs = read_log_from_file(settings['logfilepath'])
    return render_template('logs.html', rows=logs, log='Application log',
                           cputemperature=cputemperature, settings=settings, version=VERSION, year=YEAR)


@app.route('/guaccesslog')
def showgalogs():
    """"Show the Gunicorn Access Log web page"""
    cputemperature = read_cpu_temperature()
    logs = read_log_from_file(settings['gunicornpath'] + 'gunicorn-access.log')
    return render_template('logs.html', rows=logs, log='Gunicorn Access Log',
                           cputemperature=cputemperature, settings=settings, version=VERSION, year=YEAR)


@app.route('/guerrorlog')
def showgelogs():
    """"Show the Gunicorn Errors Log web page"""
    cputemperature = read_cpu_temperature()
    logs = read_log_from_file(settings['gunicornpath'] + 'gunicorn-error.log')
    return render_template('logs.html', rows=logs, log='Gunicorn Error Log',
                           cputemperature=cputemperature, settings=settings, version=VERSION, year=YEAR)


@app.route('/syslog')
def showslogs():
    """Show the last 2000 lines from the system log on a web page"""
    cputemperature = read_cpu_temperature()
    log = subprocess.Popen('/bin/journalctl -n 2000', shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode(encoding='utf-8')
    logs = log.split('\n')
    logs.reverse()
    return render_template('logs.html', rows=logs, log='System Log', cputemperature=cputemperature,
                            settings=settings, version=VERSION, year=YEAR)


if __name__ == '__main__':
    app.run()

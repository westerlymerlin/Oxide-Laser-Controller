"""
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
"""
import subprocess
from threading import enumerate as enumerate_threads
from flask import Flask, render_template, jsonify, request, Response
from logmanager import  logger
from laserclass import pyrometer, parsecontrol, laser
from app_control import settings, VERSION
from camera import video_camera_instance_0, video_camera_instance_1

logger.info('Starting %s web app version %s', settings['app-name'], VERSION)
logger.info('Api-Key = %s', settings['api-key'])

app = Flask(__name__)


def read_log_from_file(file_path):
    """Read a log from a file and reverse the order of the lines so newest is at the top"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return list(reversed(lines))


def read_cpu_temperature():
    """Read the CPU temperature from the Raspberry Pi"""
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
    """Main web status page, sets up the template for jscript on the page to retrieve status of the laser and the
    images from the two cameras. also contains the list of threads and the software name and version."""
    return render_template('index.html', version=VERSION, appname=settings['app-name'],
                           threads=threadlister())


@app.route('/api', methods=['POST'])
def api():
    """API Endpoint for programatic access - needs request data to be posted in a json file and the api-key
     in the header, if the api-key does not match it will return an error"""
    try:
        logger.debug('API headers: %s', request.headers)
        logger.debug('API request: %s', request.json)
        if 'Api-Key' in request.headers.keys():  # check api key exists
            if request.headers['Api-Key'] == settings['api-key']:  # check for correct API key
                item = request.json['item']
                command = request.json['command']
                return jsonify(parsecontrol(item, command)), 201
            logger.warning('API: access attempt using an invalid token')
            return 'access token(s) unuthorised', 401
        logger.warning('API: access attempt without a token')
        return 'access token(s) incorrect', 401
    except KeyError:
        logger.warning('API: Badly formed json message')
        return "badly formed json message", 401

@app.route('/statusdata', methods=['GET'])
def statusdata():
    """Status data read by javascript on default website"""
    ctrldata = laser.laserhttpsstatus() | pyrometer.temperature()
    ctrldata['laserfrequency'] = settings['frequency']
    ctrldata['cputemperature'] = read_cpu_temperature()
    return jsonify(ctrldata), 201

@app.route('/VideoFeed0')
def video_feed0():
    """The image feed read by the browser for camera 0"""
    return Response(video_camera_instance_0.mpeg_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/VideoFeed1')
def video_feed1():
    """The image feed read by the browser camera 1"""
    return Response(video_camera_instance_1.mpeg_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/pylog')
def showplogs():
    """Show the Application log"""
    cputemperature = read_cpu_temperature()
    logs = read_log_from_file(settings['logfilepath'])
    return render_template('logs.html', rows=logs, log='Application log',
                           cputemperature=cputemperature, appname=settings['app-name'], version=VERSION)


@app.route('/guaccesslog')
def showgalogs():
    """"Show the Gunicorn Access Log"""
    cputemperature = read_cpu_temperature()
    logs = read_log_from_file(settings['gunicornpath'] + 'gunicorn-access.log')
    return render_template('logs.html', rows=logs, log='Gunicorn Access Log',
                           cputemperature=cputemperature, appname=settings['app-name'], version=VERSION)


@app.route('/guerrorlog')
def showgelogs():
    """"Show the Gunicorn Errors Log"""
    cputemperature = read_cpu_temperature()
    logs = read_log_from_file(settings['gunicornpath'] + 'gunicorn-error.log')
    return render_template('logs.html', rows=logs, log='Gunicorn Error Log',
                           cputemperature=cputemperature, appname=settings['app-name'], version=VERSION)


@app.route('/syslog')
def showslogs():
    """Show the last 2000 entries from the system log"""
    cputemperature = read_cpu_temperature()
    log = subprocess.Popen('/bin/journalctl -n 2000', shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode(encoding='utf-8')
    logs = log.split('\n')
    logs.reverse()
    return render_template('logs.html', rows=logs, log='System Log', cputemperature=cputemperature,
                           version=VERSION, appname=settings['app-name'])



if __name__ == '__main__':
    app.run()

"""
This is the main flask application - called by Gunicorn
"""
import subprocess
from threading import enumerate as enumerate_threads
from flask import Flask, render_template, jsonify, request, Response
from logmanager import  logger
from laserclass import pyrometer, parsecontrol, laser
from app_control import settings, VERSION
from camera import VideoCamera

logger.info('Starting Laser Controller web app version %s', VERSION)
logger.info('Api-Key = %s', settings['api-key'])
app = Flask(__name__)
video_stream = VideoCamera()

def read_log_from_file(file_path):
    """Read a log from a file and reverse the order of the lines so newest is at the top"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return list(reversed(lines))


def read_cpu_temperature():
    """Read the CPU temperature"""
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
    cputemperature = read_cpu_temperature()
    return render_template('index.html', laser=laser.httpstatus(), pyro=pyrometer.httpstatus(),
                           cputemperature=cputemperature, version=VERSION, appname=settings['app-name'],
                           threads=threadlister())


@app.route('/api', methods=['POST'])
def api():
    """API Endpoint for programatic access - needs request data to be posted in a json file"""
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


def gen(camera):
    """Image processor, converts the stream of jpegs into an m-jpeg format for the browser"""
    while True:
        frame = camera.get_frame()
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'


@app.route('/video_feed')
def video_feed():
    """The image feed read by the browser"""
    return Response(gen(video_stream), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/pylog')
def showplogs():
    """Show the Application log"""
    cputemperature = read_cpu_temperature()
    logs = read_log_from_file(settings['logfilepath'])
    return render_template('logs.html', rows=logs, log='Valve-Control log',
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
    """Show the system log"""
    cputemperature = read_cpu_temperature()
    log = subprocess.Popen('/bin/journalctl -n 2000', shell=True,
                           stdout=subprocess.PIPE).stdout.read().decode(encoding='utf-8')
    logs = log.split('\n')
    logs.reverse()
    return render_template('logs.html', rows=logs, log='System Log', cputemperature=cputemperature,
                           version=VERSION, appname=settings['app-name'])



if __name__ == '__main__':
    app.run()

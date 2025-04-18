# Module Documentation


This document contains the documentation for all the modules in the **Oxide Line Laser Controller** version 1.5.1 application.

---

## Contents


[app](./app.md)  
This is the main flask application - called by Gunicorn

[app_control](./app_control.md)  
Settings module, reads the settings from a settings.json file. If it does not exist or a new setting
has appeared it will creat from the defaults in the initialise function.

[camera](./camera.md)  
Camera module, configures the webcam if it is avaialbe uses the
cv2 library from opencv-python-headless
Author: Gary Twinn

[laserclass](./laserclass.md)  
Laser Class - manages the laser via  TTL PWM

[logmanager](./logmanager.md)  
logmanager, setus up application logging. use the **logger** property to
write to the log.

[pyroclass](./pyroclass.md)  
Pyro Class - controles the microepsilon pyrometer and rangefinder laser


---


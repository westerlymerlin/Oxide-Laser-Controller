# Contents for: camera

* [camera](#camera)
  * [cv2](#camera.cv2)
  * [logger](#camera.logger)
  * [settings](#camera.settings)
  * [VideoCamera](#camera.VideoCamera)
    * [\_\_init\_\_](#camera.VideoCamera.__init__)
    * [\_\_del\_\_](#camera.VideoCamera.__del__)
    * [get\_frame](#camera.VideoCamera.get_frame)
    * [mpeg\_stream](#camera.VideoCamera.mpeg_stream)
  * [video\_camera\_instance\_0](#camera.video_camera_instance_0)
  * [video\_camera\_instance\_1](#camera.video_camera_instance_1)

<a id="camera"></a>

# camera

Camera Control and Image Capture

This module provides functionality for controlling and capturing images from a camera device.
Handles camera setup, configuration, image acquisition, and cleanup operations.

Features:
    - Camera initialization and configuration
    - Image capture and storage
    - Camera parameter adjustments (exposure, resolution, etc.)
    - Resource management (proper camera shutdown)

Usage Example:
    from camera import Camera

    camera = Camera()
    camera.capture('image.jpg')
    camera.close()

The module is designed for use with hardware camera interfaces and ensures proper
resource handling for stable operation in long-running applications.

Dependencies:
    Hardware: Compatible camera device
    Software: Appropriate camera drivers/libraries

<a id="camera.cv2"></a>

## cv2

<a id="camera.logger"></a>

## logger

<a id="camera.settings"></a>

## settings

<a id="camera.VideoCamera"></a>

## VideoCamera Objects

```python
class VideoCamera()
```

Initializes the VideoCamera class.

The constructor creates a VideoCapture object, which represents the video source. It sets the video source
properties, such as frame rate, width, height, brightness, and contrast. If no video camera is found, an
error message is logged.

<a id="camera.VideoCamera.__init__"></a>

#### \_\_init\_\_

```python
def __init__(camera_index, camerasettings)
```

<a id="camera.VideoCamera.__del__"></a>

#### \_\_del\_\_

```python
def __del__()
```

Releases resources when app is closed down

<a id="camera.VideoCamera.get_frame"></a>

#### get\_frame

```python
def get_frame()
```

Get a stream of raw images and encode as jpg files

<a id="camera.VideoCamera.mpeg_stream"></a>

#### mpeg\_stream

```python
def mpeg_stream()
```

Image processor, converts the stream of jpegs into an m-jpeg format for the browser

<a id="camera.video_camera_instance_0"></a>

#### video\_camera\_instance\_0

<a id="camera.video_camera_instance_1"></a>

#### video\_camera\_instance\_1


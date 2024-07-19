# Video apps
To speed up the video apps development with OpenCV, this module is designed with all the necessary abstractions to load, process, retransmit and record a video source. 

The video source options are local video files, camera devices, or RTSP urls (processed with [GStreamer](https://gstreamer.freedesktop.org/)).

## Dependencies
GStreamer is the backend used to handle the RTSP conections, therefore their libs must be installed in the system. Here is the command for Debian based distros, but please refer to the [oficial website](https://gstreamer.freedesktop.org/documentation/installing/index.html?gi-language=c) for more information or updates.
``` shell
$ apt install -y \
    libgstreamer1.0-dev \
	libgstreamer-plugins-base1.0-dev \
	libgstreamer-plugins-bad1.0-dev \
	gstreamer1.0-rtsp \
	gstreamer1.0-plugins-base \
	gstreamer1.0-plugins-good \
	gstreamer1.0-plugins-bad \
	gstreamer1.0-plugins-ugly \
	gstreamer1.0-libav \
	gstreamer1.0-tools \
	gstreamer1.0-x \
	gstreamer1.0-alsa \
	gstreamer1.0-gl \
	gstreamer1.0-gtk3 \
	gstreamer1.0-qt5 \
	gstreamer1.0-pulseaudio

```

Also, OpenCV is used for the video manipulation, then it should be installed and must have GStreamer support to use the streaming capabilties. The following command would tell if the installation has support for GStreamer:

``` shell
$ python3 -c "import cv2; print(cv2.getBuildInformation())" | grep GStreamer
```

## Install
This module is currently available at the [Test PyPI](https://test.pypi.org/project/video-apps/) index, use the following command to install it
``` shell
$ pip install -i https://test.pypi.org/simple/ video-apps
```

Further tested versions will be uploaded to the main index (not the test version).

## Usage
The base application is a simple video consumer. This is an example on how to load a local video file and display its content on screen.

``` python
# Import the base app (video consumer)
from video_apps.base import VideoConsumer

if __name__ == '__main__':
    # Create video consumer
    video_consumer = VideoConsumer(
        local_source='path_to_video.mp4',
        display=True
    )

    # Run the application
    video_consumer.run()
```

For new video applications where a processing function is needed, then use a subclass of the `VideoConsumer` definition.

## Custom apps
 In the subclasses only the `process` method should be overrided, because the `run` method handles the resources (create, open, release, etc.) as well as the main processing loop. 

Check the [test](./test/) folder for some basic examples.
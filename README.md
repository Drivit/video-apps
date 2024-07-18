# Video apps
To speed up the video apps development, this module is designed with all the necessary abstractions to load, process, retransmit and record a video source. 

The video source options are local video files, camera devices, or RTSP urls (processed with [GStreamer](https://gstreamer.freedesktop.org/)).

> NOTE: the OpenCV installation should have GStreamer support to use the GStreamer capabilties. 

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
 In the subclasses only the `__init__` and `process` methods should be overrided, because the `run` method handles the resources (create, open, release, etc.) as well as the main processing loop. 

Check the [test](./test/) folder for some basic examples.
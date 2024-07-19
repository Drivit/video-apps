import cv2

# Import the base app (video consumer)
from video_apps.base import VideoConsumer

# Define the custom processor
class EdgeFiltering(VideoConsumer):
    def __init__(
            self,
            camera_source: 'int | None' = None,
            rtsp_source: 'str | None' = None,
            local_source: 'str | None' = None,
            location: 'str | None' = None,
            output_path: 'str | None' = None,
            display: bool = False,
            logging_level: str = 'INFO',
            scale: float = 1
        ) -> None:
        # Initialize the base class
        super().__init__(
            camera_source,
            rtsp_source,
            local_source,
            location,
            output_path,
            display,
            logging_level,
            scale
        )

    # Override the processing function
    def process(self, frame: cv2.Mat) -> cv2.Mat:
        # Change frame to gray scale
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 

        # Blur the image for better edge detection
        frame = cv2.GaussianBlur(frame,(3,3), sigmaX=0, sigmaY=0) 

        # Apply the filter with some magic numbers
        frame = cv2.Canny(frame, 70, 135)

        # FIXME
        # Change gray to color, or else the video will not be saved properly
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR) 

        # Return the processed frame
        return frame

if __name__ == '__main__':
    # Create new video app
    video_app = EdgeFiltering(
        camera_source=0,
        display=True,
    )

    # Run the application
    video_app.run()
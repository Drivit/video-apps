# Built-in modules
import sys
import logging

# Installed modules
import cv2

# Custom modules
from .core import VideoStream
from .utils import GracefulKiller
from .utils import generate_rtsp_writer, create_rtsp_reader_pipeline

class VideoConsumer:
    '''
    This class provides an encapsulated video consumer with stream (via RTSP),
    local video and video device (webcam, video capture, etc) as possible 
    sources. 

    In this class the `process` function only reads and returns the frames (no 
    processign aplied). In order to create an application that apply some 
    processing, use this class as parent and override the `process` function 
    and add new objects if needed in the child's `__init__` function, ex: 
    ConvNets, filters, etc.

    > NOTE: if a local source is specified, then no threads are used to read
    the video file.
    '''

    def __init__(
            self,
            camera_source: 'int | None' = None,
            rtsp_source: 'str | None' = None,
            local_source: 'str | None' = None,
            location: 'str | None' = None,
            output_path: 'str | None' = None,
            display: bool = False,
            logging_level: str = 'INFO',
            scale: float = 1.0,
        ) -> None:
        '''
        Define only one video source for the application. If more than one are 
        specified, the application will be opening a single source with the 
        following hierarchy: local video > stream url > device

        The application has options for the processed video to display (in a 
        cv2 window), retransmit (via RTSP again) and save (record). These 
        options are specified in the params, by default all of them are 
        disabled.

        params:
        - `camera_source`: camera index to open and read from device
        - `rtsp_source`: rtsp url for processing with gstreamer
        - `local_source`: video path to a local video
        - `location`: location to retransmit the processed video
        - `output_path`: output file path to save the processed video
        - `display`: wheter to display or not the processed video
        - `logging-level`: logging level for the messages
        - `scale`: the scale factor for the readed frames
        '''

         # Apply loggers default config 
        logging.basicConfig(
            level=logging_level,
            format='%(asctime)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Get session logger
        self.logger = logging.getLogger()

        # Create signal handler to stop the execution
        self.program_killer = GracefulKiller()

        # Check if a video source is specified, else close
        if not local_source and not rtsp_source and (camera_source is None):
            self.logger.error('No video source specified. Closing.')
            sys.exit(1)

        # Create video capture object
        self.using_stream_as_source = True
        if local_source:
            self.using_stream_as_source = False
            self.video_source = cv2.VideoCapture(local_source)
        elif rtsp_source:
            gstreamer_pipeline = create_rtsp_reader_pipeline(rtsp_source)
            self.video_source = VideoStream(
                gstreamer_pipeline, 
                cv2.CAP_GSTREAMER
            )
        elif camera_source is not None:
            self.video_source = VideoStream(camera_source)

        # Check if the video was sucessfully opened
        try:
            assert(self.video_source.isOpened())
            if self.using_stream_as_source:
                self.video_source = self.video_source.start()

            self.logger.info('Video source ready')
        except:
            self.logger.error('The video source is unavailable. Closing.')
            sys.exit(1)
            
        # Get basic info from the video source
        if self.using_stream_as_source:
            self.height, self.width = self.video_source.resolution()
            self.fps = self.video_source.fps()
        else:
            self.width = int(self.video_source.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.video_source.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.fps = self.video_source.get(cv2.CAP_PROP_FPS)

        # Log the video resolution
        self.logger.debug(f'Original resolution: {self.width}x{self.height}')

        # Check if the video should be scaled
        self.scale = scale
        if scale != 1.0:
            self.width = int(self.width * scale)
            self.height = int(self.height * scale)

            self.logger.debug(f'New resolution: {self.width}x{self.height}')
            
        # Create retransmission if needed
        self.retransmission_channel = None
        if (location):
            self.retransmission_channel = generate_rtsp_writer(
                location, 
                self.fps, 
                self.width, 
                self.height
            )

            self.logger.info(
                f'Retransmiting video at: rtsp://localhost:8554/{location}'
            )

        # Set var to display or not the processed video
        self.display = display

        # Set the outfile file if needed
        self.output_file = None
        if output_path:
            self.output_file = cv2.VideoWriter(
                filename=output_path,
                fourcc=cv2.VideoWriter_fourcc(*'avc1'),
                fps=self.fps, 
                frameSize=(self.width, self.height),
            )

            self.logger.info(f'Processed video saved at: {output_path}')

    def process(self, frame: cv2.Mat) -> cv2.Mat:
        '''
        In this module, the function only returns the readed frames.
        '''
        return frame

    def run(self) -> None:
        '''
        This is the main processing loop, it will be running up to the end of 
        the video source or when a stop message is received. 
        
        The stop messages are:
        - Press the `q` key
        - send a `SIGTERM` signal (also by pressing `CTRL`+`C`)
        - send a `SIGINT` signal
        '''
        while True:
            if self.program_killer.kill_now:
                self.logger.debug('Closing gracefully')
                break

            # Frame capturing
            if self.using_stream_as_source:
                frame = self.video_source.read()
            else:
                ret, frame = self.video_source.read()

                # Check if a frame was grabbed
                if not ret:
                    break

            # Check if the video should be scaled
            if self.scale != 1.0:
                frame = cv2.resize(frame, (self.width, self.height))

            # Function to process the frames
            processed_frame = self.process(frame)

            # Check if the video frame should be displayed on screen
            if self.display:
                cv2.imshow(self.__class__.__name__, processed_frame)

            # Check if the video should be retransmited
            if self.retransmission_channel:
                self.retransmission_channel.write(processed_frame)

            # Check if the video should be saved
            if self.output_file:
                self.output_file.write(processed_frame)
            
            # Wait for a key interaction to stop the execution
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.program_killer.kill_now = True

        self._close()    

    def _close(self) -> None:
        '''
        After the video processing is over, release all the resources.
        '''
        # Stop reading threads if necessary 
        if self.using_stream_as_source:
            self.video_source.stop()
            
        # Close video source
        self.video_source.release()

        # Close local video file if needed
        if not (self.output_file is None):
            self.output_file.release()
        
        # Close RTSP retransmission if needed
        if not (self.retransmission_channel is None):
            self.retransmission_channel.release()
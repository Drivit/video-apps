import cv2
import signal

class GracefulKiller:
    '''
    Simple signal catcher for multiple closing or stop signals.
    '''
    def __init__(self):
        self.kill_now = False

        # Assign signal to the kill process flag
        signal.signal(signal.SIGINT, self.exit_now)
        signal.signal(signal.SIGTERM, self.exit_now)


    def exit_now(self, signum, frame):
        self.kill_now = True
        

def generate_rtsp_writer(location, fps, width, height):
    '''Create a `cv2.VideoWriter` to retransmit a video over RTSP'''
    return cv2.VideoWriter(
		'appsrc ! videoconvert' + \
			' ! x264enc speed-preset=ultrafast tune=zerolatency' + \
			' ! video/x-h264,profile=high' + \
			f' ! rtspclientsink location={location}', 
		cv2.CAP_GSTREAMER, 
		0,
		fps,
		(width, height), 
		True
	)

def create_rtsp_reader_pipeline(rtsp_url, width=640, height=480):
	'''
	Generate a pipeline for GStreamer to read a RTSP source with the minimum 
	possible latency and delay (then no buffer).
	'''
	gstreamer_pipeline = "rtspsrc " + \
			"location={} latency=0 ! " + \
			"queue ! " + \
			"rtph264depay ! " + \
			"h264parse ! " + \
			"avdec_h264 ! " + \
			"videoconvert ! " + \
			"videoscale ! " + \
			"video/x-raw,width={},height={} ! " + \
			"appsink sync=false drop=true"
	
	return gstreamer_pipeline.format(rtsp_url, width, height)
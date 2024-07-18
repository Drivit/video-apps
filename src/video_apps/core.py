import cv2
from threading import Thread

class VideoStream:
	'''
	Copy of the class `imutils.video.WebcamVideoStream` from the imutils 
	package. Designed to read frames in a separated thread to speed up the 
	real time processing.

	This copy was created to add some functionalities and a seemless integration
	of this new `VideoStream` as a regular `VideoCapture` object.
	'''
	def __init__(
			self, 
			src = 0, 
			apiReference = cv2.CAP_V4L2, 
			name="VideoStream"):
		# initialize the video camera stream and read the first frame
		# from the stream
		self.stream = cv2.VideoCapture(src, apiReference)
		(self.grabbed, self.frame) = self.stream.read()

		# initialize the thread name
		self.name = name

		# initialize the variable used to indicate if the thread should
		# be stopped
		self.stopped = False

	def start(self):
		'''start the thread to read frames from the video stream'''
		t = Thread(target=self.update, name=self.name, args=())
		t.daemon = True
		t.start()
		return self

	def update(self):
		'''keep looping infinitely until the thread is stopped'''
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return

			# otherwise, read the next frame from the stream
			(self.grabbed, self.frame) = self.stream.read()

	def read(self):
		'''return the frame most recently read'''
		return self.frame
	
	def isOpened(self):
		'''return if the capture was sucessfully opened'''
		return self.stream.isOpened()

	def stop(self):
		'''indicate that the thread should be stopped'''
		self.stopped = True
		
	def release(self):
		'''release the VideoCapture object'''
		self.stream.release()

	def resolution(self):
		'''return the current resolution of the frame'''
		return self.frame.shape[:2]
	
	def fps(self):
		'''get the FSP for the VideoCapture object'''
		return self.stream.get(cv2.CAP_PROP_FPS)


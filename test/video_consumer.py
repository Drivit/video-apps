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
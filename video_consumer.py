from video_apps.base import VideoConsumer

if __name__ == '__main__':
    video_consumer = VideoConsumer(
        # camera_source=0,
        local_source='./HD_CCTV.mp4',
        display=True
    )

    video_consumer.run()
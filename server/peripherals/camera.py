from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
from picamera2.encoders import Quality


class Camera:
    def __init__(self, size = (400, 300)) -> None:
        self.camera = Picamera2()
        config = self.camera.create_video_configuration(main={"size": size})
        self.camera.configure(config)
        self.encoder = JpegEncoder(q=90)

    def start(self, output) -> None:
        self.camera.start_recording(self.encoder, FileOutput(output), quality=Quality.VERY_HIGH)

    def stop(self) -> None:
        self.camera.stop_recording()
        self.camera.close()

import io
from threading import Condition
import struct
from threading import Thread
from network import TcpSocket
from utils.thread import stopThread


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class VideoStream:
    def __init__(self, camera, port: int, ifname) -> None:
        self.camera = camera
        self.port = port
        self.ifname = ifname
        self.runnable = False

    def start(self) -> None:
        self.runnable = True
        self.output = StreamingOutput()
        self.camera.start(self.output)

        print('opening socket for video stream..')
        self.socket = TcpSocket(self.port, self.ifname)
        self.runner = Thread(target=self._run, daemon=True)
        self.runner.start()

    def _run(self):
        self.socket.accept(self._send_video)

    def _send_video(self, connection):
        connection = connection.makefile('wb')

        while self.runnable:
            with self.output.condition:
                self.output.condition.wait()
                frame = self.output.frame

            try:
                lenFrame = len(self.output.frame)
                lengthBin = struct.pack('<I', lenFrame)
                connection.write(lengthBin)
                connection.write(frame)
            except Exception as e:
                print(f"exception in sending video: {e}")
                self.camera.stop()
                return True

        return False

    def stop(self):
        self.runnable = False
        try:
            if hasattr(self, 'runner'):
                stopThread(self.runner)
            if hasattr(self, 'socket'):
                self.camera.stop()
        except:
            pass

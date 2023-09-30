import traceback
from enum import Enum
from threading import Thread
from network import TcpSocket
from utils.thread import stopThread


class Command(Enum):
    CMD_MOTOR = 1
    CMD_M_MOTOR = 2
    CMD_CAR_ROTATE = 3
    CMD_LED = 4
    CMD_LED_MOD = 5
    CMD_SERVO = 6
    CMD_BUZZER = 7
    CMD_SONIC = 8
    CMD_LIGHT = 9
    CMD_POWER = 10
    CMD_MODE = 11

    # extra command for consistency
    CMD_LINE_TRACK = 12

    def __str__(self):
        return self.name


COMMAND_TYPE_SEPARATOR = '\n'
COMMAND_DATA_SEPARATOR = '#'

class CommandStream:
    """Provides way to get commands from clients via tcp connection"""
    def __init__(self, callback, port: int, ifname) -> None:
        self.callback = callback
        self.port = port
        self.ifname = ifname

    def start(self) -> None:
        # TODO abstract away network communication to support other protocols
        # (e.g. http)
        print('opening socket for command stream..')
        self.socket = TcpSocket(self.port, self.ifname)
        self.runner = Thread(target=self._run, daemon=True)
        self.runner.start()

    def _run(self) -> None:
        self.socket.accept(self._get_command)

    def _get_command(self, connection) -> None:
        self.connection = connection

        while True:
            # TODO handle partial data
            rawDataStr = connection.recv(1024).decode('utf-8')

            try:
                # parse commands
                commands = []
                rawCommands = [rawDataStr] if COMMAND_TYPE_SEPARATOR not in rawDataStr else rawDataStr.split(
                    COMMAND_TYPE_SEPARATOR)

                for rawCommandStr in rawCommands:
                    commandParts = rawCommandStr.split(COMMAND_DATA_SEPARATOR)
                    if len(commandParts) == 0 or len(rawCommandStr) == 0:
                        continue

                    commandName = Command[commandParts[0]]
                    commandData = commandParts[1:]
                    commands.append((commandName, commandData))

                # client misbehaves
                if len(commands) == 0:
                    continue

                # execute them
                if self.callback(commands):
                    return True

            except BrokenPipeError:
                pass

            except Exception as e:
                print(f"exception in processing command stream: {e}")
                traceback.print_exc()

    def notifyClient(self, data):
        if isinstance(data, list):
            data = COMMAND_DATA_SEPARATOR.join([str(item) for item in data])

        print(f"sending back to client: {data=}")
        self.connection.send(data.encode())

    def stop(self):
        if hasattr(self, 'runner'):
            stopThread(self.runner)
        if hasattr(self, 'connection'):
            self.connection.close()

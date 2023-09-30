import traceback
from typing import Any
from commands import *
from video import *
from capabilities import Capabilities

# define environment constants
NETWORK_INTERFACE_NAME = 'wlan0'   # NOTE: check with ifconfig
COMMAND_STREAM_PORT = 5000
VIDEO_STREAM_PORT = 8000


print('environment configured with:')
print(f"\tnetwork interface: {NETWORK_INTERFACE_NAME} (change it if you're getting \"[Errno 19] No such device\") exception")
print(f"\tcommand stream port: {COMMAND_STREAM_PORT}")
print(f"\tideo stream port: {VIDEO_STREAM_PORT}")

class ClientCallback:
    """ the way to send data back from commands to client"""
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        data = args[0]
        self.commandStream.notifyClient(data)


# setup device capabilities
callback = ClientCallback()
capabilities = Capabilities(callback)
allCommands = capabilities.getCatalog().getAllCommands()


def executeCommands(commandsData):
    for type, data in commandsData:
        print(f"received command: {type=}, {data=}")
        command = allCommands.get(type)
        command.run(data)
    callback('OK')
    # return true to exit from command stream
    return False


if __name__ == '__main__':
    try:
        print('starting streaming..')
        # create and run streams
        commandStream, videoStream = None, None
        commandStream = CommandStream(
            callback=executeCommands,
            port=COMMAND_STREAM_PORT,
            ifname=NETWORK_INTERFACE_NAME)
        callback.commandStream = commandStream
        commandStream.start()

        videoStream = VideoStream(
            capabilities.gePeripherals().camera,
            port=VIDEO_STREAM_PORT,
            ifname=NETWORK_INTERFACE_NAME)
        videoStream.start()

        print('waiting for client connections..')
        while True:
            input('')

    except KeyboardInterrupt:
        print("\nreceived interruption signal")
        pass

    except Exception as e:
        print(f"\033[91mException: \"{e}\".\033[0m")
        traceback.print_exc()

    finally:
        print("exiting gratefully..")
        if commandStream:
            commandStream.stop()

        if videoStream:
            videoStream.stop()

        for name, command in allCommands.items():
            if hasattr(command, 'stop'):
                print(f"stopping {name}")
                command.stop()

    print("completed")

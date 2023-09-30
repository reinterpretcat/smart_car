from .common import Command


class BuzzerCommand():
    def __init__(self, buzzer, isDryRun=True) -> None:
        self.buzzer = buzzer
        self.isDryRun = isDryRun

    def name(self) -> Command:
        return Command.CMD_BUZZER

    def run(self, data) -> None:
        flag = data[0] != '0'

        if self.isDryRun:
            print(f"{self.name()} {data[0]=}, setting {flag=}")
            return

        self.buzzer.run(flag)


class Command:
    def __init__(self, device_id: str, command: str) -> None:
        self._device_id = device_id
        self._command = command

    def __str__(self) -> str:
        return f"Command({self.device_id}, {self.command})"

    @property
    def device_id(self) -> str: return self._device_id
    @property
    def command(self) -> str: return self._command

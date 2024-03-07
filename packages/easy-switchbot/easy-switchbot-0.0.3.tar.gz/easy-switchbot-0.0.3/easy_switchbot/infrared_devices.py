from easy_switchbot.devices import Device
from easy_switchbot.types import Command
import json


class InfraredDevice(Device):
    """parent class of infrared devices
    """

    def command_turn_on(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "turnOn",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_turn_off(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "turnOff",
                "commandType": "command",
                "parameter": "default",
            })
        )


class OtherInfrared(InfraredDevice):
    def __init__(
            self,
            device_id: str,
            device_name: str,
            remote_type: str,
            hub_device_id: str) -> None:
        """the constructor for InfraredDevice

        Args:
            device_id (str): the id of the device
            device_name (str): the name of the device
            remote_type (str): the type of the device
            hub_device_id (str): if the device has any parents, show their ids.
        """
        super().__init__(device_id, device_name, hub_device_id)
        self._remote_type = remote_type

    @property
    def remote_type(self) -> str: return self._remote_type

    def command_run(self, command: str) -> Command:
        """
        * command
        user-defined button name
        """
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": command,
                "commandType": "customize",
                "parameter": "default",
            })
        )


class AirConditionerInfrared(InfraredDevice):
    def command_set(self, temp: int, mode: int, fan_speed: int, power_state: str) -> Command:
        """
        * power_state on/off
        """
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "setAll",
                "commandType": "command",
                "parameter": f"{temp},{mode},{fan_speed},{power_state}",
            })
        )


class TVInfrared(InfraredDevice):
    def command_set_channel(self, channel: int) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "SetChannel",
                "commandType": "command",
                "parameter": channel,
            })
        )

    def command_volume_increase(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "volumeAdd",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_volume_decrease(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "volumeSub",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_channel_increase(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "channelAdd",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_channel_increase(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "channelSub",
                "commandType": "command",
                "parameter": "default",
            })
        )


class StreamerInfrared(TVInfrared):
    pass


class SetTopBoxInfrared(TVInfrared):
    pass


class DVDInfrared(InfraredDevice):
    def command_set_mute(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "setMute",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_fast_forward(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "FastForward",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_rewind(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "Rewind",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_next(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "Next",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_previous(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "Previous",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_pause(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "Pause",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_play(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "Play",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_stop(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "Stop",
                "commandType": "command",
                "parameter": "default",
            })
        )


class SpeakerInfrared(DVDInfrared):
    def command_volume_increase(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "volumeAdd",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_volume_decrease(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "volumeSub",
                "commandType": "command",
                "parameter": "default",
            })
        )


class FanInfrared(InfraredDevice):
    def command_swing(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "swing",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_timer(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "timer",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_set_speed_low(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "lowSpeed",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_set_speed_middle(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "middleSpeed",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_set_speed_high(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "highSpeed",
                "commandType": "command",
                "parameter": "default",
            })
        )


class LightInfrared(InfraredDevice):
    def command_increase_brightness(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "brightnessUp",
                "commandType": "command",
                "parameter": "default",
            })
        )

    def command_decrease_brightness(self) -> Command:
        return Command(
            device_id=self.device_id,
            command=json.dumps({
                "command": "brightnessDown",
                "commandType": "command",
                "parameter": "default",
            })
        )

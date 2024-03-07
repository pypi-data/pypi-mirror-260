from switchbot_api.devices import Device
import json


class InfraredDevice(Device):
    """parent class of infrared devices
    """

    def command_turn_on(self) -> str:
        return json.dumps({
            "command": "turnOn",
            "commandType": "command",
            "parameter": "default",
        })

    def command_turn_off(self) -> str:
        return json.dumps({
            "command": "turnOff",
            "commandType": "command",
            "parameter": "default",
        })


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

    def command_run(self, command: str) -> str:
        """
        * command
        user-defined button name
        """
        return json.dumps({
            "command": command,
            "commandType": "customize",
            "parameter": "default",
        })


class AirConditionerInfrared(InfraredDevice):
    def command_set(self, temp: int, mode: int, fan_speed: int, power_state: str) -> str:
        """
        * power_state on/off
        """
        return json.dumps({
            "command": "setAll",
            "commandType": "command",
            "parameter": f"{temp},{mode},{fan_speed},{power_state}",
        })


class TVInfrared(InfraredDevice):
    def command_set_channel(self, channel: int) -> str:
        return json.dumps({
            "command": "SetChannel",
            "commandType": "command",
            "parameter": channel,
        })

    def command_volume_increase(self) -> str:
        return json.dumps({
            "command": "volumeAdd",
            "commandType": "command",
            "parameter": "default",
        })

    def command_volume_decrease(self) -> str:
        return json.dumps({
            "command": "volumeSub",
            "commandType": "command",
            "parameter": "default",
        })

    def command_channel_increase(self) -> str:
        return json.dumps({
            "command": "channelAdd",
            "commandType": "command",
            "parameter": "default",
        })

    def command_channel_increase(self) -> str:
        return json.dumps({
            "command": "channelSub",
            "commandType": "command",
            "parameter": "default",
        })


class StreamerInfrared(TVInfrared):
    pass


class SetTopBoxInfrared(TVInfrared):
    pass


class DVDInfrared(InfraredDevice):
    def command_set_mute() -> str:
        return json.dumps({
            "command": "setMute",
            "commandType": "command",
            "parameter": "default",
        })

    def command_fast_forward() -> str:
        return json.dumps({
            "command": "FastForward",
            "commandType": "command",
            "parameter": "default",
        })

    def command_rewind() -> str:
        return json.dumps({
            "command": "Rewind",
            "commandType": "command",
            "parameter": "default",
        })

    def command_next() -> str:
        return json.dumps({
            "command": "Next",
            "commandType": "command",
            "parameter": "default",
        })

    def command_previous() -> str:
        return json.dumps({
            "command": "Previous",
            "commandType": "command",
            "parameter": "default",
        })

    def command_pause() -> str:
        return json.dumps({
            "command": "Pause",
            "commandType": "command",
            "parameter": "default",
        })

    def command_play() -> str:
        return json.dumps({
            "command": "Play",
            "commandType": "command",
            "parameter": "default",
        })

    def command_stop() -> str:
        return json.dumps({
            "command": "Stop",
            "commandType": "command",
            "parameter": "default",
        })


class SpeakerInfrared(DVDInfrared):
    def command_volume_increase(self) -> str:
        return json.dumps({
            "command": "volumeAdd",
            "commandType": "command",
            "parameter": "default",
        })

    def command_volume_decrease(self) -> str:
        return json.dumps({
            "command": "volumeSub",
            "commandType": "command",
            "parameter": "default",
        })


class FanInfrared(InfraredDevice):
    def command_swing() -> str:
        return json.dumps({
            "command": "swing",
            "commandType": "command",
            "parameter": "default",
        })

    def command_timer() -> str:
        return json.dumps({
            "command": "timer",
            "commandType": "command",
            "parameter": "default",
        })

    def command_set_speed_low() -> str:
        return json.dumps({
            "command": "lowSpeed",
            "commandType": "command",
            "parameter": "default",
        })

    def command_set_speed_middle() -> str:
        return json.dumps({
            "command": "middleSpeed",
            "commandType": "command",
            "parameter": "default",
        })

    def command_set_speed_high() -> str:
        return json.dumps({
            "command": "highSpeed",
            "commandType": "command",
            "parameter": "default",
        })


class LightInfrared(InfraredDevice):
    def command_increase_brightness() -> str:
        return json.dumps({
            "command": "brightnessUp",
            "commandType": "command",
            "parameter": "default",
        })

    def command_decrease_brightness() -> str:
        return json.dumps({
            "command": "brightnessDown",
            "commandType": "command",
            "parameter": "default",
        })

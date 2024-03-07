import hmac
import hashlib
import time
import base64
import uuid
import requests
from typing import Any, List

from easy_switchbot.devices import *
from easy_switchbot.infrared_devices import *
from easy_switchbot.types import Command

ROOT_URL = "https://api.switch-bot.com"


class SwitchbotAPI:
    """The class which accesses API.
    """

    def __init__(self, token: str, secret: str) -> None:
        """the constructor for SwitchbotAPI

        Args:
            token (str): access token (getting from mobile app)
            secret (str): secret key (getting from mobile app)
        """
        self._token: str = token
        self._secret: bytes = bytes(secret, "utf-8")

    def __create_headers(self) -> dict:
        """creating the header for authorization.

        Returns:
            dict: headers
        """
        time_ = str(int(round(time.time()*1000)))
        nonce = str(uuid.uuid4())

        sign = base64.b64encode(
            hmac.new(
                key=self._secret,
                msg=bytes(f"{self._token}{time_}{nonce}", "utf-8"),
                digestmod=hashlib.sha256).digest()
        )

        return {
            "Authorization": self._token,
            "sign": sign,
            "t": time_,
            "nonce": nonce,
            "Content-Type": "application/json; charset=utf-8"
        }

    def get(self, path: str) -> dict:
        """create GET request to API.
            * Access to the \"{ROOT_URL}/v1.1/{path}\" and return a response.

        Args:
            path (str): segment of URL

        Returns:
            dict: response of GET
        """
        headers = self.__create_headers()
        res = requests.get(
            f"{ROOT_URL}/v1.1/{path}", headers=headers)

        return res.json()

    def run(self, command: Command) -> dict:
        """create POST request to operate your device

        Args:
            command (Command): (device_id, the parameter json of operation)

        Returns:
            dict: response of POST
        """
        headers = self.__create_headers()
        res = requests.post(
            f"{ROOT_URL}/v1.1/devices/{command.device_id}/commands", headers=headers, data=command.command)
        return res.json()

    def status(self, device: SwitchbotDevice):
        res = self.get(f"devices/{device.device_id}/status")
        if not "statusCode" in res.keys() and res["statusCode"] != 100:
            print(f"Connection failed! (Code: {int(res['statusCode'])})")
            return None
        return res["body"]

    @property
    def devices(self) -> List[SwitchbotDevice]:
        ret = []

        json = self.get("devices")

        if not "statusCode" in json.keys() and json["statusCode"] != 100:
            print(f"Connection failed! (Code: {int(json['statusCode'])})")
            return

        devices = json["body"]["deviceList"]

        for device in devices:
            # detect the device type
            if device["deviceType"] == "Bot":
                ret.append(Bot(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Curtain":
                ret.append(Curtain(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                    curtain_device_ids=device["curtainDevicesIds"],
                    calibrate=device["calibrate"],
                    group=device["group"],
                    master=device["master"],
                    openDirection=device["openDirection"]
                ))
            elif device["deviceType"] == "Curtain 3":
                ret.append(Curtain3(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                    curtain_device_ids=device["curtainDevicesIds"],
                    calibrate=device["calibrate"],
                    group=device["group"],
                    master=device["master"],
                    openDirection=device["openDirection"]
                ))
            elif device["deviceType"] == "Hub":
                ret.append(Hub(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Hub Plus":
                ret.append(HubPlus(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Hub Mini":
                ret.append(HubMini(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Hub 2":
                ret.append(Hub2(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Meter":
                ret.append(Meter(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Meter Plus":
                ret.append(MeterPlus(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Outdoor Meter":
                ret.append(OutdoorMeter(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Lock":
                ret.append(Lock(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                    group=device["group"],
                    master=device["master"],
                    group_name=device["groupName"],
                    lock_device_ids=device["lockDevicesIds"],
                ))
            elif device["deviceType"] == "Keypad":
                ret.append(Keypad(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Keypad Touch":
                ret.append(KeypadTouch(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                    lock_device_id=device["lockDeviceId"],
                    key_list=device["keyList"],
                ))
            elif device["deviceType"] == "Remote":
                ret.append(Remote(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Motion Sensor":
                ret.append(MotionSensor(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Contact Sensor":
                ret.append(ContactSensor(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Ceiling Light":
                ret.append(CeilingLight(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Ceiling Light Pro":
                ret.append(CeilingLightPro(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Plug":
                ret.append(Plug(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Plug Mini (US)":
                ret.append(PlugMiniUS(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                    lock_device_id=device["lockDeviceId"],
                    key_list=device["keyList"],
                ))
            elif device["deviceType"] == "Plug Mini (JP)":
                ret.append(PlugMiniJP(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Strip Light":
                ret.append(StripLight(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Color Bulb":
                ret.append(ColorBulb(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Robot Vacuum Cleaner S1":
                ret.append(RobotVacuumCleanerS1(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Robot Vacuum Cleaner S1 Plus":
                ret.append(RobotVacuumCleanerS1Plus(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Humidifier":
                ret.append(Humidifier(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Indoor Cam":
                ret.append(IndoorCam(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Pan/Tilt Cam":
                ret.append(PanTiltCam(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Pan/Tilt Cam 2K":
                ret.append(PanTiltCam2K(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))
            elif device["deviceType"] == "Blind Tilt":
                ret.append(BlindTilt(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                    blind_tilt_device_ids=device["blindTiltDevicesIds"],
                    calibrate=device["calibrate"],
                    group=device["group"],
                    master=device["master"],
                    direction=device["direction"],
                    slide_position=device["slidePosition"],
                ))
            elif device["deviceType"] == "Battery Circulator Fan":
                ret.append(BatteryCirculatorFan(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    enable_cloud_service=device["enableCloudService"],
                    hub_device_id=device["hubDeviceId"],
                ))

        if not "infraredRemoteList" in json["body"].keys():
            return tuple(ret)

        devices = json["body"]["infraredRemoteList"]
        for device in devices:
            if device["remoteType"] == "Air Conditioner":
                ret.append(AirConditionerInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    hub_device_id=device["hubDeviceId"]
                ))
            elif device["remoteType"] == "TV":
                ret.append(TVInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    hub_device_id=device["hubDeviceId"]
                ))
            elif device["remoteType"] == "IPTV/Streamer":
                ret.append(StreamerInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    hub_device_id=device["hubDeviceId"]
                ))
            elif device["remoteType"] == "Set Top Box":
                ret.append(SetTopBoxInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    hub_device_id=device["hubDeviceId"]
                ))
            elif device["remoteType"] == "DVD":
                ret.append(DVDInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    hub_device_id=device["hubDeviceId"]
                ))
            elif device["remoteType"] == "Speaker":
                ret.append(SpeakerInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    hub_device_id=device["hubDeviceId"]
                ))
            elif device["remoteType"] == "Fan":
                ret.append(FanInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    hub_device_id=device["hubDeviceId"]
                ))
            elif device["remoteType"] == "Light":
                ret.append(LightInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    hub_device_id=device["hubDeviceId"]
                ))
            else:
                ret.append(OtherInfrared(
                    device_id=device["deviceId"],
                    device_name=device["deviceName"],
                    remote_type=device["remoteType"],
                    hub_device_id=device["hubDeviceId"]))

        return tuple(ret)

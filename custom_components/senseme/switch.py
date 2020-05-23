"""Support for Big Ass Fans SenseME occupancy sensor."""
import logging

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN, UPDATE_RATE

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up SenseME occupancy sensors."""
    if hass.data.get(DOMAIN) is None:
        hass.data[DOMAIN] = {}
    if hass.data[DOMAIN].get("switch_devices") is None:
        hass.data[DOMAIN]["switch_devices"] = []

    async def async_discovered_devices(devices: list):
        """Async handle a (re)discovered SenseME devices."""
        new_switches = []
        for device in devices:
            if device not in hass.data[DOMAIN]["switch_devices"]:
                if device.has_sensor:
                    device.refreshMinutes = UPDATE_RATE
                    hass.data[DOMAIN]["switch_devices"].append(device)
                    if device.is_fan:
                        fan_switch = HASensemeFanMotionSwitch(device)
                        new_switches.append(fan_switch)
                        _LOGGER.debug("Added new switch: %s", fan_switch.name)
                    if device.has_light:
                        light_switch = HASensemeLightMotionSwitch(device)
                        new_switches.append(light_switch)
                        _LOGGER.debug("Added new switch: %s", light_switch.name)
        if len(new_sensors) > 0:
            hass.add_job(async_add_entities, new_sensors)

    hass.data[DOMAIN]["discovery"].add_callback(async_discovered_devices)


class HASensemeFanMotionSwitch(SwitchEntity):
    """Representation of a Big Ass Fans SenseME fan motion switch."""

    def __init__(self, device):
        """Initialize the entity."""
        self.device = device
        self._name = device.name + " Motion Auto"

    async def async_added_to_hass(self):
        """Add data updated listener after this object has been initialized."""
        self.device.add_callback(self.async_write_ha_state)

    def turn_on(self, **kwargs) -> None:
        """Turn the fan motion auto mode on."""
        self.device.motion_fan_auto = True

    def turn_off(self, **kwargs) -> None:
        """Turn the fan motion auto mode off."""
        self.device.motion_fan_auto = False

    @property
    def name(self):
        """Get switch name."""
        return self._name

    @property
    def device_info(self):
        """Get device info for Home Assistant."""
        info = {
            "connections": {("mac", self.device.id)},
            "identifiers": {("token", self.device.network_token)},
            "name": self.device.name,
            "manufacturer": "Big Ass Fans",
            "model": self.device.model,
        }
        if self.device.fw_version:
            info["sw_version"] = self.device.fw_version
        return info

    @property
    def unique_id(self):
        """Return a unique identifier for this switch."""
        uid = f"{self.device.id}-FAN-SWITCH"
        return uid

    @property
    def should_poll(self) -> bool:
        """Switch state is pushed."""
        return False

    @property
    def device_state_attributes(self) -> dict:
        """Get the current state attributes."""
        attributes = {}
        if self.device.room_status:
            attributes["room"] = self.device.room_name
        return attributes

    @property
    def available(self) -> bool:
        """Return True if available/operational."""
        return self.device.connected

    @property
    def is_on(self) -> bool:
        """Return true if fan is auto."""
        return self.device.motion_fan_auto

class HASensemeLightMotionSwitch(SwitchEntity):
    """Representation of a Big Ass Fans SenseME light motion switch."""

    def __init__(self, device):
        """Initialize the entity."""
        self.device = device
        if self.device.is_fan:
            self._name = device.name + " Light Motion Auto"
        else:
            self._name = device.name + " Motion Auto"

    async def async_added_to_hass(self):
        """Add data updated listener after this object has been initialized."""
        self.device.add_callback(self.async_write_ha_state)

    def turn_on(self, **kwargs) -> None:
        """Turn the light motion auto mode on."""
        self.device.motion_light_auto = True

    def turn_off(self, **kwargs) -> None:
        """Turn the light motion auto mode off."""
        self.device.motion_light_auto = False

    @property
    def name(self):
        """Get switch name."""
        return self._name

    @property
    def device_info(self):
        """Get device info for Home Assistant."""
        info = {
            "connections": {("mac", self.device.id)},
            "identifiers": {("token", self.device.network_token)},
            "name": self.device.name,
            "manufacturer": "Big Ass Fans",
            "model": self.device.model,
        }
        if self.device.fw_version:
            info["sw_version"] = self.device.fw_version
        return info

    @property
    def unique_id(self):
        """Return a unique identifier for this switch."""
        uid = f"{self.device.id}-LIGHT-SWITCH"
        return uid

    @property
    def should_poll(self) -> bool:
        """Switch state is pushed."""
        return False

    @property
    def device_state_attributes(self) -> dict:
        """Get the current state attributes."""
        attributes = {}
        if self.device.room_status:
            attributes["room"] = self.device.room_name
        return attributes

    @property
    def available(self) -> bool:
        """Return True if available/operational."""
        return self.device.connected

    @property
    def is_on(self) -> bool:
        """Return true if fan is auto."""
        return self.device.motion_light_auto


"""Shared Entity definition for WeatherFlow Integration."""
from __future__ import annotations

import logging

from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.helpers.entity import DeviceInfo, Entity
import homeassistant.helpers.device_registry as dr
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from pyweatherflowrest.data import ObservationDescription, StationDescription

from .const import DEFAULT_ATTRIBUTION, DEFAULT_BRAND, DOMAIN

_LOGGER = logging.getLogger(__name__)


class WeatherFlowEntity(CoordinatorEntity, Entity):
    """Base class for unifi protect entities."""

    def __init__(
        self,
        weatherflowapi,
        coordinator: DataUpdateCoordinator,
        station_data: StationDescription,
        description,
    ):
        """Initialize the entity."""
        super().__init__(coordinator)

        if description:
            self.entity_description = description

        self.weatherflowapi = weatherflowapi
        self.coordinator = coordinator
        self.station_data = station_data
        self._device_data: ObservationDescription = self.coordinator.data
        self._device_value = getattr(
            self.coordinator.data, self.entity_description.key, None
        )
        self._attr_available = self.coordinator.last_update_success
        self._attr_unique_id = (
            f"{description.key}_{self.station_data.hub_serial_number}"
        )
        self._attr_device_info = DeviceInfo(
            manufacturer=DEFAULT_BRAND,
            via_device=(DOMAIN, self.station_data.hub_serial_number),
            connections={(dr.CONNECTION_NETWORK_MAC, station_data.hub_serial_number)},
            configuration_url=f"https://tempestwx.com/station/{self.station_data.key}/grid",
        )

    @property
    def extra_state_attributes(self):
        """Return common attributes"""
        return {
            ATTR_ATTRIBUTION: DEFAULT_ATTRIBUTION,
        }

    # async def async_added_to_hass(self):
    #     """When entity is added to hass."""
    #     self.async_on_remove(
    #         self.coordinator.async_add_listener(self.async_write_ha_state)
    #     )

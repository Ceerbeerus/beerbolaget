"""
Sensor platform for Beerbolaget.
"""
import logging
from datetime import timedelta

from custom_components.beerbolaget import (BEERBOLAGET_HANDLE,
                                           BEERBOLAGET_SENSORS)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

DEPENDENCIES = ['beerbolaget']

_LOGGER = logging.getLogger(__name__)

INTERVAL = timedelta(hours=1)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup Beerbolaget handle"""
    beer_handle = hass.data[BEERBOLAGET_HANDLE]

    for sensor in BEERBOLAGET_SENSORS:
        add_entities([release(beer_handle, sensor)], True)


class release(Entity):
    """Implementation of beerbolaget sensor"""
    def __init__(self, beer_handle, name):
        _LOGGER.debug("Beerbolaget sensor - __init__")
        self._attributes = {}
        self._beer_handler = beer_handle
        self._name = name
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return 'mdi:beer'

    @property
    def state(self):
        return self._state

    @property
    def state_attributes(self):
        return self._attributes

    @Throttle(INTERVAL)
    async def async_update(self):
        await self._beer_handler.get_store_info()
        await self._beer_handler.update_beers()
        await self._beer_handler.get_images()
        self._state = await self._beer_handler.get_release()
        self._attributes['release'] = await self._beer_handler.get_beers()

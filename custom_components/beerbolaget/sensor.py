"""
Sensor platform for Beerbolaget.
"""
import logging
from datetime import date, datetime, timedelta

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
        self._prev_release = None
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def friendly_name(self):
        return self._name

    @property
    def icon(self):
        return 'mdi:beer'

    @property
    def state(self):
        return self._state

    @property
    def unit_of_measurement(self):
        return "Release current week"

    @property
    def state_attributes(self):
        return self._attributes

    @Throttle(INTERVAL)
    async def async_update(self):
        await self._beer_handler.get_store_info()
        await self._beer_handler.update_beers()
        await self._beer_handler.get_images()
        await self._beer_handler.get_ratings()
        self._attributes['release_date'] = await self._beer_handler.get_release()
        self._attributes['beverages'] = await self._beer_handler.get_beers()
        self._attributes['local_store'] = await self._beer_handler.get_store()

        try:
            release_date = datetime.strptime(self._attributes['release_date'],
                                             '%Y-%m-%d').date()
            dt = date.today()
            start_of_week = dt - timedelta(days=dt.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            if (self._state and (release_date != self._prev_release) and
                (start_of_week < release_date < end_of_week)):
                self._state = False
            elif start_of_week < release_date < end_of_week:
                self._state = True
            else:
                self._state = False
            self._prev_release = release_date
        except:
          self._state = False

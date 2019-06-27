"""
A component which allows you to view the latest
batch of beer at the swedish Systembolaget.
For more details about this component,
please refer to the documentation at
https://github.com/Ceerbeerus/beerbolaget
"""
import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import EVENT_HOMEASSISTANT_START
from homeassistant.helpers.event import async_track_time_interval

__version__ = '0.1.0'

_LOGGER = logging.getLogger(__name__)

CONF_API_KEY = 'api_key'
CONF_IMAGE_URL = 'image_url'
CONF_RATEBEER = 'ratebeer'
CONF_STORE = 'store'
CONF_UNTAPPD = 'untappd'

DOMAIN = 'beerbolaget'

INTERVAL = timedelta(hours=1)

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_API_KEY, default=''): cv.string,
        vol.Optional(CONF_IMAGE_URL, default=''): cv.string,
        vol.Optional(CONF_RATEBEER, default=''): cv.string,
        vol.Optional(CONF_STORE, default=''): cv.string,
        vol.Optional(CONF_UNTAPPD, default=''): cv.string
    })
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config):
    """Set up this component"""
    conf_api_key = config[DOMAIN][CONF_API_KEY]
    conf_image_url = config[DOMAIN][CONF_IMAGE_URL]
    conf_ratebeer = config[DOMAIN][CONF_RATEBEER]
    conf_store = config[DOMAIN][CONF_STORE]
    conf_untappd = config[DOMAIN][CONF_UNTAPPD]

    if not conf_api_key:
        _LOGGER.error("API_KEY is required to use this component.")
        return False

    _LOGGER.info("if you have any issues with this component,"
                 " please report them here:"
                 " https://github.com/Ceerbeerus/beerbolaget")
    _LOGGER.debug("Version %s", __version__)

    latest_release = release(hass, conf_api_key, conf_image_url,
                             conf_ratebeer, conf_store, conf_untappd)

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START,
                               latest_release.check_release())

    async_track_time_interval(
                hass, latest_release.check_release, INTERVAL)

    async def check_release_service(call):
        await latest_release.check_release()

    hass.services.async_register(DOMAIN, 'check_release',
                                 check_release_service)
    return True


class release():
    def __init__(self, hass, conf_api_key, conf_image_url,
                 conf_ratebeer, conf_store, conf_untappd):
        _LOGGER.debug("Systembolaget - __init__")
        from beerbolaget.ha_custom.beer import beer_handler
        self.hass = hass
        self.api_key = conf_api_key
        self.beer_handler = beer_handler(self.api_key,
                                         conf_image_url,
                                         conf_ratebeer,
                                         conf_store,
                                         conf_untappd)
        self.release = None

    async def check_release(self, now=None):
        beers = []
        await self.beer_handler.get_store_info()
        await self.beer_handler.update_new_beers()
        await self.beer_handler.get_images()
        self.release = await self.beer_handler.get_release()
        beers = await self.beer_handler.get_beers()
        attributes = {
            'beer': beers
        }
        self.hass.states.async_set('sensor.beerbolaget_new_release',
                                   self.release, attributes)

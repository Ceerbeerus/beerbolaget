"""
A component which allows you to view the latest
batch of beer at the swedish Systembolaget.
For more details about this component,
please refer to the documentation at
https://github.com/Ceerbeerus/beerbolaget
"""
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.helpers.discovery import load_platform

__version__ = '0.2.6'

_LOGGER = logging.getLogger(__name__)

BEERBOLAGET_HANDLE = 'beerbolaget_handle'

BEERBOLAGET_SENSORS = [
    'beerbolaget'
]

BEERBOLAGET_TYPES = [
    'sensor'
]

CONF_API_KEY = 'api_key'
CONF_IMAGE_URL = 'image_url'
CONF_RATEBEER = 'ratebeer'
CONF_STORE = 'store'
CONF_UNTAPPD_CLIENT_ID = 'untappd_client_id'
CONF_UNTAPPD_SECRET = 'untappd_secret'

DOMAIN = 'beerbolaget'


CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_API_KEY, default=''): cv.string,
        vol.Optional(CONF_IMAGE_URL, default=''): cv.string,
        vol.Optional(CONF_RATEBEER, default=''): cv.string,
        vol.Optional(CONF_STORE, default=''): cv.string,
        vol.Optional(CONF_UNTAPPD_CLIENT_ID, default=''): cv.string,
        vol.Optional(CONF_UNTAPPD_SECRET, default=''): cv.string
    })
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config):
    """Set up this component"""
    conf_api_key = config[DOMAIN][CONF_API_KEY]
    conf_image_url = config[DOMAIN][CONF_IMAGE_URL]
    conf_ratebeer = config[DOMAIN][CONF_RATEBEER]
    conf_store = config[DOMAIN][CONF_STORE]
    conf_untappd_client_id = config[DOMAIN][CONF_UNTAPPD_CLIENT_ID]
    conf_untappd_secret = config[DOMAIN][CONF_UNTAPPD_SECRET]

    if not conf_api_key:
        _LOGGER.error("API_KEY is required to use this component.")
        return False

    _LOGGER.info("if you have any issues with this component,"
                 " please report them here:"
                 " https://github.com/Ceerbeerus/beerbolaget")
    _LOGGER.debug("Version %s", __version__)

    handle = beer_handle(conf_api_key,
                         conf_image_url,
                         conf_ratebeer,
                         conf_store,
                         conf_untappd_client_id,
                         conf_untappd_secret)

    hass.data[BEERBOLAGET_HANDLE] = handle

    for component in BEERBOLAGET_TYPES:
        load_platform(hass, component, DOMAIN, {}, config)

    return True


class beer_handle():
    def __init__(self,
                 conf_api_key,
                 conf_image_url,
                 conf_ratebeer,
                 conf_store,
                 conf_untappd_client_id,
                 conf_untappd_secret):
        _LOGGER.debug("Beerbolaget - __init__")
        from beerbolaget.beer import beer_handler
        self.beer_handle = beer_handler(conf_api_key,
                                        conf_image_url,
                                        conf_ratebeer,
                                        conf_store,
                                        conf_untappd_client_id,
                                        conf_untappd_secret)

    async def get_store_info(self):
        await self.beer_handle.get_store_info()

    async def update_beers(self):
        await self.beer_handle.update_new_beers()

    async def get_beers(self):
        return await self.beer_handle.get_beers()

    async def get_images(self):
        await self.beer_handle.get_images()

    async def get_ratings(self):
        await self.beer_handle.get_ratings()

    async def get_release(self):
        return await self.beer_handle.get_release()

    async def get_store(self):
        return await self.beer_handle.get_store()

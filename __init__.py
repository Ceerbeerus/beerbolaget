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

VERSION = '0.0.1'

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['beerbolaget==0.0.36b3']

CONF_API_KEY = 'api_key'
CONF_RATEBEER = 'ratebeer'
CONF_UNTAPPD = 'untappd'

DOMAIN = 'beerbolaget'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_API_KEY, default=''): cv.string,
        vol.Optional(CONF_RATEBEER, default=''): cv.string,
        vol.Optional(CONF_UNTAPPD, default=''): cv.string
    })
}, extra=vol.ALLOW_EXTRA)


async def async_setup(hass, config):
    """Set up this component"""
    conf_api_key = config[DOMAIN][CONF_API_KEY]
    conf_ratebeer = config[DOMAIN][CONF_RATEBEER]
    conf_untappd = config[DOMAIN][CONF_UNTAPPD]

    if not conf_api_key:
        _LOGGER.error("API_KEY is required to use this component.")
        return False

    _LOGGER.info("if you have any issues with this component,"
                 " please report them here:"
                 " https://github.com/Ceerbeerus/beerbolaget")
    _LOGGER.debug("Version %s", VERSION)

    latest_release = release(hass, conf_api_key, conf_ratebeer, conf_untappd)

    async def check_release_service(call):
        await latest_release.check_release()

    hass.services.async_register(DOMAIN, 'check_release',
                                 check_release_service)
    return True


class release():
    def __init__(self, hass, conf_api_key, conf_ratebeer, conf_untappd):
        _LOGGER.debug("Systembolaget - __init__")
        from beerbolaget.ha_custom.beer import beer_handler
        self.hass = hass
        self.api_key = conf_api_key
        self.beer = beer_handler(self.api_key, conf_ratebeer, conf_untappd)
        self.ratebeer = conf_ratebeer
        self.untappd = conf_untappd
        self.release = None

    async def check_release(self):
        beers = []
        await self.beer.update_new_beers()
        self.release = await self.beer.get_release()
        beers = await self.beer.get_beers()
        attributes = {
            'beer': beers
        }
        self.hass.states.async_set('sensor.beerbolaget_new_release',
                                   self.release, attributes)

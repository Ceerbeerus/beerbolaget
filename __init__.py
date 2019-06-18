"""
A component which allows you to view the latest batch of beer at the swedish Systembolaget.
For more details about this component, please refer to the documentation at
https://github.com/Ceerbeerus/systembolaget
"""
import logging
import os.path

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

VERSION = '0.0.1'

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['pybeerbolaget==0.0.8']

CONF_API_KEY = 'api_key'
CONF_RATEBEER = 'ratebeer'
CONF_UNTAPPD = 'untappd'

DOMAIN = 'beerbolaget'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_API_KEY, default=''):
            vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(CONF_RATEBEER, default=False): cv.boolean,
        vol.Optional(CONF_UNTAPPD, default=False): cv.boolean
    })
}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass, config):
    """Set up this component"""
    conf_api_key = config[DOMAIN][CONF_API_KEY]
    conf_ratebeer = config[DOMAIN][CONF_RATEBEER]
    conf_untappd = config[DOMAIN][CONF_UNTAPPD]

    _LOGGER.info('if you have any issues with this component, please report them here:'
                 ' https://github.com/Ceerbeerus/systembolaget')
    _LOGGER.debug('Version %s', VERSION)

    latest_release = release(hass, conf_api_key, conf_ratebeer, conf_untappd)

    async def check_release_service(call):
        await latest_release.check_release()

    hass.services.async_register(DOMAIN, 'check_release', check_release_service)
    return True


class release():
    def __init__(self, hass, conf_api_key, conf_ratebeer, conf_untappd):
        _LOGGER.debug('Systembolaget - __init__')
        from pybeerbolaget.ha_custom.beer import beer_handler
        self.hass = hass
        self.api_key = conf_api_key
        self.beer = beer_handler(self.api_key)
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
        self.hass.states.async_set('sensor.systembolaget_new_release', self.release, attributes)

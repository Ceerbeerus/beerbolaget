"""
A component which allows you to view the latest batch of goods at the swedish Systembolaget.
For more details about this component, please refer to the documentation at
https://github.com/Ceerbeerus/systembolaget
"""
import logging
import os.path

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

VERSION = '0.0.1'

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['pybeerbolaget==0.0.5']

CONF_API_KEY = 'api_key'
CONF_SHOW_BEER = 'show_beer'
CONF_SHOW_WINE = 'show_wine'
CONF_SHOW_WHISKY = 'show_whisky'

DOMAIN = 'systembolaget'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_API_KEY, default=''):
            vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(CONF_SHOW_BEER, default=False): cv.boolean,
        vol.Optional(CONF_SHOW_WINE, default=False): cv.boolean,
        vol.Optional(CONF_SHOW_WHISKY, default=False): cv.boolean
    })
}, extra=vol.ALLOW_EXTRA)

async def async_setup(hass, config):
    """Set up this component"""
    conf_api_key = config[DOMAIN][CONF_API_KEY]
    conf_beer = config[DOMAIN][CONF_SHOW_BEER]
    conf_wine = config[DOMAIN][CONF_SHOW_WINE]
    conf_whisky = config[DOMAIN][CONF_SHOW_WINE]

    _LOGGER.info('if you have any issues with this component, please report them here:'
                 ' https://github.com/Ceerbeerus/systembolaget')
    _LOGGER.debug('Version %s', VERSION)

    latest_release = release(hass, conf_api_key, conf_beer, conf_wine, conf_whisky)

    async def check_release_service(call):
        await latest_release.check_release()

    hass.services.async_register(DOMAIN, 'check_release', check_release_service)
    return True


class release():
    def __init__(self, hass, conf_api_key, conf_beer, conf_wine, conf_whisky):
        _LOGGER.debug('Systembolaget - __init__')
        from pybeerbolaget.ha_custom.beer import beer_handler
        self.hass = hass
        self.api_key = conf_api_key
        self.beer = beer_handler(self.api_key, True)
        self.wine = conf_wine
        self.whisky = conf_whisky
        self.release = None

    async def check_release(self):
        beers = []
        await self.beer.update_new_beers()
        self.release = await self.beer.get_release()
        beers = await self.beer.get_beers()
        attributes = {
            'beer': beers,
            'wine': self.wine,
            'whisky': self.whisky
        }
        self.hass.states.async_set('sensor.systembolaget_new_release', self.release, attributes)
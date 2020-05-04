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

from homeassistant.components.http import HomeAssistantView
from homeassistant.core import callback
from homeassistant.helpers.discovery import load_platform

__version__ = '0.4.0'

_LOGGER = logging.getLogger(__name__)

AUTH_CALLBACK_NAME = 'api:untappd'
AUTH_CALLBACK_PATH = '/api/untappd'

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
CONF_UNTAPPD_CALLBACK = 'untappd_callback'
CONF_UNTAPPD_CLIENT_ID = 'untappd_client_id'
CONF_UNTAPPD_SECRET = 'untappd_secret'

CONFIGURATOR_DESCRIPTION = 'To link your Untappd account, ' \
                           'click the link, login, and authorize:'
CONFIGURATOR_LINK_NAME = 'Link Untappd account'
CONFIGURATOR_SUBMIT_CAPTION = 'I authorized successfully'

DEFAULT_CACHE_PATH = '.untappd-token-cache'
DEFAULT_NAME = 'Beerbolaget - Untappd'
DOMAIN = 'beerbolaget'


CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_API_KEY, default=''): cv.string,
        vol.Optional(CONF_IMAGE_URL, default=''): cv.string,
        vol.Optional(CONF_RATEBEER, default=''): cv.string,
        vol.Optional(CONF_STORE, default=''): cv.string,
        vol.Optional(CONF_UNTAPPD_CALLBACK, default=''): cv.string,
        vol.Optional(CONF_UNTAPPD_CLIENT_ID, default=''): cv.string,
        vol.Optional(CONF_UNTAPPD_SECRET, default=''): cv.string
    })
}, extra=vol.ALLOW_EXTRA)


def request_configuration(hass, config, auth):
    """Request Untappd authorization."""
    configurator = hass.components.configurator
    hass.data[DOMAIN] = configurator.request_config(
        DEFAULT_NAME, lambda _: None,
        link_name=CONFIGURATOR_LINK_NAME,
        link_url=auth.get_url(),
        description=CONFIGURATOR_DESCRIPTION,
        submit_caption=CONFIGURATOR_SUBMIT_CAPTION)


class UntappdAuthCallbackView(HomeAssistantView):
    """Untappd Authorization Callback View."""
    requires_auth = False
    url = AUTH_CALLBACK_PATH
    name = AUTH_CALLBACK_NAME

    def __init__(self, auth, config):
        """Initialize."""
        self.config = config
        self.auth = auth

    @callback
    async def get(self, request):
        """Receive authorization token."""
        hass = request.app['hass']
        _code = request.query['code']
        try:
            await hass.async_add_executor_job(self.auth.cache_token, _code)
        except Exception as e:
            _LOGGER.error("couldn't write token: ({})".format(e))
            pass
        hass.async_add_job(
            setup, hass, self.config)


def setup(hass, config, discovery_info=None):
    """Set up this component"""
    from beerbolaget.rating import oauth
    conf_api_key = config[DOMAIN][CONF_API_KEY]
    conf_image_url = config[DOMAIN][CONF_IMAGE_URL]
    conf_ratebeer = config[DOMAIN][CONF_RATEBEER]
    conf_store = config[DOMAIN][CONF_STORE]
    conf_untappd_callback = config[DOMAIN][CONF_UNTAPPD_CALLBACK]
    conf_untappd_client_id = config[DOMAIN][CONF_UNTAPPD_CLIENT_ID]
    conf_untappd_secret = config[DOMAIN][CONF_UNTAPPD_SECRET]

    if not conf_api_key:
        _LOGGER.error("API_KEY is required to use this component.")
        return False

    auth = oauth(DEFAULT_CACHE_PATH,
                 conf_untappd_callback,
                 conf_untappd_client_id,
                 conf_untappd_secret)

    token = auth.get_token_from_cache()
    if (not token and conf_untappd_client_id and
            conf_untappd_secret and conf_untappd_callback):
        _LOGGER.info("no token; requesting authorization")
        hass.http.register_view(UntappdAuthCallbackView(
                                auth, config))
        request_configuration(hass, config, auth)
        return True
    if hass.data.get(DOMAIN):
        configurator = hass.components.configurator
        configurator.request_done(hass.data.get(DOMAIN))
        del hass.data[DOMAIN]

    _LOGGER.info("if you have any issues with this component,"
                 " please report them here:"
                 " https://github.com/Ceerbeerus/beerbolaget")
    _LOGGER.debug("Version %s", __version__)

    handle = beer_handle(conf_api_key,
                         conf_image_url,
                         conf_ratebeer,
                         conf_store,
                         conf_untappd_client_id,
                         conf_untappd_secret,
                         token)

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
                 conf_untappd_secret,
                 conf_untappd_token):
        _LOGGER.debug("Beerbolaget - __init__")
        from beerbolaget.beer import beer_handler
        self.beer_handle = beer_handler(conf_api_key,
                                        conf_image_url,
                                        conf_ratebeer,
                                        conf_store,
                                        conf_untappd_client_id,
                                        conf_untappd_secret,
                                        conf_untappd_token)

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

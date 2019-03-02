"""Config flow for Ambiclimate."""
import logging

from homeassistant import config_entries
from homeassistant.components.http import HomeAssistantView
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import (AUTH_CALLBACK_NAME, AUTH_CALLBACK_PATH, CONF_CLIENT_ID,
                    CONF_CLIENT_SECRET, DOMAIN, STORAGE_VERSION, STORAGE_KEY)

DATA_AMBICLIMATE_IMPL = 'ambiclimate_flow_implementation'

_LOGGER = logging.getLogger(__name__)


@callback
def register_flow_implementation(hass, client_id, client_secret):
    """Register a ambiclimate implementation.

    domain: Domain of the component responsible for the implementation.
    name: Name of the component.
    client_id: Client id.
    client_secret: Client secret.
    """
    if DATA_AMBICLIMATE_IMPL not in hass.data:
        hass.data[DATA_AMBICLIMATE_IMPL] = dict()

    hass.data[DATA_AMBICLIMATE_IMPL] = {
        CONF_CLIENT_ID: client_id,
        CONF_CLIENT_SECRET: client_secret,
    }


@config_entries.HANDLERS.register('ambiclimate')
class AmbiclimateFlowHandler(config_entries.ConfigFlow):
    """Handle a config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize flow."""
        self._registred_view = False

    async def async_step_user(self, user_input=None):
        """Handle external yaml configuration."""
        if self.hass.config_entries.async_entries(DOMAIN):
            return self.async_abort(reason='already_setup')

        config = self.hass.data.get(DATA_AMBICLIMATE_IMPL, {})

        if not config:
            _LOGGER.debug("no config")
            return self.async_abort(reason='no_config')

        return await self.async_step_auth()

    async def async_step_auth(self, user_input=None):
        """Handle a flow start."""
        if self.hass.config_entries.async_entries(DOMAIN):
            return self.async_abort(reason='already_setup')

        errors = {}

        if user_input is not None:
            errors['base'] = 'follow_link'

        if not self._registred_view:
            self.hass.http.register_view(AmbiclimateAuthCallbackView())
            self._registred_view = True

        oauth = await self._generate_oauth()

        return self.async_show_form(
            step_id='auth',
            description_placeholders={'authorization_url':
                                      oauth.get_authorize_url()},
            errors=errors,
        )

    async def async_step_code(self, code=None):
        """Received code for authentication."""
        if self.hass.config_entries.async_entries(DOMAIN):
            return self.async_abort(reason='already_setup')

        if code is None:
            return self.async_abort(reason='no_code')

        oauth = await self._generate_oauth()

        import ambiclimate
        try:
            token_info = await oauth.get_access_token(code)
        except ambiclimate.AmbiclimateOauthError:
            _LOGGER.error("Failed to get access token", exc_info=True)
            return self.async_abort(reason='access_token')

        store = self.hass.helpers.storage.Store(STORAGE_VERSION, STORAGE_KEY)
        await store.async_save(token_info)
        config = self.hass.data.get(DATA_AMBICLIMATE_IMPL, {}).copy()
        config['callback_url'] = '{}{}'.format(self.hass.config.api.base_url,
                                               AUTH_CALLBACK_PATH)

        return self.async_create_entry(
            title="Ambiclimate",
            data=config,
        )

    async def _generate_oauth(self):
        import ambiclimate
        config = self.hass.data.get(DATA_AMBICLIMATE_IMPL, {})
        clientsession = async_get_clientsession(self.hass)
        callback_url = '{}{}'.format(self.hass.config.api.base_url,
                                     AUTH_CALLBACK_PATH)
        oauth = ambiclimate.AmbiclimateOAuth(config.get(CONF_CLIENT_ID),
                                             config.get(CONF_CLIENT_SECRET),
                                             callback_url,
                                             clientsession)
        return oauth


class AmbiclimateAuthCallbackView(HomeAssistantView):
    """Ambiclimate Authorization Callback View."""

    requires_auth = False
    url = AUTH_CALLBACK_PATH
    name = AUTH_CALLBACK_NAME

    async def get(self, request):
        """Receive authorization token."""
        code = request.query.get('code')
        if code is None:
            return "No code"
        hass = request.app['hass']
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN,
                context={'source': 'code'},
                data=code,
            ))
        return "OK!"

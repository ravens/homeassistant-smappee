import logging
from datetime import datetime, timedelta
import voluptuous as vol
import json
import requests

from homeassistant.const import (
	CONF_NAME, CONF_HOST
)

from homeassistant.util import Throttle
from homeassistant.helpers.discovery import load_platform
from homeassistant.loader import get_component
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['requests==2.18.1']

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'Smappee'

DOMAIN = 'smappee'

DATA_SMAPPEE = 'SMAPPEE'


CONFIG_SCHEMA = vol.Schema({
	DOMAIN: vol.Schema({
		vol.Required(CONF_HOST): cv.string,
		vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string
	}),
}, extra=vol.ALLOW_EXTRA)



def setup(hass, config):
	host = config.get(DOMAIN).get(CONF_HOST)

	smappee = Smappee(host)

	hass.data[DATA_SMAPPEE] = smappee

	load_platform(hass, 'sensor', DOMAIN, {}, config)
	
	return True


class Smappee(object):
	def __init__(self, host):
		self.host = host
	
	def loadInstantaneous(self):
		url = 'http://' + self.host +'/gateway/apipublic/instantaneous'
		postdata = 'loadInstantaneous'
		headers = {'Content-type': 'application/json'}
		try:
			resp = requests.post(url=url, data=postdata, headers=headers)
			if resp:
				data = json.loads(resp.text)
				if data:
					result = {}
					for i in range(len(data)):
						if (data[i]["key"] == "phase0ActivePower"):
							result["power"] = data[i]["value"]
						if (data[i]["key"] == "phase0Cosfi"):
							result["cosphi"] = data[i]["value"]
					return result
			return False
		except Exception as e:
			_LOGGER.error("Retrieving instantaneous load failed, %s", e)
			return False
		

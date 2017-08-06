import logging
import math
from datetime import datetime, timedelta

from custom_components.smappee import DATA_SMAPPEE, DOMAIN
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
from homeassistant.util import dt as dt_util
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

SENSOR_PREFIX = 'Smappee'

SENSOR_TYPES = {
	'power': ['Power', 'mdi:power-plug', 'W'],
	'cosphi': ['Cosphi', 'mdi:power-plug', 'factor'],
}

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)


def setup_platform(hass, config, add_devices, discovery_info=None):
	""" setup the sensor platform for smappee """
	smappee = hass.data[DATA_SMAPPEE]
	dev = []
	for sensor in SENSOR_TYPES:
	   dev.append(SmappeeSensor(smappee, sensor))
	add_devices(dev)
	return True

class SmappeeSensor(Entity):
	"""Implementation of a Smappee sensor."""

	def __init__(self, smappee, sensor):
		"""Initialize the sensor."""
		self._smappee = smappee
		self._sensor = sensor
		self.data = None
		self._state = None
		self._timestamp = None
		self.update()


	@property
	def name(self):
		return "{} {}".format(SENSOR_PREFIX, SENSOR_TYPES[self._sensor][0])

	@property
	def icon(self):
		return SENSOR_TYPES[self._sensor][1]

	@property
	def state(self):
		return self._state

	@property
	def unit_of_measurement(self):
		return SENSOR_TYPES[self._sensor][2]

	@property
	def device_state_attributes(self):
		attr = {}
		attr['Last Update'] = self._timestamp
		return attr

	@Throttle(MIN_TIME_BETWEEN_UPDATES)
	def update(self):
		
		data = self._smappee.loadInstantaneous()

		if data:
			if SENSOR_TYPES[self._sensor][0] == 'Power':
				self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				self._state = round(float(data["power"]) / 1000, 2)

			elif SENSOR_TYPES[self._sensor][0] is 'Cosphi':
				self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				self._state = float(data["cosphi"])
			
			else:
				return None

		return None


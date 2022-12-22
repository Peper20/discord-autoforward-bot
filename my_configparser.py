from configparser import *
from json import loads
from json.decoder import JSONDecodeError




def my_get_item(self, key):
	if not self._parser.has_option(self._name, key):
		raise KeyError(key)

	response = self._parser.get(self._name, key)

	try:
		return loads(response)

	# except JSONDecodeError:
	except Exception as error:
		return response

SectionProxy.__getitem__ = my_get_item


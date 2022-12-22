import typing


from my_configparser import ConfigParser
from bot import My_bot


class Core:
	__bots_run_tasks = []
	__bots = []
	__reserved_property_fields: set[str, ...] = set()

	_config: ConfigParser = None


	def _fast_init(self):
		self._config = ConfigParser()

	def _controlled_init(self):
		self._config = ConfigParser()


	def __init__(
		self,
		fast_init: bool = True
	):
		if fast_init:
			self._fast_init


	@classmethod
	def read_config(
		cls,
		filenames: str | typing.Iterable,
		encoding: str = None,
	):

		cls._config.read(filenames, encoding=None)






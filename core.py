import typing


from asyncio import create_task
from my_configparser import ConfigParser
from bot import My_bot


class Core:
	__bots_run_tasks = []
	__bots = []
	__reserved_property_fields: set[str, ...] = set()

	_config: ConfigParser = None


	def read_config(
		self,
		filenames: str | typing.Iterable,
		encoding: str = None,
	):

		self._config.read(filenames, encoding=None)


	def _init_bots_list(self):
		self.__bots = [
			My_bot(
				self._config['forward_ids']['ids_from_forward'],
				self._config['forward_ids']['ids_to_forward'], 
				self._config['bot_settings']['token'], 
			)
		]


	def _fast_init(self):
		self._config = ConfigParser()
		self.read_config('config.ini')
		self._init_bots_list()

	def _controlled_init(self):
		self._config = ConfigParser()


	def __init__(
		self,
		fast_init: bool = True
	):
		if fast_init:
			self._fast_init()


	async def start(self):
		for bot in self.__bots:
			self.__bots_run_tasks.append(create_task(bot.start()))
		return [await task for task in self.__bots_run_tasks]


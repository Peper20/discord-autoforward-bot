import discord


from asyncio import create_task




class My_bot(discord.Bot):
	_ids_from_forward: list = None
	_ids_to_forward: list = None

	_places_from_forward: list = None
	_places_to_forward: list = None

	_places_ids_from_forward: list = None
	_places_ids_to_forward: list = None


	@staticmethod
	async def get_user_dm_id(place):
		return (place.dm_channel or await place.create_dm()).id

	@staticmethod
	async def get_simple_id(place):
		return place.id


	__ids_handlers = {discord.User: get_user_dm_id, discord.TextChannel: get_simple_id}

	async def get_place_id(self, place):
		return await self.__ids_handlers[type(place)](place)

	async def get_places(self, place_ids: list) -> tuple:
		places_response = []
		places_ids_response = []

		for place_id in place_ids:
			place = self.get_user(place_id) or self.get_channel(place_id)
			if place:
				places_response.append(place)
				places_ids_response.append(await self.get_place_id(place))

		return places_response, places_ids_response


	def __init__(self, ids_from_forward, ids_to_forward, **kwargs) -> None:
		self._ids_from_forward = ids_from_forward
		self._ids_to_forward = ids_to_forward

		if 'intents' not in kwargs:
			kwargs['intents'] = discord.Intents.all()

		super().__init__(**kwargs)


	async def _post_init(self, forward_from_ids: list, forward_to_ids: list) -> None:
		self._places_from_forward, self._places_ids_from_forward = await self.get_places(forward_from_ids)
		self._places_to_forward, self._places_ids_to_forward = await self.get_places(forward_to_ids)


	async def on_ready(self) -> None:
		await self._post_init(self._ids_from_forward, self._ids_to_forward)

		print(f'Bot connected as user {self.user} (id {self.user.id})')

	async def on_message(self, message):
		if message.channel.id in self._places_ids_from_forward and not message.author.bot:
			for place in self._places_to_forward:
				await place.send(message.content)
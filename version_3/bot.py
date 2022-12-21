import discord
import os
import requests


from PIL import Image
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

	__ids_handlers = {
		discord.User: get_user_dm_id,
		discord.TextChannel: get_simple_id,
	}

	@staticmethod
	async def save_file(url, index):
		data = requests.get(url, stream=True)
		name = f'trash_imgs/{index}.{url.split(".")[-1]}'

		with open(name, 'wb') as file:
			file.write(data.content)

		return name


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
			
			get_files_tasks = []
			for index, attachment in enumerate(message.attachments):
				get_files_tasks.append(
					create_task(
						self.save_file(attachment.url, index),
					)
				)

			send_messages_tasks = []
			for place in self._places_to_forward:
				send_messages_tasks.append(
					create_task(
						place.send(
							message.content,
							files=[discord.File(await file_name) for file_name in get_files_tasks],
						)
					)
				)

			for task in send_messages_tasks:
				await task

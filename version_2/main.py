import my_configparser


from bot import My_bot
from json import loads





config = my_configparser.ConfigParser()
config.read('config.ini')
bot = My_bot(config['forward_ids']['ids_from_forward'], config['forward_ids']['ids_to_forward'])


if __name__ == '__main__':
	bot.run(config['bot_settings']['token'])
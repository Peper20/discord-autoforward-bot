from core import Core




def _main():
	config = my_configparser.ConfigParser()
	config.read('config.ini')

	bot = My_bot(config['forward_ids']['ids_from_forward'], config['forward_ids']['ids_to_forward'])
	bot.run(config['bot_settings']['token'])


if __name__ == '__main__':
	_main()
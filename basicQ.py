from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
import os

exists = os.path.isfile('db.sqlite3')

bot = ChatBot('basicQ')
bot.set_trainer(ListTrainer)
if not exists:
	for each in os.listdir('basicChats'):
		chats = open('basicChats/'+each, 'r').readlines()
		bot.train(chats)
		exists = True
		#continue
while exists:
	request = input('\n> ')
	if "tarun kolla" in question.lower():
		response = bot.get_response(request)
		print('-', response)
	else:
		print('idk')
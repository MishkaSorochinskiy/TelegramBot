import telebot
from telebot.types import Message
from datetime import *
from random import randint

bot = telebot.TeleBot("702425430:AAGLU8_6u0sSor3Wk9eb64IT-6EYuVvmqnA")

players={}
current_date=0

def sorted_players(players:dict)->list:
    new_list=[]
    for i in players.keys():
        new_list.append([get_avarage(players[i][2],players[i][3]),i])
    return sorted(new_list,reverse=True)

def get_avarage(times,per)->float:
	if times==0:
		return 0
	else:
		return per/times

@bot.message_handler(commands=['help'])
def send_help(message):
	commands=["startgame - click this command in order to take part in the game"]
	commands.append("metodday - click this command to get to know your percentage of being 'Мох' today")
	commands.append("history - click this command to get info about all players and their avarage % of being 'Мох'")
	bot.reply_to(message, "{0}\n\n{1}\n\n{2}".format(commands[0],commands[1],commands[2]))

@bot.message_handler(commands=['startgame'])
def add_player(message:Message):
	if message.json['from']['id'] in players.keys():
		bot.reply_to(message,"Ooops, you are already in the game!!!")
	else:
		players[message.json['from']['id']]=[message.json['from']['first_name'],message.json['from']['last_name'],0,0,True]
		print(players)
	
@bot.message_handler(commands=['history'])
def show_history(message:Message):
    text=''
    place=1
    for i in sorted_players(players):
        text+="{0}.{1} {2} - {3}\n ".format(str(place),players[i[1]][0],players[i[1]][1],i[0])
        place+=1
    bot.reply_to(message,"List of losers for the whole time:\n\n"+text)

@bot.message_handler(commands=['metoday'])
def get_percentage(message:Message):
	global current_date
	if message.json['from']['id'] not in players.keys():
		bot.reply_to(message,"Who are you?? You did not register")
		return 
	if fromtimestamp(message.json['date']).day!=current_date:
		current_date=fromtimestamp(message.json['date']).day
		for i in players.keys():
			players[i][4]=True
	if players[message.json['from']['id']][4]==True:
		players[message.json['from']['id']][4]=False
		value=randint(0,100)
		bot.reply_to(message,"{0} % - you are Мох today".format(str(value)))
		players[message.json['from']['id']][2]+=1
		players[message.json['from']['id']][3]+=value
	else:
		bot.reply_to(message,"Sorry, you have already played today!!")



bot.polling(none_stop=True, interval=0)

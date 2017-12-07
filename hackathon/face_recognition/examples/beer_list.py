 #-*- coding: utf-8 -*-

import random



list_hi = ['Hey ', 'Hi ', 'Servus ']

list_pb = [', enjoy your beer!',', it seems that you like beer!',', Prost!']

list_pc = [', you had enough coffee. Now its time for a beer!',', finish your coffee quickly and get a beer!',', let me give you a beer instead of the coffee!']

list_pnb = [', why don´t you have a beer? Go and get one!',', you look thirsty. Let me give you a beer!',', im sure you will make one more beer!']

list_ub = ['Hey, nice to meet you! Enjoy your beer!','Hi man, cheers!','Hey, i don´t know you, but i like you because you drink beer!']

list_uc = ['Hey you, coffee time is over. Go and get a beer!','Hey you, finish that coffee quickly and drink a beer!','Hey there, beer tastes much better than coffee. Do you wanna try?']

list_unb = ['Hey, nice to meet you! Why don´t you have a beer? Go and get one!','Hey there, you look thirsty. Let me give you a beer!','Hello! I don´t know you but i want invite you for a beer!']


def generateDialogue(person,beer,coffee):
	if person and beer:
		return str(random.choice(list_hi)+ person + random.choice(list_pb))
	elif person and not beer and not coffee:
		return str(random.choice(list_hi)+ person+ random.choice(list_pnb))
	elif person and coffee and not beer:
		return str(random.choice(list_hi)+ person+ random.choice(list_pc))
	elif not person and beer:
		return str(random.choice(list_ub))
	elif not person and not beer and coffee:
		return str(random.choice(list_uc))
	elif not person and not beer and not coffee:
		return str(random.choice(list_unb))


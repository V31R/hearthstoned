# This is a sample Python script.
# This is a sample Python script.





# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup

import os
import pkg_resources
import time
from threading import Thread
russian_locale = "ruRU"
english_locale = "enUS"

language = russian_locale
card_art_url = "https://art.hearthstonejson.com/v1/render/latest/"+language+"/512x/"

name_set = set()

hero_minions = {
	"TB_BaconShop_HP_033t": True,
	"TB_BaconShop_HP_022t": True,
	"TB_BaconShop_HP_105t": True,
}


keyword_translate = {

	'AVENGE': 'Месть',
	'OVERKILL': 'Сверхурон',
	'WINDFURY': 'Неистовство ветра',
	'POISONOUS': 'Яд',
	'BATTLECRY': 'Боевой клич',
	'DIVINE_SHIELD': 'Божественный щит',
	'TAUNT': 'Провокация',
	'DEATHRATTLE': 'Предсмертный хрип',
	'REBORN': 'Перерождение',
	'CHARGE': 'Рывок',

}

types_translate = {

	'26': 'Все',
	'15': 'Демон',
	'24': 'Дракон',
	'20': 'Зверь',
	'17': 'Механизм',
	'14': 'Мурлок',
	'23': 'Пират',
	'43': 'Свинобраз',
	'18': 'Элементаль',
	" ": "Отсутствует",
}


def get_types_translate(str):
	if str is not None:
		return types_translate[str]
	return types_translate[" "]


rarity_translate = {

	'1': 'Обычная',
	'2': '??????',  # стандартный набор?
	'3': 'Редкая',
	'4': 'Эпическая',
	'5': 'Легендарная',

}


def get_locale_text_data(line, locale):
	start_index = line.find("<" + locale+">") + 1
	if start_index != 0:
		start_index = line.find(">", start_index) + 1
	end_index = line.find("</"+locale+">", start_index)
	if end_index == -1:
		end_index = len(line)
	string = ""
	i = start_index
	while i < end_index:
		string += line[i]
		i += 1
	return string


__version__ = pkg_resources.require("hearthstone_data")[0].version


def get_bountydefs_path():
	return pkg_resources.resource_filename("hearthstone_data", "BountyDefs.xml")


def get_carddefs_path():
	return pkg_resources.resource_filename("hearthstone_data", "CardDefs.xml")


def get_mercenarydefs_path():
	return pkg_resources.resource_filename("hearthstone_data", "MercenaryDefs.xml")


def get_strings_file(locale=language, filename = "GLOBAL.txt"):
	path = os.path.join("Strings", locale, filename)

	return pkg_resources.resource_filename("hearthstone_data", path)

def collect_cards_data_localised(locales=[language]):
	data = []
	with open(get_carddefs_path(), "r", encoding="UTF8") as file:
		flag = False
		foundTeg = False
		for line in file:
			add = True
			if line.find("LocString") != -1:
				flag = True
				data.append(line)
			if flag:
				in_file = False
				for locale in locales:
					if line.find(locale) != -1:
						in_file = True
						break
				if not in_file:
					add = False
					foundTeg = True
					if(line.find("/")):
						foundTeg = False
			if flag and line.find("/Tag") != -1:
				flag = False
				add = True
			if add and not foundTeg:
				data.append(line)
		file.close()
	return data


def collect_bg_cards_data_localised(filename, locales=[language]):
	cardTag = "Entity"
	data = []
	entity = []
	with open(filename, "r", encoding="UTF8") as file:
		flag=False
		foundTeg = False
		bg_card = False
		for line in file:
			add = True
			if line.find('TECH_LEVEL') != -1:
				bg_card = True
			if line.find("LocString") != -1:
				flag = True
				entity.append(line)
			if flag:
				in_file = False
				for locale in locales:
					if line.find(locale) != -1:
						in_file = True
						break
				if not in_file:
					add = False
					foundTeg = True
					if line.find("/"):
						foundTeg = False
			if flag and line.find("/Tag") != -1:
				flag = False
				add = True
			if add and not foundTeg:
				entity.append(line)

			if line.find("</"+cardTag) != -1:
				if bg_card:
					for l in entity:
						data.append(l)
					bg_card = False
				entity = []

		file.close()
	return data


def collect_and_load_cards_data(locales=[language]):
	data = collect_cards_data_localised(locales_in_file)
	filename = "cards"
	for name in locales_in_file:
		filename += "_" + name
	filename += ".xml"
	resultFile = open(filename, mode="w", encoding="UTF8")
	for line in data:
		resultFile.write(line)
	resultFile.close()
	print("Successfully collected " +str(len(data))+" strings to " + filename)
	return [data,filename]

def collect_and_load_bg_cards_data(filename, locales=[language]):
	data = collect_bg_cards_data_localised(filename, locales_in_file)
	bg_filename = "bg_cards"
	for name in locales_in_file:
		bg_filename += "_" + name
	bg_filename += ".xml"
	resultFile = open(bg_filename, mode="w", encoding="UTF8")
	for line in data:
		resultFile.write(line)
	resultFile.close()
	print("Successfully collected " +str(len(data))+" strings to " + bg_filename)
	return [data,bg_filename]

class Card:
	def __init__(self):
		self.data=dict()

	def get_CardID(self):
		return self.data["CardID"]


def get_tag_data(line):
	start_index = line.find("\"") + 1
	start_index = line.find("\"", start_index) + 1 # skip tag_id
	start_index = line.find("\"", start_index) + 1  # find name
	end_index = line.find("\"", start_index )
	name=""
	i = start_index
	while i < end_index:
		name += line[i]
		i += 1
	start_index = line.find("\"", end_index+1)+1 # skip type value
	start_index = line.find("\"", start_index ) +1 #
	start_index = line.find("\"", start_index)+1  # find value
	end_index = line.find("\"", start_index)
	value = ""
	i = start_index
	while i < end_index:
		value += line[i]
		i += 1
	return [name,value]


def parse_cards(filename, locale=language):
	cards=[]
	with open(filename, "r", encoding="UTF8") as file:
		cardTag="Entity"
		attrTag="Tag"
		get_data=False
		name_data=None
		card=None
		for line in file:
			if (line.find("<" + cardTag) != -1):
				get_data = False
			if get_data:
				card.data[name_data]+=get_locale_text_data(line,locale)
				if(line.find("/"+locale)!=-1):
					get_data=False
				continue
			if(line.find("<"+cardTag)!=-1):

				card= Card()
				start_index=line.find("\"")+1
				end_index = line.find("\"",start_index+1)
				i=start_index
				card.data["CardID"]=""
				while i < end_index:
					card.data["CardID"]+=line[i]
					i+=1
				start_index = line.find("\"",i+1) + 1
				end_index = line.find("\"", start_index + 1)
				i = start_index
				card.data["ID"] = ""
				while i < end_index:
					card.data["ID"] += line[i]
					i += 1

			if(line.find("<"+attrTag)!=-1):# or line.find("<Referenced"+attrTag)!=-1):

				name, value=get_tag_data(line)
				card.data[name]=value
				if(name=="CARDNAME" or name=="CARDTEXT"or name=="FLAVORTEXT"):
					get_data=True
					name_data=name
					card.data[name_data]=""
					continue
				elif(name=="ARTISTNAME"):
					start_index = line.find(">") + 1
					end_index = line.find("</", start_index)
					i = start_index
					card.data[name] = ""
					while i < end_index:
						card.data[name] += line[i]
						i += 1
				elif (name.isdigit() and line.find("Card")!=-1):
					start_index = line.find("\"") + 1
					end_index = line.find("\"", start_index + 1)
					i = start_index
					value=""
					while i < end_index:
						value += line[i]
						i += 1
					card.data["HERO_POWER"]=value

			if(line.find("/"+cardTag)!=-1):
				if(card!=None):
					if(card.data.get('CARDTYPE')==4):
						if(not card.data.get('ATK')):
							card.data['ATK']='0'
					cards.append(card)
					#print("Inserted ", cards[len(cards)-1].data)
				card=None

		file.close()
		print("Was collected " + str(len(cards))+" cards from " + filename+".")
		return cards

def collect_bg_cards(filename, locale=language):
	return [card for card in parse_cards(filename, locale) if card.data.get("TECH_LEVEL")]

def collect_hero(filename, locale=language):
	return [card for card in parse_cards(filename, locale) if card.data.get("HERO_POWER")]

def collect_bg_hero(filename, locale=language):
	return [card for card in parse_cards(filename, locale)
			if card.data.get("HERO_POWER") and card.get_CardID().find("Bacon")!=-1]

def collect_bg_cards_by_cards(cards):
	return [card for card in cards if card.data.get("TECH_LEVEL") and
			(card.data.get("IS_BACON_POOL_MINION") or hero_minions.get(card.get_CardID()))]

def collect_hero_by_cards(cards):
	return [card for card in cards if card.data.get("HERO_POWER")]

def collect_bg_hero_by_cards(cards):
	return [card for card in cards
			if card.data.get("HERO_POWER") is not None and card.get_CardID().find("_HERO_") != -1
			and card.get_CardID().find("_SKIN_") == -1 and card.data.get('BACON_HERO_CAN_BE_DRAFTED') is not None]


def is_card_in_cards(cards, cardID):
	for card in cards:
		if card.get_CardID() == cardID:
			return True
	return False

def get_card_in_cards(cards, cardID):
	for card in cards:
		if card.get_CardID() == cardID:
			return card
	return None

def collect_hero_abilities(heroes, cards):
	abilities = []
	for hero in heroes:
		ability=get_card_in_cards(cards, hero.data.get("HERO_POWER"))
		if ability !=None:
			if not ability.data.get("COST"):
				if ability.data.get("HIDE_COST"):
					ability.data["COST"] = -int(ability.data.get("HIDE_COST"))
					ability.data.pop("HIDE_COST")
				else:
					ability.data["COST"]=0
			else:
				ability.data["COST"]=int(ability.data["COST"])
			if not get_card_in_cards(abilities,ability.get_CardID()):
				abilities.append(ability)

	return abilities


def download_art(card, output_folder):
	p = requests.get(card_art_url + card.get_CardID() + ".png")
	out = open(output_folder + "/" + card.get_CardID().lower() + ".png", "wb")
	out.write(p.content)
	out.close()

def download_arts_in_range(cards, output_folder, start, end):
	i=start
	while(i<end):
		download_art(cards[i], output_folder)
		i+=1

def make_file_with_bg_cards(filename,cards,locale=language, output_folder="cards_art"):
	data = collect_bg_cards_by_cards(cards)
	print("Successfully found " + str(len(data)) + " battlegrounds cards from " + filename + ".")
	start_time=time.time()
	threads=[]
	thread_number=8
	for i in range(thread_number):
		start=i*int(len(data)/thread_number)
		end=(i+1)*int(len(data)/thread_number)
		if(i==thread_number-1):
			end+=len(data)%thread_number
		threads.append(Thread(
			target=download_arts_in_range,
			args=[data,
			output_folder,
			start,
			end
			]
		))
	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()

	print("Successfully download " + str(len(data)) + " cards to " +
		output_folder + " in %s seconds." % (time.time()-start_time))
	return data

def make_file_with_bg_heroes_and_abilities(filename, card_data,locale=language, output_folder="heroes_art"):
	bg_heroes_abilities=collect_bg_hero_by_cards(card_data)
	bg_heroes_abilities+=collect_hero_abilities(bg_heroes_abilities,card_data)
	print("Successfully found " + str(len(bg_heroes_abilities)) + " battlegrounds heroes with abilities from " + filename + ".")
	start_time=time.time()
	threads=[]
	thread_number=8
	for i in range(thread_number):
		start=i*int(len(bg_heroes_abilities)/thread_number)
		end=(i+1)*int(len(bg_heroes_abilities)/thread_number)
		if(i==thread_number-1):
			end+=len(bg_heroes_abilities)%thread_number
		threads.append(Thread(
			target=download_arts_in_range,
			args=[bg_heroes_abilities,
			output_folder,
			start,
			end
			]
		))
	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()

	print("Successfully download " + str(len(bg_heroes_abilities)) + " heroes cards to " +
		output_folder + " in %s seconds." % (time.time()-start_time))
	return data

def make_db_bg_hero(heroes, abilities):

	hero_attr=["CardID", "CARDNAME","HEALTH"]
	ability_attr = ["CardID", "CARDNAME",'CARDTEXT',"COST"]
	db_hero = []
	for hero in heroes:
		ability = get_card_in_cards(abilities, hero.data.get("HERO_POWER"))
		if ability!=None:
			new_hero = Card()
			for attr in hero_attr:
				new_hero.data[attr]=hero.data[attr]
			for attr in ability_attr:
				new_hero.data[attr + "_HP"]=ability.data[attr]

			db_hero.append(new_hero)

	return db_hero


	pass




from getpass import getpass

from mysql.connector import connect, Error
import tabulate

from tkinter import *
from functools import partial
from tkinter import ttk # Модули пакета импортируются отдельно
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from typing import List, Optional, Tuple, Callable


class service_database:
	def __init__(self):
		try:
			self.connection = connect(host="localhost",user=login,password=password)
		except Error as e:
			raise
		self.cursor=self.connection.cursor()

	def get_connection(self):
			return self.connection

	def get_cursor(self):
			return self.cursor

	def print_query_result(self):
		print(tabulate.tabulate(self.cursor, [i[0] for i in self.cursor.description], tablefmt='grid'))

	def execute(self, query):
		try:
			self.cursor.execute(query)
		except Error as e:
			raise
		return self

	def execute_multi_insert(self, table, field_names,field_values):
		query = "insert into " + table
		query+=" ( "
		i=0
		for name in field_names:

			query+=name
			if(i<len(field_names)-1):
				query+=", "
			i+=1
		query+=" ) \nvalues \n"


		j = 0
		for values in field_values:
			i = 0
			query += " ( "
			for value in values:
				if(value!=None):
					temp = value
					if (type(value) == str):
						query += "'"
						if (temp.find("'") != -1):
							end = value.find("'")
							temp = ""
							for ind in range(0, end + 1):
								temp += value[ind]
						# temp+="'"
							for ind in range(end, len(value)):
								temp += value[ind]
						query += temp
					else:
						query += str(value)
				else:
					query+="NULL"
				if (type(value) == str):
					query += "'"
				if (i < len(values) - 1):
					query += ", "
				i += 1
			query += " )"
			if (j < len(field_values) - 1):
				query += ",\n"
			j += 1
		query+=";"
		try:
			#print(query)
			self.cursor.execute(query)
		except Error as e:
			raise
		return self.cursor

	def execute_insert(self, table, field_value, select_q =False, select_query=None):
		query = "insert into " + table

		if(not select_q):
			query+=" ( "
			values=[]
			i=0
			for name, value in field_value.items():
				values.append(value)
				query+=name
				if(i<len(field_value)-1):
					query+=", "
				i+=1
			query+=" ) \nvalues \n"

			query += " ( "

			i = 0
			for value in values:
				temp=value
				if(type(value)==str):
					query+="'"
					if(temp.find("'")!=-1):
						end=value.find("'")
						temp=""
						for ind in range(0,end+1):
							temp+=value[ind]
						#temp+="'"
						for ind in range(end, len(value)):
							temp += value[ind]

					query += temp
				else:
					query += str(value)
				if (type(value) == str):
					query += "'"
				if (i < len(values) - 1):
					query += ", "
				i += 1
			query += " );\n"
		try:
			print(query)
			self.cursor.execute(query)
		except Error as e:
			raise
		return self.cursor

	def execute_select(self, columns, tables, columns_alias=None, joins=None, where=None, group_by = None, having=None,
					   order_by = None, distinct=False, limit = None):
		query=self.make_query(columns, tables, columns_alias, joins, where, group_by, having, order_by, distinct, limit)
		try:
			self.cursor.execute(query)
		except Error as e:
			raise
		return self.cursor

	def make_query(self, columns, tables, columns_alias=None,joins=None, where=None, group_by = None, having=None,
				   order_by = None, distinct=False, limit = None ):
		query = 'select '
		if(distinct):
			query+='distinct '
		i = 0
		for column in columns:
			query += column
			if(columns_alias!=None):
				query += ' as \''
				query+=columns_alias[i]
				query += '\''
			if (i + 1 < len(columns)):
				query += ', '
			i += 1
		query += ' from '

		i = 0
		for table in tables:
			query += table
			if (i + 1 < len(tables)):
				query += ', '
			i += 1

		query += '\n'

		if (joins != None):
			for join in joins:
				query += join[0]
				query += ' join '
				query += join[1]
				query += ' on '
				query += join[2]
				query += '\n'

		if (where != None):
			query += 'where '
			query += where
			query += '\n'

		if (group_by != None):
			query += 'group by '
			i = 0
			for column in group_by:
				query += column
				if (i + 1 < len(group_by)):
					query += ', '
				i += 1
			query += '\n'
		if (having != None):
			query += 'having '
			query += having
			query += '\n'

		if (order_by != None):
			query += 'order by '
			i = 0
			for column in order_by:
				query += column
				if (i + 1 < len(order_by)):
					query += ', '
				i += 1
			query += '\n'

		if (limit != None):

			query += 'limit '
			query += str(limit)
			query += '\n'
		return query

background_color='#2b2b2b'
button_color='#3c3f41'
fill_color='#afb1b3'



class Graphic_interface(Frame):
	def __init__(self, root, bg_cards, bg_heroes =None):
		super().__init__(root)
		self.bg_cards=bg_cards
		self.bg_heroes = bg_heroes
		self.top_frame=Frame(bg=background_color)
		self.middle_frame = Frame(bg=background_color)
		self.bottom_frame = Frame(bg=background_color)
		self.first_top = Frame(self.top_frame,bg=background_color)
		self.second_top = Frame(self.top_frame, bg=background_color)
		self.tree=None
		self.search_tree=None
		self.db_service=service_database()
		self.current_choose_hero={1:None,2:None,3:None,4:None,}
		self.current_opponent_heroes = {1: None, 2: None, 3: None, 4: None,5:None, 6: None, 7: None}
		self.current_cards = {1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None}
		self.input_choose_hero=None
		self.input_opponent_heroes = None
		self.input_cards = None
		self.result_battle = {'Номер Героя': None, 'Место': None, 'Рейтинг': None, 'BattleTag': None}
		self.input_result_battle = None
		self.card_race_in_battle= {}
		for key, name in types_translate.items():
			self.card_race_in_battle[name]=None;
		self.card_race_in_battle.pop('Все')
		self.card_race_in_battle.pop('Отсутствует')
		self.card_race_in_battle=[name for name, value in self.card_race_in_battle.items()]
		self.current_race_list= set()
		self.card_race_button={}
		for race in self.card_race_in_battle:

			self.card_race_button[race]=Button(
				self.middle_frame,
				text=race,
				width=20,
				command=partial(self.add_card_race, race),
				bg=button_color,
				fg=fill_color,
				bd=1,
				compound=TOP,
				padx=10
			)
			self.card_race_button[race].pack(side=TOP)

		self.db_service.execute("select * from hs.gets_heroes_stats;")
		#print(self.db_service.get_cursor().fetchall())
		ser_data_array=[]
		for row in self.db_service.get_cursor().fetchall():
			CARDID, name, win_rate, avg_position, selection_frequency, health, hp_name, hp_text, hp_cost, hp_id, rate_ch, bt, id = row

			ser_data={}
			ser_data['cardID']=CARDID
			ser_data['heroName']=name
			ser_data['heroPowerName'] = hp_name
			ser_data['heroPowerText'] = hp_text
			ser_data['heroPowerCost'] = int(hp_cost)
			ser_data['heroPowerID'] = hp_id
			if win_rate is not None:
				ser_data['winRate']=float(win_rate)
			else:
				ser_data['winRate'] = None

			if avg_position is not None:
				ser_data['averagePosition'] = float(avg_position)
			else:
				ser_data['averagePosition'] = None

			if selection_frequency is not None:
				ser_data['selectionFrequency'] = float(selection_frequency)
			else:
				ser_data['selectionFrequency'] = None

			if health is not None:
				ser_data['health'] = int(health)
			else:
				ser_data['health'] = None

			if rate_ch is not None:
				ser_data['ratingChange'] = int(rate_ch)
			else:
				ser_data['ratingChange'] = None
			ser_data_array.append(ser_data)
		print(ser_data_array)

		ser_data_array = []
		self.db_service.execute("select * from hs.gets_cards_stats;")
		for row in self.db_service.get_cursor().fetchall():
			CARDID, name, win_rate, avg_pos, attack, health, tech_level, card_text, c_race, heroID, hero_name, flavor_text, bt, id = row

			ser_data = {}
			ser_data['cardID'] = CARDID
			ser_data['cardName'] = name
			ser_data['cardRace'] = c_race
			ser_data['attack'] = int(attack)
			ser_data['health'] = int(health)
			ser_data['techLevel'] = int(tech_level)
			if win_rate is not None:
				ser_data['winRate'] = float(win_rate)
			else:
				ser_data['winRate'] = None
			if avg_pos is not None:
				ser_data['averagePosition'] = float(avg_pos)
			else:
				ser_data['averagePosition'] = None

			if card_text is not None:
				ser_data['cardText'] = card_text
			else:
				ser_data['cardText'] = None

			if heroID is not None:
				ser_data['heroID'] = heroID
			else:
				ser_data['heroID'] = None
			if hero_name is not None:
				ser_data['heroName'] = hero_name
			else:
				ser_data['heroName'] = None
			if flavor_text is not None:
				ser_data['flavorText'] = flavor_text
			else:
				ser_data['flavorText'] = None
			ser_data_array.append(ser_data)
		print(ser_data_array)
		self.menu = {
			'Типы существ': lambda service: service.execute_select(
				columns=['name'],
				columns_alias=['Название'],
				tables=['hs.card_race']
			),
			'Ключевые слова': lambda service: service.execute_select(
				columns=['name'],
				columns_alias=['Название'],
				tables=['hs.keyword']
			),
			'Карты': lambda service: service.execute_select(
				columns=['CARDID', 'blizzard_id','card.name', 'card_race.name'],
				#columns_alias=['cArd', 'Дата начала работы', 'Количество проданных машин','Автосалон'],
				tables=['hs.card'],
				joins=[['inner','hs.card_race','hs.card_race.card_race_id = hs.card.card_race_id']]
			),
			'Герои': lambda service: service.execute_select(
				columns=['CARDID', 'name', 'health', 'hp_id','hp_name','hp_cost'],
				# columns_alias=['cArd', 'Дата начала работы', 'Количество проданных машин','Автосалон'],
				tables=['hs.hero'],
				#joins=[['inner', 'hs.card_race', 'hs.card_race.card_race_id = hs.card.card_race_id']]
			),
			'Игроки': lambda service: service.execute_select(
				columns=['BattleTag'],
				# columns_alias=['cArd', 'Дата начала работы', 'Количество проданных машин','Автосалон'],
				tables=['hs.player'],
				# joins=[['inner', 'hs.card_race', 'hs.card_race.card_race_id = hs.card.card_race_id']]
			),
			'Матчи': lambda service: service.execute_select(
				columns=['battle_id','battle_tag', 'position', 'name', 'rate_points'],
				# columns_alias=['cArd', 'Дата начала работы', 'Количество проданных машин','Автосалон'],
				tables=['hs.player'],
				joins=[['inner', 'hs.battle_result', 'hs.battle_result.player_id = hs.player.player_id'],
					   ['inner', 'hs.hero', 'hs.battle_result.hero_id = hs.hero.hero_id']]
			),

		}
		toolbar = Frame(self.first_top, bg=background_color)
		searchbar = Frame(self.middle_frame,bg=background_color)
		editbar = Frame(self.second_top,bg=background_color)

		for item in self.menu.items():
			name=item[0]
			# Создаём каждый объект и упаковываем их на toolbar
			self.set_buttonPosition(toolbar, name, partial(self.__show_result, item[1],self.second_top), LEFT)

		# Устанавливаем toolbar на экран



		edit_string="Вставка в таблицы:"
		text=Text(editbar, width=len(edit_string), height=1, bg=background_color,bd=0, padx=10,fg=fill_color)
		text.insert(1.0,edit_string)
		text.config(state="disabled")
		#text['state']='disabled'
		text.pack(side=TOP)

		edit_data_button = {
			'Карты':partial(self.insert_in_cards,self.bg_cards),
			'Герои':partial(self.insert_in_heroes,self.bg_heroes),
		}

		for name, function in edit_data_button.items():
			self.set_buttonPosition(editbar, name, function, TOP)

		self.texts_fields = []
		search_data={
			'Поиск по картам':partial(self.search_cards,searchbar),
			'Поиск по героям':partial(self.search_heroes,searchbar)
		}

		self.main_workplace = Frame(bg=background_color)
		self.main_workplace.pack(side=TOP, fill=X)



		#self.texts_fields = []
		self.search_trees=[]
		for name, function in search_data.items():
			self.set_passiveTextPosition(searchbar,name, TOP)

			self.texts_fields.append(Text(searchbar, width=len(name), height=1, padx=10,bg=fill_color))
			self.texts_fields[len(self.texts_fields)-1].pack(side=TOP)
			self.set_buttonPosition(searchbar, name, function, TOP)


		name='Результат'

		self.tree = ttk.Treeview(self.second_top, columns=[name], height=25, show='headings')
		self.tree.column(name, width=200, anchor=CENTER)
		self.tree.heading(name, text=name)
		self.tree.pack(side=TOP)

		self.search_tree=ttk.Treeview(searchbar, columns=[name], height=10, show='headings')
		self.search_tree.column(name, width=200, anchor=CENTER)
		self.search_tree.heading(name, text=name)
		self.search_tree.pack(side=TOP)


		temp_frame=Frame(self.middle_frame, bg=background_color)
		Button(
			temp_frame,
			text='Найти справа',
			width=20,
			command=partial(self.set_focus),
			bg=button_color,
			fg=fill_color,
			bd=1,
			compound=TOP,
			padx=10
		).pack(side=TOP)

		self.hero_choose_frame=Frame(self.bottom_frame, bg=background_color)

		self.input_choose_hero=[]
		self.set_passiveTextPosition(self.bottom_frame, "Выбор героев", TOP)
		for name, value in self.current_choose_hero.items():
			string='Герой %s:'%str(name)
			frame=Frame(self.bottom_frame, bg=background_color)
			self.set_passiveTextPosition(frame,string,LEFT)
			self.input_choose_hero.append(Text(frame, width=30, height=1, padx=10, bg=fill_color))
			self.input_choose_hero[len(self.input_choose_hero) - 1].pack(side=LEFT)
			self.set_buttonPosition(frame,"Выбрать",partial(self.choose_hero_num,name),LEFT)
			frame.pack(side=TOP, fill=X)

		self.input_opponent_heroes = []
		self.set_passiveTextPosition(self.bottom_frame, "Выбор героев противника", TOP)
		for name, value in self.current_opponent_heroes.items():
			string = 'Герой %s:' % str(name)
			frame = Frame(self.bottom_frame, bg=background_color)
			self.set_passiveTextPosition(frame, string, LEFT)
			self.input_opponent_heroes.append(Text(frame, width=30, height=1, padx=10, bg=fill_color))
			self.input_opponent_heroes[len(self.input_opponent_heroes) - 1].pack(side=LEFT)
			self.set_buttonPosition(frame, "Выбрать", partial(self.opponent_hero_num, name), LEFT)
			frame.pack(side=TOP, fill=X)

		self.input_cards = []
		self.set_passiveTextPosition(self.bottom_frame, "Выбор существ", TOP)
		for name, value in self.current_cards.items():
			string = 'Карта %s:' % str(name)
			frame = Frame(self.bottom_frame, bg=background_color)
			self.set_passiveTextPosition(frame, string, LEFT)
			self.input_cards.append(Text(frame, width=30, height=1, padx=10, bg=fill_color))
			self.input_cards[len(self.input_cards) - 1].pack(side=LEFT)
			self.set_buttonPosition(frame, "Выбрать", partial(self.card_num, name), LEFT)
			frame.pack(side=TOP, fill=X)



		self.input_result_battle = []
		self.set_passiveTextPosition(self.bottom_frame, "Результат матча", TOP)
		for name, value in self.result_battle.items():

			frame = Frame(self.bottom_frame, bg=background_color)
			self.set_passiveTextPosition(frame, name, LEFT)
			self.input_result_battle.append(Text(frame, width=30, height=1, padx=10, bg=fill_color))
			self.input_result_battle[len(self.input_result_battle) - 1].pack(side=RIGHT)
			#self.set_buttonPosition(frame, "Выбрать", partial(self.choose_hero_num, name), LEFT)
			frame.pack(side=TOP, fill=X)

		self.set_buttonPosition(self.bottom_frame, "Вставить данные матча", self.get_battle_data, TOP)
		searchbar.pack(side=TOP,fill=BOTH)
		temp_frame.pack(side=TOP,fill=BOTH)
		toolbar.pack(side=LEFT, fill=BOTH)
		editbar.pack(side=BOTTOM, fill=BOTH)

		self.first_top.pack(side=TOP, fill=BOTH)
		self.second_top.pack(side=TOP, fill=BOTH)
		self.middle_frame.pack(side=LEFT, fill=BOTH)
		self.bottom_frame.pack(side=LEFT, fill=BOTH)
		self.top_frame.pack(side=RIGHT, fill=BOTH)



		# Определяем рабочее пространство


	def __show_result(self, function,bar):
		cursor = function(self.db_service)
		columns = [i[0] for i in cursor.description]

		# Если таблица уже была - уничтожаем её
		if self.tree is not None:
			self.tree.destroy()
		# Создаём новую таблицу
		self.tree = ttk.Treeview(bar, columns=columns, height=25, show='headings')

		# Заполняем каждый столбец именами столбцов
		for column in columns:
			self.tree.column(column, width=len(column) * 17+len(columns), anchor=CENTER)
			self.tree.heading(column, text=column)
		self.tree.pack(side=TOP)

		# Заполняем таблицу данными
		for row in cursor.fetchall():
			self.tree.insert('', 'end', iid=row[0],values=row)

	def set_focus(self):
		selected = self.search_tree.selection()
		if len(selected) < 1:
			mb.showerror('Error', 'Выберите запись!')
			return

		item = self.search_tree.item(self.search_tree.focus())
		# print(item)
		data = item['values'][:1]
		print(data)
		print(data)
		try:
			self.tree.selection_set(data)
			self.tree.focus(self.tree.selection())
		except Exception as e:
			mb.showerror('Error',"Нет такой записи в таблице справа %s" % data)

	def choose_hero_num(self, number):
		self.insert_data_for_update(self.input_choose_hero[number-1])

	def opponent_hero_num(self, number):
		self.insert_data_for_update(self.input_opponent_heroes[number-1])

	def card_num(self, number):
		self.insert_data_for_update(self.input_cards[number - 1])

	def get_battle_data_in(self):

		data=[name for name, value in self.result_battle.items()]
		data_dict=self.get_data(self.input_result_battle,data)

		for i in range(0,3):
			data_dict[data[i]]=int(data_dict[data[i]])

		return data_dict

		pass


	def get_hero_id(self, CARDID):
		self.db_service.execute_select(
			columns=['hero_id'],
			tables=['hs.hero'],
			where="%s in('%s')" % ('CARDID', CARDID)
		)
		id = None
		table = self.db_service.get_cursor().fetchall()
		if len(table) != 1:
			mb.showerror("Ошибка", 'Нет такого героя %s.' % CARDID)
		else:
			id = table[0][0]

		return id
	def get_card_id(self, CARDID):
		self.db_service.execute_select(
			columns=['card_id'],
			tables=['hs.card'],
			where="%s in('%s')" % ('CARDID', CARDID)
		)
		id = None
		table = self.db_service.get_cursor().fetchall()
		if len(table) != 1:
			mb.showerror("Ошибка", 'Нет такой карты %s.' % CARDID)
		else:
			id = table[0][0]

		return id

	def get_battle_data(self):

		if len(self.current_race_list)<1:
			mb.showerror("Ошибка", 'Выберите существ.')
			return
		card_type=[race for race in self.current_race_list]
		print(card_type)
		chosed_hero=self.get_data(self.input_choose_hero,[name for name, value in self.current_choose_hero.items()])

		chosed_hero_notNull=set()
		print(chosed_hero)
		for name, value in chosed_hero.items():
			if value is not None:
				chosed_hero_notNull.add(value)
		print(chosed_hero_notNull)
		if len(chosed_hero_notNull) != 2 and len(chosed_hero_notNull) != 4:
			mb.showerror("Ошибка", 'Должно быть 2 или 4 различных героя при выборе')
			return

		choose_hero_id=[]
		for name in chosed_hero_notNull:
			id = self.get_hero_id(name)
			if id is None:
				return
			choose_hero_id.append(id)

		op_hero = self.get_data(self.input_opponent_heroes, [name for name, value in self.current_opponent_heroes.items()])

		op_hero_notNull =set()

		for name, value in op_hero.items():
			if value is not None:
				op_hero_notNull.add(value)
		print(op_hero_notNull)
		if len(op_hero_notNull) != 7:
			mb.showerror("Ошибка", 'Должно быть 7 различных героев оппонентов')
			return

		if len(chosed_hero_notNull.intersection(op_hero_notNull)) !=0:
			mb.showerror("Ошибка", 'Герои противников не могут быть при выборе.')
			return

		op_hero_id = []
		for name in op_hero_notNull:
			id = self.get_hero_id(name)
			if id is None:
				return
			op_hero_id.append(id)

		cards = self.get_data(self.input_cards,
								[name for name, value in self.current_cards.items()])

		cards_notNull = {}

		for name, value in cards.items():
			if value is not None:
				cards_notNull[name] = value

		card_id = []
		for name,value in cards_notNull.items():
			id = self.get_card_id(value)
			if id is None:
				return
			card_id.append(id)

		print(cards_notNull)
		battle_meta_data=self.get_battle_data_in()
		name = 'CARDID'
		index=battle_meta_data['Номер Героя']-1
		data={}
		data[name]=self.input_choose_hero[index].get(1.0, END)[:len(self.input_choose_hero[index].get(1.0, END)) - 1]
		#data=self.get_data([],[name])

		print(data)
		id=self.get_hero_id(data[name])
		if id is None:
			return

		data_to_insert={}
		data_to_insert['hero_id']=int(id)
		data_to_insert['position']=battle_meta_data['Место']
		data_to_insert['rate_points'] = battle_meta_data['Рейтинг']

		print(data_to_insert)
		name='battle_tag'
		self.db_service.execute_select(
			columns=['player_id'],
			tables=['hs.player'],
			where="%s in('%s')" % (name, battle_meta_data[name])
		)

		id = None
		table = self.db_service.get_cursor().fetchall()
		if len(table) != 1:
			mb.showerror("Ошибка", 'Нет такого игрока %s.' % battle_meta_data[name])
			return
		else:
			id = table[0][0]
		print('player_id' + str(id))
		data_to_insert['player_id']=int(id)
		self.db_service.execute_insert("hs.battle_result",data_to_insert)
		self.db_service.execute_select(
			columns=['count(*)'],
			tables=['hs.battle_result'],
		)
		id = None
		table = self.db_service.get_cursor().fetchall()
		if len(table) != 1:
			mb.showerror("Ошибка", 'Нет боёв')
			return
		else:
			id = table[0][0]

		battle_id=id
		print(data_to_insert)
		try:

			card_race_data = []
			for card_race in self.current_race_list:
				self.db_service.execute_select(
					columns=['card_race_id'],
					tables=['hs.card_race'],
					where="name in('%s')" % card_race
				)
				race_id =None
				table = self.db_service.get_cursor().fetchall()
				if len(table) != 1:
					mb.showerror("Ошибка", 'Нет такого типа существ %s' % card_race)
					return
				else:
					race_id = table[0][0]

				card_race_data.append([battle_id, race_id])
			print(card_race_data)
			self.db_service.execute_multi_insert("hs.battle_card_race", ['battle_id', 'card_race_id'],
												 card_race_data)

			hero_choice_data=[]
			for hero_id in choose_hero_id:
				hero_choice_data.append([battle_id, hero_id, int(hero_id==data_to_insert['hero_id'])])
			print(hero_choice_data)
			self.db_service.execute_multi_insert("hs.battle_hero_choice",['battle_id','hero_id', 'selected'], hero_choice_data)

			battle_opponent_hero_data = []
			for hero_id in op_hero_id:
				battle_opponent_hero_data.append([battle_id, hero_id])
			print(battle_opponent_hero_data)
			self.db_service.execute_multi_insert("hs.battle_opponent_hero", ['battle_id', 'hero_id'],
												 battle_opponent_hero_data)

			card_data = []
			for id in card_id:
				card_data.append([battle_id, id])
			print(battle_opponent_hero_data)
			self.db_service.execute_multi_insert("hs.battle_card", ['battle_id', 'card_id'], card_data)

		except Error as e:
			mb.showerror("Ошибка", str(e))
			return
		self.db_service.get_connection().commit()
		pass

	def insert_in_cards(self, cards):

		data_name=['CARDID','blizzard_id','name', 'card_text','flavor_text','health','attack','tech_level','card_race_id']
		card_data_name = ['CardID', 'ID', 'CARDNAME', 'CARDTEXT', 'FLAVORTEXT', 'HEALTH', 'ATK', 'TECH_LEVEL']
		data_to_multi=[]
		for card in cards:
			self.db_service.execute_select(
				columns=['card_race_id'],
				tables=['hs.card_race'],
				where='name in(\''+get_types_translate(card.data.get('CARDRACE'))+'\')'
			)
			race=get_types_translate(None)
			table=self.db_service.get_cursor().fetchall()
			if len(table) != 1:
				mb.showerror("Ошибка",'Нет такого типа существ '+get_types_translate(card.data.get('CARDRACE')))
				return
			else:
				race=table[0][0]
				#print(race)

			to_insert=[]

			for dataname in card_data_name:
				if ['HEALTH', 'ATK', 'ID', 'TECH_LEVEL'].count(dataname)!=0:
					#try:
					if card.data.get(dataname):
						card.data[dataname]=int(card.data[dataname])

					#except Error as e:
					#print(card.data)
						#print(e)
				to_insert.append(card.data.get(dataname))
			to_insert.append(race)
			data_to_multi.append(to_insert)

		try:
			self.db_service.execute_multi_insert("hs.card",data_name,data_to_multi)
		except Error as e:
			print(e)
			mb.showerror("Ошибка", 'Не удалось выполнить запрос по вставке карт.')
			#return
		data_to_multi=[]

		for card in cards:
			self.db_service.execute_select(
				columns=['card_id'],
				tables=['hs.card'],
				where='CARDID in(\'' + card.data['CardID'] + '\')'
			)
			table = self.db_service.get_cursor().fetchall()
			#print('table',table)
			id = 0
			if len(table) != 1:
				print(table)
				mb.showerror("Ошибка", 'Нет такой карты ' + card.data['CardID'] )
				return
			else:
				id = table[0][0]
				#print(id)

			for name, value in card.data.items():
				to_insert = []
				if keyword_translate.get(name):
					self.db_service.execute_select(
						columns=['keyword_id'],
						tables=['hs.keyword'],
						where='name in(\'' +  keyword_translate.get(name) + '\')'
					)
					keyword_id = 0
					table = self.db_service.get_cursor().fetchall()
					if len(table) != 1:

						mb.showerror("Ошибка", 'Нет такого свойства ' + keyword_translate.get(name))
						return
					else:
						keyword_id = table[0][0]
						#print(keyword_id)

					to_insert.append(id)
					to_insert.append(keyword_id)

				if len(to_insert) != 0:
					data_to_multi.append(to_insert)

			#self.db_service.execute_multi_insert("hs.card_keyword", ['card_id','keyword_id'], data_to_multi)
		try:
			self.db_service.execute_multi_insert("hs.card_keyword", ['card_id','keyword_id'], data_to_multi)
		except Error as e:
			print(e)
			mb.showerror("Ошибка", 'Не удалось выполнить запрос по вставке свойств карт.')
			return
		self.db_service.connection.commit()
		return

	def insert_in_heroes(self, heroes):
		# 'CardID', 'CARDNAME', 'HEALTH', 'CardID_HP', 'CARDNAME_HP', 'CARDTEXT_HP', 'COST_HP'

		data_name = ['CARDID', 'name', 'health', 'hp_id','hp_name','hp_text','hp_cost']
		card_data_name = ['CardID', 'CARDNAME', 'HEALTH', 'CardID_HP', 'CARDNAME_HP', 'CARDTEXT_HP', 'COST_HP']
		data_to_multi = []
		for hero in heroes:

			to_insert = []

			for dataname in card_data_name:
				if ['HEALTH'].count(dataname) != 0:
					if hero.data.get(dataname):
						hero.data[dataname] = int(hero.data[dataname])

				to_insert.append(hero.data.get(dataname))
			data_to_multi.append(to_insert)

		try:
			self.db_service.execute_multi_insert("hs.hero",data_name,data_to_multi)
		except Error as e:
			print(e)
			mb.showerror("Ошибка", 'Не удалось выполнить запрос по вставке геров.')

		self.db_service.connection.commit()
		return

	def search_cards(self,searchbar):
		finded = []
		substr = self.texts_fields[0].get(1.0, END)[:len(self.texts_fields[0].get(1.0, END))-1]
		for card in self.bg_cards:
			if card.data['CARDNAME'].lower().find(substr.lower()) != -1:
				finded.append([card.get_CardID(),card.data['CARDNAME']])

		if self.search_tree is not None:
			self.search_tree.destroy()
		columns = ['CardID', 'Название карты']
		self.search_tree = ttk.Treeview(searchbar, columns=columns, height=10, show='headings')
		for column in columns:
			self.search_tree.column(column, width=len(column) * 15+len(columns), anchor=CENTER)
			self.search_tree.heading(column, text=column)
		self.search_tree.pack(side=TOP)
		for row in finded:
			self.search_tree.insert('', 'end', values=row)
		pass
	def search_heroes(self,searchbar):
		finded = []
		substr = self.texts_fields[1].get(1.0, END)[:len(self.texts_fields[1].get(1.0, END)) - 1]
		for card in self.bg_heroes:
			if card.data['CARDNAME'].lower().find(substr.lower()) != -1:
				finded.append([card.get_CardID(),card.data['CARDNAME']])

		if self.search_tree is not None:
			self.search_tree.destroy()
		columns = ['CardID', 'Название героя']
		self.search_tree = ttk.Treeview(searchbar, columns=columns, height=10, show='headings')
		for column in columns:
			self.search_tree.column(column, width=len(column) * 15 + len(columns), anchor=CENTER)
			self.search_tree.heading(column, text=column)
		self.search_tree.pack(side=TOP)
		for row in finded:
			self.search_tree.insert('', 'end', values=row)
		pass

	def set_passiveTextPosition(self, root, string,position):
		text = Text(root, width=len(string), height=1, bg=background_color, bd=0, padx=10,fg=fill_color)
		text.insert(1.0, string)
		text.config(state="disabled")
		text.pack(side=position)

	def set_buttonPosition(self, root, string, function, position):
		Button(
			root,
			text=string,
			# Функция, которая выполняется при нажатии на кнопку.
			# Это функция вывода таблицы, и кортеж из функции получения данных и имён столбцов таблицы

			command=function,
			bg=button_color,
			fg=fill_color,
			bd=1,
			compound=TOP,
			padx=10
		).pack(side=position)

	def add_card_race(self, name):
		temp = set()
		temp.add(name)
		if len(self.current_race_list.intersection(temp)) != 0:
			self.current_race_list.remove(name)
			self.card_race_button[name].configure(background=button_color)
		else:
			self.current_race_list.add(name)
			self.card_race_button[name].configure(background="#499c54")

	def clear_input(self, texts):
		for text in texts:
			text.delete(1.0, END)

	def insert_data_for_update(self, text):
		selected = self.get_selected_id()
		if selected is not None:
			item = self.tree.item(self.tree.focus())
			data = item['values'][:1]
			self.clear_input([text])
			text.insert(1.0, item['values'][:1][0])

	def get_selected_id(self):
		selected = self.tree.selection()
		if len(selected) < 1:
			mb.showerror('Error', 'Выберите запись!')
			return None
		return selected[0]

	def get_data(self, texts_array, data_name):
		result_dict = {}
		i = 0
		for i in range(0, len(data_name)):
			str = texts_array[i].get(1.0, END)[:len(texts_array[i].get(1.0, END)) - 1]
			result_dict[data_name[i]] = str
			if str.find('None') != -1 and len(str) == 4 or len(str) == 0:
				result_dict[data_name[i]] = None

		return result_dict


if __name__ == '__main__':

	locales_in_file = [russian_locale]
	data, filename = collect_and_load_cards_data(locales_in_file)
	bg_data, bg_filename = collect_and_load_bg_cards_data(filename, locales_in_file)

	cards = parse_cards(filename)

	bg_cards = parse_cards(bg_filename)

	make_file_with_bg_heroes_and_abilities(filename, cards)

	bg_heroes = collect_bg_hero_by_cards(cards)
	bg_abilities = collect_hero_abilities(bg_heroes, cards)

	bg_cards = make_file_with_bg_cards(bg_filename, bg_cards)

	db_bg_heroes = make_db_bg_hero(bg_heroes, bg_abilities)

	root = Tk()
	try:
		app = Graphic_interface(root, bg_cards, db_bg_heroes)
		app.pack()
		root.title("Hearthstoned")
		root.geometry("1350x650")

	except Error as e:
		print(e)
	root.mainloop()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

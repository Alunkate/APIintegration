import requests
import config
import telebot
from telebot import types
from tinydb import TinyDB, Query
dbUser = TinyDB('dbUser.json')#Объявление БД
historiUser = TinyDB('historiUser.json')#Объявление БД
Fruit = Query()
try:
	bot = telebot.TeleBot(config.token)

	@bot.message_handler(commands=['start'])#обработка команд
	def find_file_ids(message):
		serchIdUser = dbUser.search(Fruit.mhid == message.chat.id)
		if serchIdUser==[]:
			dbUser.insert({'chid': message.chat.id,
				'statusedeistviya': False,
				'token': False,
				'idServisa': False,
				'kol': False,
				'link': False
				})
			markup = types.ReplyKeyboardMarkup(True)
			markup.add("Накрутить")
			markup.add("Отменить заказ")
			markup.add("Проверить статус заказа")
			markup.add("Информация")
			markup.add("Посмотреть баланс")
			markup.add("История заказов")
			bot.send_message(message.chat.id, 'Добро пожаловать в бот по накрутке.', reply_markup=markup)
		else:
			markup = types.ReplyKeyboardMarkup(True)
			markup.add("Накрутить")
			markup.add("Отменить заказ")
			markup.add("Проверить статус заказа")
			markup.add("Информация")
			markup.add("Посмотреть баланс")
			markup.add("История заказов")
			bot.send_message(message.chat.id, 'Добро пожаловать в бот по накрутке.', reply_markup=markup)


	@bot.message_handler(content_types=["text"]) #обработка сообщений
	def repeat_all_messages(message):
		serchIdUser = dbUser.search(Fruit.chid == message.chat.id)
		if serchIdUser!=[]:
			if serchIdUser[0]['statusedeistviya'] == 'voo2':
				dbUser.update({'statusedeistviya': False}, Fruit.chid == message.chat.id)
				serchIdUser = dbUser.search(Fruit.chid == message.chat.id)
				key2 = serchIdUser[0]['token']
				try:
					response = requests.get('https://instagram777.ru/api/?key=' + str(key2) + '&action=cancel&order='+str(message.text))
					print(response.content)
					markup = types.ReplyKeyboardMarkup(True)
					markup.add("Накрутить")
					markup.add("Отменить заказ")
					markup.add("Проверить статус заказа")
					markup.add("Информация")
					markup.add("Посмотреть баланс")
					markup.add("История заказов")
					bot.send_message(message.chat.id, response.content, 'Все получилось.')
					bot.send_message(message.chat.id, 'Денежные средства на сайт возвращаются не сразу, ожидайте.\nПримерное время ожидание от 1 до 30 минут',reply_markup=markup)
				except:
					bot.send_message(message.chat.id, '🎉Заказ уже выполнен, или не верно введены данные \nЛибо запрос API не прошел, попробуйте позже',reply_markup=markup)

			if serchIdUser[0]['statusedeistviya'] == 'voo':
				dbUser.update({'token': message.text}, Fruit.chid == message.chat.id)
				bot.send_message(message.chat.id, 'Введите ID заказа: ')
				dbUser.update({'statusedeistviya': 'voo2'}, Fruit.chid == message.chat.id)

		serchIdUser = dbUser.search(Fruit.chid == message.chat.id)
		if serchIdUser!=[]:
			if serchIdUser[0]['statusedeistviya'] == 'voos2':
				dbUser.update({'statusedeistviya': False}, Fruit.chid == message.chat.id)
				serchIdUser = dbUser.search(Fruit.chid == message.chat.id)
				key2 = serchIdUser[0]['token']
				try:
					response = requests.get('https://instagram777.ru/api/?key=' + str(key2) + '&action=status&order='+str(message.text))
					print(response.content)
					markup = types.ReplyKeyboardMarkup(True)
					markup.add("Накрутить")
					markup.add("Отменить заказ")
					markup.add("Проверить статус заказа")
					markup.add("Информация")
					markup.add("Посмотреть баланс")
					markup.add("История заказов")
					bot.send_message(message.chat.id, response.content, 'Все получилось.')
					bot.send_message(message.chat.id, 'quantity - кол-во.\nlink - ссылка на накрутку.\nservice - id сервиса \nremains - остаток накрутки\nstatus - статус заказа\nСтатусы заказов бывают:\nCompleted - заказ завершен\nCanceled - заказ отменен\nstart_count - кол-во с которого начиналась накрутка\n_____________\nОшибка: {"Error":"Invalid order ID."}\nОзначает не верный ID заказа\nОшибка: {"Error":"Invalid API key."}\nОзначает не верный API ключ',reply_markup=markup)
				except:
					bot.send_message(message.chat.id, '🎉Заказ уже выполнен, или не верно введены данные \nЛибо запрос API не прошел, попробуйте позже',reply_markup=markup)

			if serchIdUser[0]['statusedeistviya'] == 'voos':
				dbUser.update({'token': message.text}, Fruit.chid == message.chat.id)
				bot.send_message(message.chat.id, 'Введите ID заказа: ')
				dbUser.update({'statusedeistviya': 'voos2'}, Fruit.chid == message.chat.id)


			if serchIdUser[0]['statusedeistviya']==4:

				dbUser.update({'link': message.text}, Fruit.chid == message.chat.id)
				dbUser.update({'statusedeistviya': False}, Fruit.chid == message.chat.id)
				serchIdUser = dbUser.search(Fruit.chid == message.chat.id)
				assss = serchIdUser[0]['token']
				service = serchIdUser[0]['idServisa']
				kolvo = serchIdUser[0]['kol']
				link = serchIdUser[0]['link']
				sasas = 'Токен: ' + str(assss) + '\n' + 'Сервис: ' + str(service) + '\n' + 'Количество: ' + str(kolvo) + '\n' + 'Ссылка: ' + str(link)
				historiUser.insert({'id': message.chat.id,'hist':sasas})
				bot.send_message(message.chat.id, sasas)
				try:
					response = requests.get('https://instagram777.ru/api/?key=' + str(assss) + '&action=create&service=' + str(service) + '&quantity=' + str(kolvo) + '&link=' + str(link))
					print(response.content)
					markup = types.ReplyKeyboardMarkup(True)
					markup.add("Накрутить")
					markup.add("Отменить заказ")
					markup.add("Проверить статус заказа")
					markup.add("Информация")
					markup.add("Посмотреть баланс")
					markup.add("История заказов")
					bot.send_message(message.chat.id, response.content, 'Все получилось.')
					bot.send_message(message.chat.id, 'Заказ создан. Если в дебаг режиме вписан: <<{"order: ID...}, то заказ создан. Error balance - нет баланса/либо не хватает на выполнение накрутки. Invalid API key - ключ не верный.',reply_markup=markup)
				except:
					bot.send_message(message.chat.id, 'Неудача, попробуйте еще раз.',reply_markup=markup)
					pass
					

			if serchIdUser[0]['statusedeistviya']==3:
				dbUser.update({'kol': message.text}, Fruit.chid == message.chat.id)
				bot.send_message(message.chat.id, 'Введите ссылку: ')
				dbUser.update({'statusedeistviya': 4}, Fruit.chid == message.chat.id)

			if serchIdUser[0]['statusedeistviya']==2:
				dbUser.update({'idServisa': message.text}, Fruit.chid == message.chat.id)
				bot.send_message(message.chat.id, 'Введите количество : ')
				dbUser.update({'statusedeistviya': 3}, Fruit.chid == message.chat.id)


			if serchIdUser[0]['statusedeistviya']=='1':
				dbUser.update({'token': message.text}, Fruit.chid == message.chat.id)
				bot.send_message(message.chat.id, 'Введите id сервиса: ')
				dbUser.update({'statusedeistviya': 2}, Fruit.chid == message.chat.id)

		if message.text == 'Накрутить':
			markup = types.ReplyKeyboardRemove()
			dbUser.update({'statusedeistviya': '1'}, Fruit.chid == message.chat.id)
			bot.send_message(message.chat.id, 'Введите API ключ: ',reply_markup=markup)
		if message.text=='Информация':
			bot.send_message(message.chat.id, 'https://telegra.ph/CHtoby-sdelat-zakaz-09-28')
		if message.text == 'Отменить заказ':
			markup = types.ReplyKeyboardRemove()
			dbUser.update({'statusedeistviya': 'voo'}, Fruit.chid == message.chat.id)
			bot.send_message(message.chat.id, 'Введите API ключ: ', reply_markup=markup)
		if message.text == 'Проверить статус заказа':
			markup = types.ReplyKeyboardRemove()
			dbUser.update({'statusedeistviya': 'voos'}, Fruit.chid == message.chat.id)
			bot.send_message(message.chat.id, 'Введите API ключ: ', reply_markup=markup)


		if message.text=='Посмотреть баланс':
			if serchIdUser[0]['token'] == False:
				bot.send_message(message.chat.id, 'Вы еще не пользовались услугаи накрутки, мы не можем посмотреть ваш баланс')
			else:
				tk = serchIdUser[0]['token']
				response = requests.get(f'https://instagram777.ru/api/?key={tk}&action=balance')
				result = response.json()
				result = str(result)
				bot.send_message(message.chat.id, result)
				



		if message.text=="История заказов":
			serchIdUser = historiUser.search(Fruit.id == message.chat.id)
			if serchIdUser!=[]:
				for i in serchIdUser:
					bot.send_message(message.chat.id, i['hist'])
			else:
				bot.send_message(message.chat.id, 'Записей нет.')





except :
	print('Я упал')







if __name__ == '__main__':
     bot.polling(none_stop=True)

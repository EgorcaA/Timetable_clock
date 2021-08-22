from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

import read
import datetime
import draw

vk_session = vk_api.VkApi(token='2d2ae4f656af24a60460838e105d1db43b4a39230dc00209271306591d4b51ea94b2e0f4299fe8d9f8443')
longpoll = VkBotLongPoll(vk_session, '182720639')
Lslongpoll = VkLongPoll(vk_session)
Lsvk = vk_session.get_api()

def get_strings():


	new_strings = []
	i = 1
	while True:
		a = Lsvk.messages.getHistory(
		                	user_id=189079249,
		                	count=i,
		                	peer_id=189079249,
		                )
		string = a['items'][i-1]['text']
		if string=='':
			break
		else:
			new_strings.append(string)
			i +=1
	#print(new_strings)
	return new_strings

def send_image(filename):
	vk = vk_session.get_api()
	upload = vk_api.VkUpload(vk)
	photo = upload.photo_messages(filename + '.png')
	owner_id = photo[0]['owner_id']
	photo_id = photo[0]['id']
	access_key = photo[0]['access_key']
	attachment = f'photo{owner_id}_{photo_id}_{access_key}'
	vk.messages.send(peer_id=189079249, random_id=0, attachment=attachment)


'''
strlist = ['14 июня 11.00 ; 19 июля 12.00: 11-12',
					'14 июня 15.00 ; 19 июля 17.00: 15-17',	
					'14 июня 19.00 ; 19 июля 21.00: 19-21',
					'14 июня 22.00 ; 23 июля 23.00: 22-23',
					#'14 июня 3.00 ; 23 июля 6.00: 3-6',
					'14 июня 9.00 ; 23 июля 10.00: 9-10'
					15 мая 17.00-19.00: 17-19
					]	

'''
new_strings = get_strings()

def add_day(sourcedate, day):
    month = sourcedate.month
    year = sourcedate.year
    month = sourcedate.month
    day = sourcedate.day+day
    return datetime.datetime(year, month, day, 0, 0, 0)


dbb = read.db()
smthnew = 0
if new_strings:
	smthnew = 1
	for stri in new_strings:
		if stri == 'rmrf':
			dbb.rmrf()
		if stri == 'rm':
			dbb.rm()
		try:
			print(stri)
			dbb.update_db(stri)
		except Exception:
			pass
		finally:
			pass
			print('new right string')

dbb.print()

tommorow = add_day(datetime.datetime.now(), 1)
day_after_tom = add_day(datetime.datetime.now(), 2)
today = add_day(datetime.datetime.now(), 0)


pic = draw.draw_day(tommorow, day_after_tom)
pic.draw_tasks()
pic.show('tomorrow.png')


pic1 = draw.draw_day(today, tommorow)
pic1.draw_tasks()
pic1.show('today.png')

if smthnew:
	send_image('tomorrow')
	send_image('today')



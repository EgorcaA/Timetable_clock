import datetime
import sqlite3

def add_day(sourcedate, day):
    month = sourcedate.month
    year = sourcedate.year
    month = sourcedate.month
    day = sourcedate.day+day
    return datetime.datetime(year, month, day, 0, 0, 0)


class db:

	date_now = datetime.date.today() 
	months_names = { 'январь':1, 'февраль':2, 'март':3, 'апрель':4, 'май':5, 'июнь':6, 'июль':7, 'август':8, 'сентябрь':9, 'октяябрь':10, 'ноябрь':11, 'декабрь':12}
	month_names =	{'января':1, 'февраля':2, 'марта':3, 'апреля':4, 'мая':5, 'июня':6, 'июля':7, 'августа':8, 'сентября':9, 'октября':10, 'ноября':11, 'декабря':12}
			
	def __init__(self):	pass

	def read_string(self, string):
		string = string.split(':')
		#print(str)
		date = string[0]
		task = string[1]
		wordarr = date.split(' ')
		month = []
		day = []
		time = []
		flag_tommorow = 0
		flag_today = 0
		for i in range(len(wordarr)):
			if wordarr[i] in self.month_names.keys():
				#print('here')
				month.append(wordarr[i])
				day.append(int(wordarr[i-1]))
				time.append(wordarr[i+1])
			if wordarr[i] == 'з':
				#print('ffbrefb')
				month.append(add_day(datetime.datetime.now(), 1).month)
				day.append(add_day(datetime.datetime.now(), 1).day)
				time.append(wordarr[i+1])
				flag_tommorow = 1
			
			if wordarr[i] == 'с':
				#print('ffbrefb')
				month.append(datetime.datetime.now().month)
				day.append(datetime.datetime.now().day)
				time.append(wordarr[i+1])
				flag_today = 1
				#print(month, day, time)
				#print(month[0])
		
		if len(month) == 2:
			time_start = time[0].split('.')
			time_stop = time[1].split('.')
			date_start =  datetime.datetime(self.date_now.year, self.month_names[month[0]], day[0], int(time_start[0]), int(time_start[1]), 00)
			date_stop =  datetime.datetime(self.date_now.year, self.month_names[month[1]], day[1], int(time_stop[0]), int(time_stop[1]), 00)
		elif flag_tommorow == 0 and flag_today == 0:
			time = time[0].split('-')
			time_start = time[0].split('.')
			time_stop = time[1].split('.')
			#print(time_start, time_stop)
			date_start =  datetime.datetime(self.date_now.year, self.month_names[month[0]], day[0], int(time_start[0]), int(time_start[1]), 00)
			date_stop =  datetime.datetime(self.date_now.year, self.month_names[month[0]], day[0], int(time_stop[0]), int(time_stop[1]), 00)
		else:
			time = time[0].split('-')
			time_start = time[0].split('.')
			time_stop = time[1].split('.')
			#print(time_start, time_stop)
			date_start =  datetime.datetime(self.date_now.year, month[0], day[0], int(time_start[0]), int(time_start[1]), 00)
			date_stop =  datetime.datetime(self.date_now.year, month[0], day[0], int(time_stop[0]), int(time_stop[1]), 00)

		
		#print(date_start.strftime('%Y-%m-%d %H:%M:%S'))
		#print(date_stop.strftime('%Y-%m-%d %H:%M:%S'))
		return date_start.strftime('%Y-%m-%d %H:%M:%S'), date_stop.strftime('%Y-%m-%d %H:%M:%S'), task
		#if date.split(' ')[0] in month.keys() :
		#	print('here')


	def update_db(self, str):
		#str = '15 января 13.00-15.00: сдача по матану'
		date_start, date_stop, task = self.read_string(str)
		#print(date_start, date_stop, task)
		li = [date_start, date_stop, task]

		turp = tuple(li)
		#print(turp)

		con = sqlite3.connect("mydatabase.db")
		cur = con.cursor()
		#try:
		#	cur.execute("CREATE TABLE timetable (time_start, time_stop, task)")

		cur.execute("INSERT INTO timetable (time_start, time_stop, task) VALUES (?, ?, ?)", turp)
		#cur.execute("DELETE FROM timetable WHERE task NOT IN (SELECT min(rowid) FROM timetable GROUP BY task)")
		
		
		#for row in cur.execute('SELECT * FROM timetable WHERE time_start < %s' % time0):
		#	print(row)
		

		con.commit()
		con.close()


	def select(self, time0, time1):
		con = sqlite3.connect("mydatabase.db")
		cur = con.cursor()
		
		items = []
		for row in cur.execute("SELECT * FROM timetable WHERE time_start BETWEEN '%s' AND '%s'" % (time0, time1)):
			items.append(row[1:])
			#print(row)
		con.close()
		return items
#strftime('%s', date) BETWEEN strftime('%s', start_date) AND strftime('%s', end_date)


	def print(self):
		con = sqlite3.connect("mydatabase.db")
		cur = con.cursor()
		for row in cur.execute('SELECT * FROM timetable ORDER BY time_start'):
			print(row)
		con.close()

	def rmrf(self):
		con = sqlite3.connect("mydatabase.db")
		cur = con.cursor()
		cur.execute("DELETE FROM timetable")
		con.commit()
		con.close()

	def rm(self):
		con = sqlite3.connect("mydatabase.db")
		cur = con.cursor()
		cur.execute("delete from timetable where task_id  = (select task_id from timetable order by task_id limit 1 )")
		con.commit()
		con.close()


	def create(self):
		con = sqlite3.connect("mydatabase.db")
		cur = con.cursor()
		cur.execute("CREATE TABLE timetable (task_id INTEGER PRIMARY KEY AUTOINCREMENT,  time_start DATETIME, time_stop DATETIME, task VARCHAR(70))" )
		con.commit()
		con.close()

if __name__ == '__main__':
	dbb = db()
	#dbb.rm()
	dbb.create()
	str = 'з 14.00-19.00: сдать дз'
	dbb.update_db(str)
	#dbb.rm()
	dbb.print()
	#dbb.select(time0, time1)
#print(month.keys())

#июнь: докатать катку
#13-15 июня: транжирь
#завтра 13.00-15.00: сдача по матану
#14 июня 12.00-15.00: порабоать
#207
#265
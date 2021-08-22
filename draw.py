from PIL import Image, ImageDraw, ImageFont
import numpy as np
import read
import datetime
import random

def add_day(sourcedate, day):
    month = sourcedate.month
    year = sourcedate.year
    month = sourcedate.month
    day = sourcedate.day+day
    return datetime.datetime(year, month, day, 0, 0, 0)



class draw_day:

	def __init__(self, need_start, need_stop):	
		self.need_start = need_start
		self.need_stop = need_stop
		self.alpha = 0.5
		self.height = self.alpha*1920
		self.width = self.alpha*1280
		self.radius = 0.25*self.width
		self.center_up = np.array([self.width/2, self.height/4])
		self.center_down = np.array([self.width/2, self.height*(3/4)])
		self.ticks_start = 0.8*self.radius
		self.ticks_stop = 1.1*self.radius
	
		self.bg = Image.open("bg.png")
		self.bg = self.bg.resize((int(self.width), int(self.height)), Image.ANTIALIAS)
		#img = Image.new('RGBA', (height, width), 'white')  

		self.idraw = ImageDraw.Draw(self.bg)

		self.idraw.ellipse((self.center_up - self.radius).tolist() + (self.center_up + self.radius).tolist(), fill=None, outline=(255, 204, 255), width=15)
		self.idraw.ellipse((self.center_down - self.radius).tolist() + (self.center_down + self.radius).tolist(), fill=None, outline=(255, 204, 255), width=15) 

		for hour in range(12):
			vec1 = np.array([0, -self.ticks_start])
			vec2 = np.array([0, -self.ticks_stop])
			phi = 2*np.pi/12*hour
			rm = np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])
			vec_new1 = np.dot(rm, vec1) + self.center_up
			vec_new2 = np.dot(rm, vec2) + self.center_up
			self.idraw.line(vec_new1.tolist() + vec_new2.tolist(), fill=(245 - 20*hour, 206, 235), width=5, joint='curve')

			vec_new1 = np.dot(rm, vec1) + self.center_down
			vec_new2 = np.dot(rm, vec2) + self.center_down
			self.idraw.line(vec_new1.tolist() + vec_new2.tolist(),fill=(245 - 20*hour, 206, 235), width=5, joint='curve')

	def draw_arc(self, phi_start, phi_stop, text, upod):
		if upod == 1: center = self.center_up
		else:	center = self.center_down
		self.idraw.pieslice((center - 1.2*self.radius).tolist() + (center + 1.2*self.radius).tolist(),   phi_start+3, phi_stop-3, fill=(255, 204, 255), outline=(204, 204, 204), width=0)
		self.idraw.pieslice((center - 1.1*self.radius).tolist() + (center + 1.1*self.radius).tolist(),   phi_start+3, phi_stop-3, fill=( 204 + random.randint(-30, 30),102 + random.randint(-30, 30),255+ random.randint(-30, 0)), outline=(204, 204, 204), width=2)
		phi = (((phi_stop + phi_start)/2)%360 )/360*2*np.pi  #- len(text)*2.2
		#print(phi)
		vec_ne1 = np.array([np.cos(phi)*1.0*self.radius, np.sin(phi)*1.0*self.radius]) + center
		#print(vec_ne1.tolist())
		if ((phi_stop + phi_start)/2)%360 >90 and ((phi_stop + phi_start)/2)%360 < 270:
			arch = "rd"
		else:
			arch = "ld"
		font = ImageFont.truetype("Times New Roman.ttf", size=20)
		self.idraw.ellipse((vec_ne1- 0.03*self.radius).tolist() + (vec_ne1+ 0.03*self.radius).tolist(), fill=None, outline='Red', width=5)
		self.idraw.text(vec_ne1.tolist(), text, font=font, anchor=arch, fill=(0, 0, 0))

	def draw_tasks(self):

		dbb = read.db()
		
		#str = '14 июня 12.00 ; 19 июля 15.00: влоgsrgкуолт'
		#str = '14 июня 15.00-17.00: порvreабоать'
		#time0 = datetime.datetime(2021, 6, 14)
		#time1 = datetime.datetime(2021, 6, 15)
		#dbb.rm()
		
		time0 = self.need_start
		time1 = self.need_stop
		#dbb.print()
		items = dbb.select(time0, time1)

		for item in items[:]:
			print(item)
			time_st1 = datetime.datetime.strptime(item[0], '%Y-%m-%d %H:%M:%S')
			time_st2 = datetime.datetime.strptime(item[1], '%Y-%m-%d %H:%M:%S')
			phi_start = time_st1.hour/12*360 - 90 + time_st1.minute/60/12*360
			phi_stop = time_st2.hour/12*360 - 90 + time_st2.minute/60/12*360
			#print(time_st1.hour, time_st2.hour)
			if time_st1.hour < 12 and time_st2.hour < 12:
				#print(time_st1.hour, time_st2.hour)
				self.draw_arc(phi_start, phi_stop, item[2], upod=1)
			if time_st1.hour >= 12  and time_st2.hour <= 24:
				self.draw_arc(phi_start, phi_stop, item[2], upod=2)

			if  time_st1.hour < 12  and time_st2.hour >= 12:
				self.draw_arc(phi_start%360, 270, item[2], upod=1)
				if time_st2.hour > 12:
					self.draw_arc(-90, phi_stop%360, item[2], upod=2)

		self.idraw.ellipse((self.center_up - 0.7*self.radius).tolist() + (self.center_up + 0.7*self.radius).tolist(), outline=None, fill=(255, 255, 255), width=15)
		self.idraw.ellipse((self.center_down - 0.7*self.radius).tolist() + (self.center_down + 0.7*self.radius).tolist(), outline=None, fill=(255, 255, 255), width=15)
		for hour in range(0, 12, 3):
			vec1 = np.array([0, -0.8*self.ticks_start])
			phi = 2*np.pi/12*hour
			rm = np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])
			vec_new1 = np.dot(rm, vec1) + self.center_up
			#self.idraw.line(vec_new1.tolist() + vec_new2.tolist(), fill=(100, 206, 235), width=50, joint='curve')
			self.idraw.text(vec_new1.tolist(), str(hour), font=ImageFont.truetype("Times New Roman.ttf", size=30), anchor="mm", fill=(0, 0, 0))
			vec_new1 = np.dot(rm, vec1) + self.center_down
			self.idraw.text(vec_new1.tolist(), str(hour + 12), font=ImageFont.truetype("Times New Roman.ttf", size=30), anchor="mm", fill=(0, 0, 0))
			#self.draw_arc(phi_start, phi_stop, item[2])
		self.idraw.text((self.center_up + np.array([0, -0.22*self.height])).tolist(), str(self.need_start.date()), font=ImageFont.truetype("Times New Roman.ttf", size=30), anchor="mm", fill=(30, 0, 0))
	
	def show(self, filename):
		#self.bg.show()
		self.bg.save(filename)


	
if __name__ == '__main__':

	tommorow = add_day(datetime.datetime.now(), 1)
	#print(tommorow)
	day_after_tom = add_day(datetime.datetime.now(), 2)
	today = datetime.datetime.now()
	#print(day_after_tom)
	pic = draw_day(tommorow, day_after_tom)

	pic.draw_tasks()
	pic.show()



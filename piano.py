from pygame import *
from random import randint
from time import sleep

init()
mixer.init(22050, -16, 1, 1024)
res=[1512,500]
window=display.set_mode(res)
clock=time.Clock()
black=(0,0,0)
red=(255,0,0)
blue=(0,0,255)
green=(0,255,0)
yellow=(255,255,0)
lightred=(204,0,0)
lightblue=(51,153,255)
lightgreen=(153,255,51)
lightyellow=(255,255,102)
white=(255,255,255)
Font=font.SysFont("arial",20)


class Piano(object):
	def __init__(self):
		self.channel=0
		self.keys=[]
		self.recordbutton=Recordbutton()
		self.playbutton=Playbutton()
		self.record=False
		self.lastkey=" "
		self.speed=0.2
		file=open("list.dat")
		for line in file:
			col=line.split()
			if len(col)==6:
				self.keys.append(Button(col[0],col[1],col[2],col[3],col[4],col[5]))
	def draw(self):
		window.fill(black)
		self.recordbutton.draw()
		self.playbutton.draw()
		text = Font.render("Speed: "+str(piano.speed),True,white)
		window.blit(text,(700,355))
		for key in self.keys:
			if key.shift==0:
				key.draw()
		for key in self.keys:
			if key.shift==1:
				key.draw()
	def recording(self):
		if self.record:
			silent=True
			for i in range(8):
				if mixer.Channel(i).get_busy()==1:
					silent=False
			if silent and self.lastkey!=" ":
				self.recordfile.write(" ")
				self.lastkey=" "

class Button(object):
	def __init__(self,id,num,shift,file,key1,key2):
		self.id=id
		self.num=int(num)
		self.shift=int(shift)
		self.file=file
		self.key1=key1
		self.key2=key2
		
	def play(self,piano):
		mixer.Channel(piano.channel).play(mixer.Sound(self.file))
		print self.id
		if piano.record:
			piano.recordfile.write(str(self.id))
			piano.lastkey=str(self.id)
		if self.shift==0:
			draw.rect(window,green,Rect((self.num-1)*42,1,41,298),0)
		elif self.shift==1:
			draw.rect(window,green,Rect((self.num-1)*42+32,1,21,150),0)
		display.flip()
		piano.channel=piano.channel+1
		if piano.channel==8:
			piano.channel=0
	
	def draw(self):
		if self.shift==0:
			draw.rect(window,white,Rect((self.num-1)*42,1,41,298),0)
		elif self.shift==1:
			draw.rect(window,black,Rect((self.num-1)*42+32,1,21,150),0)

class Recordbutton(object):
	def __init__(self):
		self.x=300
		self.y=350
		self.h=40
		self.w=150
		
	def draw(self):
		if mouse.get_pos()[0]>self.x and mouse.get_pos()[0]<self.x+self.w and mouse.get_pos()[1]>self.y and mouse.get_pos()[1]<self.y+self.h:
			draw.rect(window,green,Rect(self.x,self.y,self.w,self.h),1)
		else:
			draw.rect(window,white,Rect(self.x,self.y,self.w,self.h),1)
		text = Font.render("      Record",True,white)
		window.blit(text,(self.x+5,self.y+5))
		
	def event(self,piano):
		if self.click() and piano.record:
			piano.record= not piano.record
			piano.recordfile.close()
			print "record stop"
		elif self.click() and not piano.record:
			piano.recordfile=open("record.dat",'w')
			piano.record= not piano.record
			print "record start"
			
		
	def click(self):
		if mouse.get_pressed()[0]:
			if mouse.get_pos()[0]>self.x and mouse.get_pos()[0]<self.x+self.w and mouse.get_pos()[1]>self.y and mouse.get_pos()[1]<self.y+self.h:
				return True
			
class Playbutton(object):
	def __init__(self):
		self.x=500
		self.y=350
		self.h=40
		self.w=150
		self.playing=False
		self.num=0
		self.line=" "
		
	def draw(self):
		if mouse.get_pos()[0]>self.x and mouse.get_pos()[0]<self.x+self.w and mouse.get_pos()[1]>self.y and mouse.get_pos()[1]<self.y+self.h:
			draw.rect(window,green,Rect(self.x,self.y,self.w,self.h),1)
		else:
			draw.rect(window,white,Rect(self.x,self.y,self.w,self.h),1)
		text = Font.render("      Play",True,white)
		window.blit(text,(self.x+5,self.y+5))
		
	def event(self,piano):
		if self.click() and not self.playing:
			self.file=open("record.dat")
			self.num=0
			self.line=self.file.readline()
			c=self.line[self.num]
			for k in piano.keys:
				if c==str(k.id):
					k.play(piano)
					sleep(piano.speed)
					piano.draw()
				elif c==" ":
					sleep(piano.speed)
					break
			self.num=self.num+1
			self.playing=True
		elif self.click() and self.playing:
			self.playing=False
		elif not self.click() and self.playing:
			if self.num<len(self.line):
				c=self.line[self.num]
				for k in piano.keys:
					if c==str(k.id):
						k.play(piano)
						sleep(piano.speed)
						piano.draw()
					elif c==" ":
						sleep(piano.speed)
						break
				self.num=self.num+1
			else :
				self.num=0
				self.line=self.file.readline()
		if self.line=="":
			self.playing=False
			self.line=" "

			
		
	def click(self):
		if mouse.get_pressed()[0]:
			if mouse.get_pos()[0]>self.x and mouse.get_pos()[0]<self.x+self.w and mouse.get_pos()[1]>self.y and mouse.get_pos()[1]<self.y+self.h:
				return True
piano=Piano()
end=False
while not end:
	piano.draw()
	for z in event.get():
		if z.type==QUIT:
			end=True
		if z.type==KEYDOWN:
			if z.key== K_KP_MINUS:
				piano.speed=piano.speed-0.1
				if piano.speed<=0.1:
					piano.speed=0.1
			if z.key== K_KP_PLUS:
				piano.speed=piano.speed+0.1

		for k in piano.keys:
			if z.type==KEYDOWN:
				keys = key.get_pressed()
				if z.key==int(k.key1)  and key.get_mods() & KMOD_SHIFT and k.shift==1:
					k.play(piano)
				if z.key==int(k.key1)  and not key.get_mods() & KMOD_SHIFT and k.shift==0:
					k.play(piano)
	piano.recording()
	
	#print mixer.Channel(0).get_busy()
	piano.recordbutton.event(piano)
	piano.playbutton.event(piano)
	display.flip()
	clock.tick(20)

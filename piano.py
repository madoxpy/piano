from pygame import *
from random import randint
from time import sleep

init()
res=[1512,300]
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
		self.keys=[]
		file=open("list.dat")
		for line in file:
			col=line.split()
			if len(col)==6:
				self.keys.append(Button(col[0],col[1],col[2],col[3],col[4],col[5]))
	def draw(self):
		for key in self.keys:
			if key.shift==0:
				key.draw()
		for key in self.keys:
			if key.shift==1:
				key.draw()

class Button(object):
	def __init__(self,id,num,shift,file,key1,key2):
		self.id=id
		self.num=int(num)
		self.shift=int(shift)
		self.file=file
		self.key1=key1
		self.key2=key2
		
	def play(self):
		mixer.Channel(0).play(mixer.Sound(self.file))
		print self.id
		if self.shift==0:
			draw.rect(window,green,Rect((self.num-1)*42,1,41,298),0)
		elif self.shift==1:
			draw.rect(window,green,Rect((self.num-1)*42+32,1,21,150),0)
		display.flip()
	
	def draw(self):
		if self.shift==0:
			draw.rect(window,white,Rect((self.num-1)*42,1,41,298),0)
		elif self.shift==1:
			draw.rect(window,black,Rect((self.num-1)*42+32,1,21,150),0)


piano=Piano()		
end=False
while not end:
	piano.draw()
	for z in event.get():
		if z.type==QUIT:
			end=True
		for k in piano.keys:
			if z.type==KEYDOWN:
				keys = key.get_pressed()
				if z.key==int(k.key1)  and key.get_mods() & KMOD_SHIFT and k.shift==1:
					k.play()
				if z.key==int(k.key1)  and not key.get_mods() & KMOD_SHIFT and k.shift==0:
					k.play()
		'''if z.type==KEYDOWN:
			if z.key==K_q:
				mixer.Channel(0).play(mixer.Sound('a.wav'))
			if z.key==K_w:
				mixer.Channel(1).play(mixer.Sound('h.wav'))
			if z.key==K_e:
				mixer.Channel(2).play(mixer.Sound('c.wav'))
			if z.key==K_r:
				mixer.Channel(3).play(mixer.Sound('d.wav'))
			if z.key==K_t:
				mixer.Channel(4).play(mixer.Sound('e.wav'))
			if z.key==K_y:
				mixer.Channel(5).play(mixer.Sound('f.wav'))
			if z.key==K_u:
				mixer.Channel(6).play(mixer.Sound('g.wav'))
		'''
	'''keys = key.get_pressed()
	for k in piano.keys:
		if keys[int(k.key1)] and keys[int(k.key2)]:
			k.play()'''
	display.flip()
	clock.tick(20)

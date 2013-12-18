import pygame, sys, os, math
from pygame.locals import *

class Play_Music(pygame.sprite.Sprite):
	
	def __init__(self, filename, loop_count):
		pygame.sprite.Sprite.__init__(self)	
		pygame.mixer.init()
		pygame.mixer.set_num_channels(50)
		full_path = os.path.dirname(os.path.realpath(sys.argv[0]))
		
		self.song = pygame.mixer.Sound(full_path + filename)

		self.playing = False

		self.channel = pygame.mixer.find_channel()
		self.channel.play(self.song)
		self.channel.pause()
		
	def play(self):
		self.channel.play(self.song, -1)
		self.playing = True
	
	def play_once(self):
		self.channel.play(self.song, 0)
		
	def stop(self):
		self.channel.pause()
		self.playing = False 
		
	def locate(self, dx, dy):
		distance = math.sqrt((dx * dx) + (dy * dy))
		if distance < 300:
			distance = 300
		
		if dy > 300:
			distance *= 2
		
		if dx < -300:
			pan = [0, 1]
		elif dx > 300:
			pan = [1, 0]
		else:
			pan = [(float(dx) + 300.0) / 600, 1 - ((float(dx) + 300.0) / 600)]
			
		volume = 300 / distance
		self.channel.set_volume(pan[1] * volume, pan[0] * volume)
	
	def set_volume(self, volume):
		self.channel.set_volume(volume)
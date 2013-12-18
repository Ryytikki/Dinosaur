import pygame, sys, math, os
from pygame.locals import *
from random import random

def load_image(name):
	full_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	image = pygame.image.load(full_path + "\\"+ name).convert_alpha()
	return(image)
	

class Cloud(pygame.sprite.Sprite):
		
	def __init__(self, ID):
		pygame.sprite.Sprite.__init__(self)		
		self.image = load_image("Images\\Maps\\clouds\\cloud" + str(ID) + ".png")
		self.rect = self.image.get_rect()
		
		x = random() * 10000
		self.rect.topleft = [x, 125.0]
		
		self.ID = ID
	
	def update(self, foreground_X, map_size):
		self.rect[0] += 1 * -1 ** (self.ID + 1)
		if self.rect[0] > (1000 * (map_size + 1)) + foreground_X + 200:
			self.rect[0] = -200
		if self.rect[0] < foreground_X - 200:
			self.rect[0] = 1000 * (map_size + 1) - foreground_X + 200

	
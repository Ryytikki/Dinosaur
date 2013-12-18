import pygame, sys, math, os
from pygame.locals import *

def load_image(name):
	full_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	image = pygame.image.load(full_path + "\\"+ name)
	return(image)
	

class Gust(pygame.sprite.Sprite):
		
	def __init__(self, height, map_size):
		pygame.sprite.Sprite.__init__(self)
		self.height = height
		
		self.image = pygame.Surface((0,100))
		self.blank_image = self.image
		self.gust_image = pygame.Surface((1000 * (map_size - 1), 100), pygame.SRCALPHA, 32)
		gust_image = load_image("Images\\Maps\\gust.png")
		for i in range(0, map_size - 1):
			self.gust_image.blit(gust_image, [i * 1000, 0])
		self.rect = self.image.get_rect()
		self.rect[1] = height - 110
		self.timer = 0
		self.gust = 90
		self.gust_duration = 1
		
		self.type = "gust"
		
	def update(self, player_list, map_location):
		if self.timer >= self.gust:
			self.image = self.gust_image
			self.rect[0] += 25
			self.run_gust(player_list, map_location)
			if self.timer > self.gust + self.gust_duration:
				self.timer = 0
				self.image = self.blank_image
				self.rect[0] = 0
				
		self.timer += 1
		
	def run_gust(self, player_list, map_location):	
		for player in player_list:
			if player.rect[1] - map_location[1] + 1200 + player.rect[3]< self.height: 			
				if self.timer + 1 < self.gust + self.gust_duration:
					player.animation_type = "gust"
				else:
					player.animation_type = "idle"
					player.frame_ID = 0
			elif player.animation_type == "gust":
				player.animation_type = "idle"
				player.frame_ID = 0
	def test_landed(self, player, map_location):
		return(False)
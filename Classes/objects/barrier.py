import pygame, sys, math, os
from pygame.locals import *

def load_image(name):
	full_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	image = pygame.image.load(full_path + "\\"+ name).convert_alpha()
	return(image)

class Barrier(pygame.sprite.Sprite):
		
	def __init__(self, rect_size, direction):
		pygame.sprite.Sprite.__init__(self)	
		self.rect = rect_size
		self.image = pygame.Surface((0,0))#rect_size[2], rect_size[3]))
		self.direction = direction
		
		self.type = "barrier"
		
	def update(self, map_location, players):
		collide_rect = [self.rect[0] + map_location[0], self.rect[1] + map_location[1] - 832, self.rect[2], self.rect[3]]
		for player in players:
			if player.ID == 2 and player.hit_rect.colliderect(collide_rect) and player.x_direction == 1:
				if self.direction[0] == -1 and player.hit_rect[0] + player.hit_rect[2] > self.rect[0] + map_location[0]:
					player.rect[0]  -= player.speed
				elif self.direction[0] == 1 and player.hit_rect[0] > self.rect[0] + self.rect[2] + map_location[0] and player.x_direction == -1:
					player.rect[0] = collide_rect[0]
			
			
	def test_landed(self, player, offset):
		collide_rect = [self.rect[0] + offset[0], self.rect[1] + offset[1], self.rect[2], self.rect[3]]
		if player.hit_rect.colliderect(collide_rect):
			if self.direction[1] == 1 and player.hit_rect[1] >= collide_rect[1]:
				if player.y_speed < 0:
					player.landed == True
					player.rect[1] = collide_rect[1] - 145
					player.jumping = False
					player.animation_type = "land"
					player.y_speed = 0
					player.frame_ID = 0
				return(True)
			else:
				return(False)
import pygame, sys, math, os
from pygame.locals import *
from Classes.objects.block import Block

def load_image(name):
	full_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	image = pygame.image.load(full_path + "\\"+ name).convert_alpha()
	return(image)

class Spawner(pygame.sprite.Sprite):
		
	def __init__(self, location):
		pygame.sprite.Sprite.__init__(self)	
		
		self.image = load_image("Images\\spawner.png")
		self.rect = self.image.get_rect()
		self.rect.center = location
		
		self.spawn_delay = 10
		self.spawn_counter = 0
		self.spawned = 0
		self.blocks = []
		self.rubble_counter = [-1,-1,-1]
		self.type = "spawner"
		self.spawn()
		
	def update(self, map_location, players, map):
		if self.spawn_counter > self.spawn_delay:
			self.blocks[self.spawned].rect[1] = self.rect[1]
			self.blocks[self.spawned].y_speed = 1
			self.spawned -= 1
			
			if self.spawned < 0:
				self.spawned = 2
				
			self.spawn_counter = 0
			
		for item in self.blocks:
			test_rect = [item.rect[0] + map_location[0], item.rect[1] + map_location[1] - 880, item.rect[2], item.rect[3]]
			item.true_rect = test_rect
			item.rect[1] += 5
			for player in players:
				if player.x_direction == 1:
					test_rect[0] -= 75

				if player.rect.colliderect(test_rect) and player.rect[0] - test_rect[0] > -150 and player.rect[0] - test_rect[0] < 50 and item.dead == False and player.dead == 0 and player.jumping == False:
					player.dead = 1
					player.animation_type = "squashed"
					player.frame_ID = 3
					player.x_direction = 0
					
			item.spawner_update(map_location, map, players)
				
		self.spawn_counter += 1

	def spawn(self):
		for i in range(0,3):
			block = Block([self.rect[0] + 390 * i + 110, self.rect[1]], 1)
			block.y_speed = 0
			self.blocks.append(block)
			
	def test_landed(self, player, offset):
		return(False)
import pygame, sys, math, os
from pygame.locals import *
from Classes.objects.block import Block
from Classes.play_music import Play_Music

def load_image(name):
	full_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	image = pygame.image.load(full_path + "\\"+ name).convert_alpha()
	return(image)

class Water(pygame.sprite.Sprite):
		
	def __init__(self, location, width, ID):
		pygame.sprite.Sprite.__init__(self)	
		
		self.image = load_image("Images\\pipe.png")
		self.rect = self.image.get_rect()
		
		self.water = pygame.Surface((1350 * width, 450), pygame.SRCALPHA, 32)
		water_image =  load_image("Images\\maps\\water\\WATER-0001.png")
		self.water_rect = self.water.get_rect()
		self.rect.center = location
		self.water_rect[0] = self.rect[0] - 500
		
		self.plank = load_image("Images\\plank.png")
		self.plank_rect = self.plank.get_rect()
		
		for i in range(0, width):
			self.water.blit(water_image, (1350 * i, 0))
			
		self.type = "water"
		self.ID = ID
			
		self.on = False
		self.water_height = 0
		
		self.frame_ID = 17
		self.water_ID = 0
		
		self.start = []
		self.flow = []
		self.stop = []
		self.pipe = load_image("Images\\pipe.png")
		self.water_animation = []
		self.blit_rect = []
		
		self.water_pouring = Play_Music("//sfx//water-flow.ogg", -1)
		
		self.prebuffer()
		
	def update(self, players, map_location):

		if self.on and self.water_height < 90:
			self.water_height += 2
		elif self.on == False and self.water_height > 0:
			self.water_height -= 2
		self.water_rect[1] = self.rect[1] + 50 - self.water_height
		
		if self.on and self.frame_ID < 16:
			self.image = self.start[self.frame_ID]
			
		if self.on == False and self.frame_ID < 16:
			self.image = self.stop[self.frame_ID]
			
		if self.on and self.frame_ID >= 16:
			self.image = self.flow[self.frame_ID - 16]
			
			if self.frame_ID >= 31:
				self.frame_ID = 16
				
		if self.on == False and self.frame_ID >= 16:
			self.image = self.pipe
			
		self.water = self.water_animation[int(self.water_ID)]
		
		if self.water_ID >= 22:
			self.water_ID = 0
		
		self.frame_ID += 1
		self.water_ID += 0.5
		
		self.blit_rect = [self.rect[0], 490 - self.water_height + self.rect[1], 321, 300]
		self.plank_rect = [self.rect[0] - 320, self.rect[1] + 490 - self.water_height, self.plank_rect[2], self.plank_rect[3]]
		
		test_rect = [self.plank_rect[0] + map_location[0] + self.rect[3] / 2, self.plank_rect[1] + map_location[1] - 832, self.plank_rect[2], self.plank_rect[3]]
		for player in players:
			if player.player_ID == player.ID:
				self.water_pouring.locate(test_rect[0] - player.rect[0], test_rect[1] - player.rect[1])
		
	def trigger(self, trigger_code):
		self.on = not self.on
		if self.frame_ID >= 16:
			self.frame_ID = 0
		
		if self.on:
			self.water_pouring.play()
		else:
			self.water_pouring.stop()
		
	def prebuffer(self):
		for i in range(1, 17):
			self.start.append(load_image("Images\\begin-flow\\start-flow-" + str(10000 + i)[1:] + ".png"))
		
		for i in range(1, 17):
			self.flow.append(load_image("Images\\flowing\\flowing-" + str(10000 + i)[1:] + ".png"))
		
		for i in range(1, 17):
			self.stop.append(load_image("Images\\stopping\\stopping-" + str(10000 + i)[1:] + ".png"))
		
		for i in range(1, 24):
			self.water_animation.append(load_image("Images\\Maps\\water\\water-" + str(10000 + i)[1:] + ".png"))
		
	def test_landed(self, player, offset):
		# Corrected rect for floating blocks
		collide_rect = [self.plank_rect[0] + offset[0], self.plank_rect[1] + offset[1] + 30, self.plank_rect[2], self.plank_rect[3] + 500]
		# Check the player is within the hitbox and is colliding with the block (first check is for air, second for ground)
		if (player.hit_rect.colliderect(collide_rect)):
			if player.y_speed < 0:
				player.rect[1] = self.rect[1] + 490 - self.water_height + offset[1] - 150 + 30
				player.jumping = False
				player.animation_type = "land"
				player.y_speed = 0
				player.frame_ID = 0	
				
			if player.rect[1] > self.rect[1] + 490 - self.water_height + offset[1] - 150 + 30 and player.jumping == False:
				player.rect[1] = self.rect[1] + 490 - self.water_height + offset[1] - 150 + 30
				
			if self.on and self.water_height > 0 and self.water_height < 90:
				player.rect[1] -= 2
			
			if not self.on and self.water_height != 0:
				player.rect[1] += 2
			
			return(True)
		else:
			return(False)
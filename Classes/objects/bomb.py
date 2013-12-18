import pygame, sys, math, os
from pygame.locals import *
from Classes.play_music import Play_Music

def load_image(name):
	full_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	image = pygame.image.load(full_path + "\\"+ name).convert_alpha()
	return(image)

class Bomb(pygame.sprite.Sprite):
		
	def __init__(self, location):
		pygame.sprite.Sprite.__init__(self)	
		self.bomb = load_image("Images\TNT-unlit.png")
		self.bomb_loop = []
		for i in range(1,6):
			self.bomb_loop.append(load_image("Images/TNT-frames/TNT-" + str(10000 + i)[1:] + ".png"))
			
		self.no_image = pygame.Surface((1,1), pygame.SRCALPHA, 32)
		self.no_image.fill(0)
		self.image = self.bomb
		self.frame_ID = 0
		
		self.rect = self.image.get_rect()
		self.rect.center = location
		self.start_location = location
		
		self.carried = False
		self.interacting_timer = 0
		self.player = ""
		self.boom_time = 1500
		self.boom_sfx = Play_Music("//sfx//bomb-explode.ogg", -1)
		self.hiss_sfx = Play_Music("//sfx//hiss-fuse.ogg", -1)
		
		self.y_speed = 0
		self.x_speed = 0
		self.jumping = False
		
		self.type = "bomb"
		self.active = False
		
		self.live = False
		self.countdown = 0
		
		self.frame_ID = 0
		
	def update(self, player_list, map, map_location, objects):
	
		active = 0
		for object in objects:
			if object.type == "bomb" and object.active == True:
				active += 1
				
		if active == 1 and self.active == True:
			active = 0
			
		if map.ground_collision(self, [0,532]) == False and self.carried == False:
			self.y_speed += 2
			self.rect[1] += self.y_speed
		else:
			self.x_speed = 0
			self.y_speed = 0
			
		test_rect = [self.rect[0] + map_location[0], self.rect[1] + map_location[1] - 832, self.rect[2], self.rect[3]]
			
		for player in player_list:
			if player.ID == 2 and player.dropping == True and player.player_ID == player.ID:	
				if self.carried == False:
					if player.hit_rect.colliderect(test_rect) and active == 0:
						self.carried = True
						self.player = player
						self.active = True
						player.bomb = True
						player.frame_ID = 1
						player.animation_type = "pickup"
						player.dead = 1
						self.interacting_timer = 0
						if self.countdown <= 1:
							self.countdown = 1
				elif self.interacting_timer > 30 and player.ID == 2 and self.active == True:
					self.carried = False
					self.active = False
					self.player.bomb = False
					self.x_speed = (player.speed * player.x_direction)
					self.frame_ID = 0
					self.image = self.bomb_loop[self.frame_ID]
					
			elif player.dead != 0 and player.ID == 2 and player.animation_type != "pickup" and self.active == True:
				self.carried = False
				self.active = False
				self.player.bomb = False
				self.x_speed = (player.speed * player.x_direction)
				self.frame_ID = 0
				self.image = self.bomb_loop[self.frame_ID]
				
			
			if player.animation_type == "pickup" and player.frame_ID == 15:
				self.image = self.no_image
			
		if self.countdown >= self.boom_time:
			if self.countdown == self.boom_time:
				self.boom_sfx.play_once()
			if self.carried == True and self.player.dead == 0:
				self.player.dead = 1
				self.player.animation_type = "boom"
				self.live = True
				self.player.bomb = False
				self.player.frame_ID = 1
				self.rect[1] -= 100
				self.rect[0] -= 100
			elif self.frame_ID == 1:
				self.rect[1] -= 75
				self.rect[0] -= 75
				
			self.frame_ID += 1
			self.image = load_image("Images/TNT-explosion-frames/TNT-explosion-" + str(10000 + self.frame_ID)[1:] + ".png")
			size = self.image.get_rect()
			self.rect[2] = size[2]
			self.rect[3] = size[3]
			
			for item in objects:
					if item.type == "gate" and item.ID == 4 and item.transition_counter != 500:
						if abs(self.rect[0] - item.rect[0]) < 200:
							item.trigger(10)
			
			if self.frame_ID >= 9:
				self.live = False
				self.image = self.bomb
				self.rect[0] = self.start_location[0]
				self.rect[1] = self.start_location[1]
				self.countdown = 0
				self.carried = False
				self.active = False
				self.frame_ID = 1			
		else:
			if self.frame_ID > 4:
				self.frame_ID = 0
				
		if self.carried == True and self.image == self.no_image:
			self.rect = [self.player.rect[0] - map_location[0], self.player.rect[1] - map_location[1]  + 887, self.rect[2], self.rect[3]]
			if self.player.facing == 1:
				self.rect[0] += 175
				
		self.interacting_timer += 1
		if self.countdown != 0:
			self.countdown += 1
			if self.carried == False and self.countdown < self.boom_time:
				self.image = self.bomb_loop[self.frame_ID]
		if self.countdown == 2:
			self.hiss_sfx.play_once()
		self.rect[0] += self.x_speed
		
		self.frame_ID += 1
		
		
	def test_landed(self, player, offset):
		return(False)
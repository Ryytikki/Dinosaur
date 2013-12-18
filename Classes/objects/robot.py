import pygame, sys, math, os
from pygame.locals import *
from Classes.play_music import Play_Music

def load_image(name):
	full_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	image = pygame.image.load(full_path + "\\"+ name).convert_alpha()
	return(image)

class Robot(pygame.sprite.Sprite):
		
	def __init__(self, location):
		pygame.sprite.Sprite.__init__(self)	
		self.image = load_image("Images/miner2-run/miner2-running0001.png")
		self.rect = self.image.get_rect()
		self.rect.center = location
		self.rect[2] += 15
		
		self.start_location = location
		
		self.run = []
		self.stand = []
		self.jump = []
		self.frame_ID = 0
		
		self.running = False
		self.active = False
		self.boulder = []
		self.destruction_timer = 0
		
		self.speed = 8
		self.x_direction = 0
		self.facing = -1
		
		self.y_speed = 0
		self.jumping = False
		
		self.pick_sfx = Play_Music("//sfx//robots-picking-at-rocks.ogg", -1)
		self.walk_sfx = Play_Music("//sfx//robot-walk.ogg", -1)
		self.boom_sfx = Play_Music("//sfx//boulder-explode.ogg", -1)

		self.walking = False
		self.picking = False
		
		
		self.type = "robot"
		
		self.pre_buffer()
		
	def pre_buffer(self):
		for i in range(1,13):
			self.run.append(load_image("Images/miner2-run/miner2-running" + str(10000 + i)[1:] + ".png"))
		for i in range(1,13):
			self.stand.append(load_image("Images/miner2/miner2" + str(10000 + i)[1:] + ".png"))
		for i in range(1,13):
			self.jump.append(load_image("Images/miner/miner-" + str(10000 + i)[1:] + ".png"))
		
	def update(self, map_location, map, players):
	
		if self.active == True:
					
			if self.boulder.rect.colliderect(self.rect) and self.rect[0] - self.boulder.rect[0] < 100 and self.boulder.rect[0] - self.rect[0] < 100	:
				self.walk_sfx.stop()
				self.walking = False
				if self.picking == False:
					self.pick_sfx.play()
					self.picking = True
				self.x_direction = 0
				if self.rect[0] < self.boulder.rect[0]:
					self.facing = -1
					self.image = pygame.transform.flip(self.stand[self.frame_ID], 1, 0)
				else:
					self.facing = 1
					self.image = self.stand[self.frame_ID]
					
				self.destruction_timer += 1
				self.boulder.health -= 1
				self.boulder.show_health = True
				if self.destruction_timer > 450:
					self.boulder.health = 450
					self.boulder.show_health = False
					self.boom_sfx.play_once()
					self.boulder.dead = True
					self.boulder.respawn = True
					self.active = False
					self.boulder = []
					self.destruction_timer = 0
					self.pick_sfx.stop()
					
				if self.frame_ID > 10:
					self.frame_ID = 0
			else:
				if self.walking == False:
					self.walk_sfx.play()
					self.walking = True
				self.pick_sfx.stop()
				self.picking = False
				if self.rect[0] < self.boulder.rect[0]:
					self.x_direction = 1
					self.facing = 1
					self.image = pygame.transform.flip(self.run[self.frame_ID], 1, 0)
				else:
					self.x_direction = -1
					self.facing = -1
					self.image = self.run[self.frame_ID]
					
				if self.frame_ID > 10:
					self.frame_ID = 0
					
				self.rect[0] += self.x_direction * self.speed
		else:
			if abs(self.rect[0] - self.start_location[0]) > 100:
				if self.walking == False:
					self.walk_sfx.play()
					self.walking = True
				self.pick_sfx.stop()
				self.picking = False
				if self.rect[0] < self.start_location[0]:
					self.x_direction = 1
					self.facing = 1
					self.image = pygame.transform.flip(self.run[self.frame_ID], 1, 0)
				else:
					self.x_direction = -1
					self.facing = -1
					self.image = self.run[self.frame_ID]
					
				if self.frame_ID > 10:
					self.frame_ID = 0
					
				self.rect[0] += self.x_direction * self.speed
			else:
				self.image = self.jump[self.frame_ID]
				self.walk_sfx.stop()
				if self.frame_ID > 10:
					self.frame_ID = 0
				
		if map.ground_collision(self, [0,422]) == False:
			self.y_speed += 1
			self.rect[1] += self.y_speed
		else:
			self.y_speed = 0
			
		self.frame_ID += 1
		
		test_rect = [self.rect[0] + map_location[0], self.rect[1] + map_location[1] - 832, self.rect[2], self.rect[3]]
		
		for player in players:
			if player.player_ID == player.ID:
				self.walk_sfx.locate(test_rect[0] - player.rect[0], test_rect[1] - player.rect[1])
				self.pick_sfx.locate(test_rect[0] - player.rect[0], test_rect[1] - player.rect[1])
				self.boom_sfx.locate(test_rect[0] - player.rect[0], test_rect[1] - player.rect[1])

	def test_landed(self, player, offset):
		return(False)
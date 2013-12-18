import pygame, sys, math, os
from pygame.locals import *
from Classes.play_music import Play_Music

def load_image(name):
	full_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	image = pygame.image.load(full_path + "/"+ name).convert_alpha()
	return(image)

class Block(pygame.sprite.Sprite):
		
	def __init__(self, location, map):
		pygame.sprite.Sprite.__init__(self)		
		self.image = load_image("Images/block.png")
		self.block_image = self.image
		
		self.explode_img = []
		for i in range(1,15):
			self.explode_img.append(load_image("Images/expload/boulder-explosion-" + str(10000 + i)[1:] + ".png"))
		self.rect = self.image.get_rect()
		self.rect.center = location
		self.start_location = location
		self.respawn = False
		
		self.roll = []
		self.x_direction = 0
		
		for i in range(1, 32):
			self.roll.append(load_image("Images/roll/roll-" + str(10000 + i)[1:] + ".png"))
		
		self.loc = self.rect
		self.map = 0#map
			
		self.type = "block"
		
		self.jumping = False
		self.y_speed = 0
		self.speed = 0
		
		self.angle = 0
		
		self.active = False
		self.dead = False
		self.dead_count = 0
		self.boom_timer = 0
		
		self.health = 450.0
		self.show_health = False
		self.health_image = pygame.Surface((169, 45), pygame.SRCALPHA, 32)
		self.health_background = load_image("Images/healthbar-background.png")
		self.health_foreground = load_image("Images/healthbar-bar.png")
		
		
		self.roll_sfx = Play_Music("//sfx//boulder-rolling.ogg", -1)
		self.boom_sfx = Play_Music("//sfx//rock-crumble.ogg", -1)
		
	def update(self, player_list, map, map_location, objects, robots):
		#self.rect[1] -= map_location[2]
		if self.dead == False:
			if map[0].ground_collision(self, [0,422]) == False:
				self.y_speed += 1
				self.rect[1] += self.y_speed
			else:
				self.y_speed = 0
			moving = 0
			test_rect = [self.rect[0] + map_location[0], self.rect[1] + map_location[1] - 832, self.rect[2], self.rect[3]]
			
			active = 0
			for object in objects:
				if object.type == "block" and object.active == True:
					active += 1
					
			if active == 1 and self.active == True:
				active = 0
				
			for player in player_list:
				if player.ID == 1:
					if player.hit_rect.colliderect(test_rect):
						if player.interacting == True:
							if player.hit_rect[1] > test_rect[1] + 40 and active < 1:
								if player.animation_type != "push":
									self.roll_sfx.play()
									player.animation_type = "push"
									player.frame_ID = 0
								if player.x_direction == -1: 
									if test_rect[0] < player.hit_rect[0] - 100:
										self.speed = 10 * player.x_direction
										self.angle += 1
										self.active = True
								elif player.x_direction == 1:  
									if test_rect[0] > player.rect[0] + 100:
										self.speed = 10 * player.x_direction
										self.angle -= 1
										self.active = True
								ping = []
								for robot in robots:
									if robot.boulder == []:
										ping = robot
									elif robot.boulder == self:
										ping = []
										break;
										
								if ping != []:
									ping.boulder = self
									ping.active = True
									
						else:
							for object in objects:
								if object.type == "block":
									object.active = False
									object.roll_sfx.stop()
									
					else:
						self.speed = 0
						self.roll_sfx.stop()
				elif player.ID == 1:
					self.active = False
				if player.animation_type == "push" and active == 0 and self.active == False:
					if player.x_direction != 0:
						player.animation_type = "run"
					else:
						player.animation_type = "idle"
						
					player.frame_ID = 0
				
			if self.show_health == True:
				self.health_image.blit(self.health_background, (0,0))
				overlay = pygame.Surface((169, 45), pygame.SRCALPHA, 32)
				overlay.blit(self.health_foreground, (0,0))
				overlay.fill(0, (0, 0, ( 1- self.health / 450.0) * 169 ,45))
				print self.health / 450
				self.health_image.blit(overlay, (0,0))
				#self.image.blit(self.health_image, (0,0))

			if self.active == False:
				self.speed = 0
				
			if self.angle > 30:
				self.angle = 0
			if self.angle < 0:
				self.angle = 30
			
			self.image = self.roll[self.angle]
					
			self.rect[0] += self.speed
		else:
			self.explode(map_location, player_list)

		
	def spawner_update(self, map_location, map, players):
		if self.dead == True:
			self.rect[1] = 1950
			self.explode(map_location, players)
		elif self.rect[1] < 1950:
			self.y_speed += 1
			self.rect[1] += self.y_speed
			self.boom_timer += 1
		else:
			self.y_speed = 0
			self.dead = True
		
	def explode(self, map_location, players):
		if self.dead_count > 14:
			self.dead = False
			if self.respawn == False:
				self.rect[1] = -1000000
			else:
				self.rect.center = self.start_location
			self.image = self.block_image
			self.dead_count = 0
			self.boom_timer = 0
		elif self.dead_count == 1:
			self.show_health = False
			self.boom_sfx.play_once()
			self.image = self.explode_img[self.dead_count - 1]
			self.dead_count += 1
			test_rect = [self.rect[0] + map_location[0], self.rect[1] + map_location[1] - 832, self.rect[2], self.rect[3]]
			for player in players:
				if player.player_ID == player.ID:
					self.boom_sfx.locate(test_rect[0] - player.rect[0], test_rect[1] - player.rect[1])
		else:
			self.image = self.explode_img[self.dead_count - 1]
			self.dead_count += 1
		
	def test_landed(self, player, offset):
		return False
		## Corrected rect for floating blocks
		# collide_rect = [self.rect[0] + offset[0], self.rect[1] + offset[1], self.rect[2], self.rect[3]]
		##Check the player is within the hitbox and is colliding with the block (first check is for air, second for ground)
		# if player.rect[1] >= self.rect[1] - 100 + offset[1] and player.rect[1] < self.rect[1] - 50 + offset[1] and player.dropping == 10:
			# if (player.hit_rect.colliderect(collide_rect) or player.hit_rect.colliderect(self.rect)):
				# if player.y_speed < 0:
					# player.rect[1] = self.rect[1] - 100 + offset[1]
					# player.jumping = False
					# player.animation_type = "land"
					# player.y_speed = 0
					# player.frame_ID = 0	
				
				# return(True)
			# else:
				# return(False)
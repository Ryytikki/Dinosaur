import pygame, sys, math, os, time
from pygame.locals import *
from Classes.switch import switch
from Classes.play_music import Play_Music

GRAVITY = 1
HEALTH_DAMAGE = -250
	
def load_image(name):
	full_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	image = pygame.image.load(full_path + "\\"+ name).convert_alpha()
	rect = image.get_rect()
	return(image)
	
def change_image(type, facing, ID):
	image = load_image("Images/Players/" + ID + "/"+ type + ".png")
	if facing == 1:
		image = pygame.transform.flip(image, 1, 0)

	return image
	
class Player(pygame.sprite.Sprite):

	def __init__(self, ID):
		pygame.sprite.Sprite.__init__(self)		
		
		self.image = load_image("Images" + "\Players\\" + str(ID) + "\Idle/idle-0001.png")
		self.rect = self.image.get_rect()
		self.rect.center = (400.0, 500.0)
		
		self.reset = False
		
		self.hit_image = load_image("Images" + "\Players\\" + str(ID) + "/hit.png")
		self.hit_rect = self.hit_image.get_rect()
		self.hit_rect.center = self.rect.center
		
		self.land_rect = self.hit_image.get_rect()
		if ID != 2:
			self.land_image = load_image("Images\\Players\\1\\player_land.png")
			self.land_rect = self.land_image.get_rect()
			self.land_rect.center = self.rect.center
			
		self.x_direction = 0
		self.prev_x = 0
		self.speed = 10 + (5 * (ID - 1))
		
		self.jumping = False
		self.y_speed = 0
		self.landed = False
		self.dropping = 10
		
		self.facing = 1
		self.animation_type = "idle"
		self.frame_ID = 0

		self.player_ID = 1
		self.ID = ID
		self.dead = False
		self.type = "player"
		
		self.interacting = False
		self.bomb = False
		
		self.health = 10
		
		self.idle = []
		self.run = []
		
		self.idle_counter = 0
		
		self.run_sfx = Play_Music("//sfx//" + str(self.ID) + "-run.ogg", -1)
		self.jump_sfx = Play_Music("//sfx//" + str(self.ID) + "-jump.ogg", -1)
		
		self.pre_buffer()
	
	def pre_buffer(self):
		if self.ID == 1:
			for i in range(1,109): 
				self.idle.append(load_image("Images/Players/1/Idle/idle-" + str(10000 + i)[1:] + ".png"))
			for i in range(1,17):
				self.run.append(load_image("Images/Players/1/Running/run-" + str(10000 + i)[1:] + ".png"))
		else:
			for i in range(1,101): 
				self.idle.append(load_image("Images/Players/2/Idle/idle-" + str(10000 + i)[1:] + ".png"))
			for i in range(1,17):
				self.run.append(load_image("Images/Players/2/Running/run-" + str(10000 + i)[1:] + ".png"))
		
	def update(self, current_ID, item_list, player_list, map, map_location):
		if self.dead != 1:
			if current_ID == self.ID:
				self.keyboard_controls()
			
			self.update_image()
			if self.ID == 1:
				self.land_rect.center = [self.rect[0] + 25, self.rect[1] + 25]
			if self.ID == 1:
				self.hit_rect.center = [self.rect[0] + 110, self.rect[1] + 140]
			else:
				self.hit_rect.center = [self.rect[0] + 125 + 25 * self.facing, self.rect[1] + 150]
			#self.image.blit(self.hit_image, (self.hit_rect[0] - self.rect[0], self.hit_rect[1] - self.rect[1]))
			self.run_collisions(item_list, player_list, map, map_location)
			if self.dropping < 10:
				self.dropping += 1
			self.idle_counter += 1
			
			if self.idle_counter > 9000:
				self.reset = True
		else:
			self.play_dead()
		
		if self.health <= 0:
			self.dead = 1
		
	def keyboard_controls(self):
		# Keyboard controls
		for event in pygame.event.get():
			# Quits the program
			if event.type == QUIT: 
				pygame.quit()
			
			# Key press handling
			if event.type == KEYDOWN:
				# If escape is pressed, close
				if event.key == K_F12:
					pygame.event.post(pygame.event.Event(QUIT))
					
				if event.key == K_F1:
					self.reset = True
				
				# X movement
				if self.jumping == False or self.jumping == True:
					if event.key == K_a or event.key == K_LEFT:
						self.x_direction = -1
						self.idle_counter = 0
						
					if event.key == K_d or event.key == K_RIGHT:
						self.x_direction = 1
						self.idle_counter = 0
						
				if event.key == K_1:
					self.player_ID = 1
					self.idle_counter = 0
				
				if event.key == K_2:
					self.player_ID = 2
					self.idle_counter = 0
				
				# Jumping
				if event.key == K_w or event.key == K_UP:
					if self.jumping == False or self.ID == 3:
						self.jumping = True
						self.jump_sfx.play_once()
						self.y_speed = 12
						if self.ID == 2:
							self.y_speed += 5
					
				# Enabling interaction
				if event.key == K_SPACE:
					self.interacting = True

				if event.key == K_s or event.key == K_DOWN:
					self.dropping = True
			
			# Key release hadling
			if event.type == KEYUP:
				# Refreshes the events
				pygame.event.pump()
				# Creates a list of pressed keys
				key_list = pygame.key.get_pressed()
				# If A is up
				if event.key == K_a or event.key == K_LEFT:
					# But D is down
					if key_list[pygame.K_d] == True or key_list[pygame.K_RIGHT] == True:
						# Swap directions
						self.x_direction = 1
					# But D is up
					else:
						# Stop moving
						self.x_direction = 0
				# Same for D
				if event.key == K_d or event.key == K_RIGHT:
					if key_list[pygame.K_a] == True or key_list[pygame.K_LEFT] == True:
						self.x_direction = -1
					else:
						self.x_direction = 0
						
			# Disabling interaction
				if event.key == K_SPACE:
					self.interacting = False
				
				if event.key == K_s or event.key == K_DOWN:
					self.dropping = False
						
	def update_image(self):

		if self.facing is not self.x_direction:
			# if they're swapping directions
			if self.x_direction is not 0:
				# Flip the way they're facing and refresh the image
				self.facing = self.x_direction
				self.animation_type = "run"
				if self.run_sfx.playing == False:
					self.run_sfx.play()
				self.image = self.run[0]
			else:
				# If they're stopping but havent already started the slow animation
				if self.prev_x is not 0:
					# play the slow animation
					self.animation_type = "slow"
					if self.bomb == False:
						self.image = change_image("slow", self.facing, str(self.ID))
					else:
						self.image = change_image("slow-TNT", self.facing, str(self.ID))
					# Dont want to change the direction they're facing or the stop image will flip
					if self.x_direction is not 0:
						self.facing = self.x_direction
					# Reset the counter
					self.frame_ID = 0
		
		#If the player starts moving from standing but doesnt change direction
		if self.x_direction is not self.prev_x and self.prev_x is 0:
			self.animation_type = "run"
			if self.run_sfx.playing == False:
				self.run_sfx.play()
			self.image = self.run[0]
			self.frame_ID = 0
		
		# if the player is slowing down
		if self.animation_type is "slow":
			if self.frame_ID >= 3:
				# Reset the animation to the standing player
				self.animation_type = "idle"
				self.image = self.idle[0]
				self.frame_ID = 0
			#else:
				# If it hasnt finished slowing, move slightly forwards
				#self.rect[0] += 2 * self.facing * self.speed / (self.frame_ID + 1)

		self.prev_x = self.x_direction
		
		if self.run_sfx.playing == True and self.animation_type != "run":
			self.run_sfx.stop()
		
		# Vertical stuff
		if self.jumping == True:
			self.y_speed -= GRAVITY
			# Going up
			if self.y_speed > 0:
				if self.animation_type == "jump" and self.frame_ID > 5 and self.animation_type != "tuck" and self.ID == 2:
					self.animation_type = "tuck"
					if self.bomb == False:
						self.image = change_image("tuck", self.facing, str(self.ID))
					else:
						self.image = change_image("tuck-TNT", self.facing, str(self.ID))
				elif self.animation_type != "tuck" and self.animation_type != "jump":
					self.animation_type = "jump"
					if self.bomb == False:
						self.image = change_image("jump", self.facing, str(self.ID))
					else:
						self.image = change_image("jump-TNT", self.facing, str(self.ID))
					self.frame_ID = 0
			# Going down
			else:
				if self.animation_type is not "jump2":
					self.animation_type = "jump2"
					self.frame_ID = 0
				if self.ID is not 2:
					self.image = change_image("jump2", self.facing, str(self.ID))
		
		if self.animation_type == "land":
			if self.frame_ID >= 1:
				if self.x_direction == 0:
					self.animation_type = "idle"
					self.image = self.run[0]
					self.frame_ID = 0
				else:
					self.animation_type = "run"
					if self.run_sfx.playing == False:
						self.run_sfx.play()
					if self.bomb == False:
						self.image = change_image("slow", self.facing, str(self.ID))
					else:
						self.image = change_image("slow-TNT", self.facing, str(self.ID))
				self.frame_ID = 0

		self.rect[1] -= self.y_speed
		
		# These animations override even jumping
		if self.animation_type == "sinking":
			self.x_direction = 0
			self.jumping = False
				
		# Play the animations
		self.frame_ID += 1
		if self.bomb == False:
			for case in switch(self.animation_type):
				if case("idle"):

					self.image = self.idle[self.frame_ID]
					if self.facing == 1:
						self.image = pygame.transform.flip(self.image, 1, 0)
					if self.frame_ID > 106 and self.ID == 1:
						self.frame_ID = 0
					if self.frame_ID > 98 and self.ID == 2:
						self.frame_ID = 0
					break;
				if case("run"):
					self.image = self.run[self.frame_ID]
					if self.facing == 1:
						self.image = pygame.transform.flip(self.image, 1, 0)
					if self.frame_ID > 14 and self.ID == 1:
						self.frame_ID = 0
					if self.frame_ID > 14 and self.ID == 2:
						self.frame_ID = 0
					break;
				if case("jump2") and self.ID == 2:
					self.image = change_image("Falling/flap-" + str(10000 + self.frame_ID)[1:], self.facing, str(self.ID))
					if self.frame_ID > 3:
						self.frame_ID = 0
					break;
				elif self.animation_type == "push" and self.ID == 1:
					self.image = change_image("boulder-push//boulder-push-" + str(10000 + self.frame_ID)[1:], self.facing, str(self.ID))
					if self.frame_ID > 14:
						self.frame_ID = 0
					break;
					
		else:
			if self.animation_type == "idle":
				self.image = change_image("idle-TNT/idle" + str(10000 + self.frame_ID)[1:], self.facing, str(self.ID))
				if self.frame_ID > 99 and self.ID == 2:
					self.frame_ID = 0
			elif self.animation_type == "run":
				self.image = change_image("running-TNT/running-TNT-" + str(10000 + self.frame_ID)[1:], self.facing, str(self.ID))
				if self.frame_ID > 15 and self.ID == 2:
					self.frame_ID = 0
			elif self.animation_type == "jump2":
				self.image = change_image("flap-wTNT/flapping-flash-TNT" + str(10000 + self.frame_ID)[1:], self.facing, str(self.ID))
				if self.frame_ID > 3:
					self.frame_ID = 0

	def run_collisions(self, item_list, player_list, map, map_location):
		# Have to define a new variable for some reason
		map_loc = [0,0]
		map_loc[0] = map_location[0]
		map_loc[1] = map_location[1] - 432
		
		# Reset for next loop
		self.landed = False 

		# Check if falling
		if self.jumping == True:
			# If hit ground
			if map[self.ID - 1].ground_collision(self, [map_location[0], map_location[1]]) == True:
				# Reset the player to their walking values
				self.jumping = False
				self.landed = True
				self.animation_type = "land"
				if self.y_speed <= HEALTH_DAMAGE:
						self.health -= 1
				self.y_speed = 0
				# Reset the image
				self.frame_ID = 0
				self.image = change_image("land", self.facing, str(self.ID))
				for object in item_list:
					if object.type == "button":
						object.float = False
		# Still need to check if they've walked off a ledge/down a slope
		elif map[self.ID - 1].ground_collision(self, map_location) == True:
				self.landed = True

		# Player on player collisions - NEEDS FIXING
		for player in player_list:
			# If player 2 is on top of player 1
			if self.ID == 2 and player.ID != 2 and self.hit_rect.colliderect(player.rect) and self.landed == False:
				# this if statement is horrible and ugly and doesnt work - fix ASAP
				if self.hit_rect[1] - 70 >= player.rect[1] and  self.hit_rect[0] * self.facing < player.hit_rect[0] + 30 and self.hit_rect[0] * self.facing > player.hit_rect[0] - 20 and self.y_speed <= 0 and abs(self.hit_rect[1] - player.hit_rect[1]) > 5:
					
					# Same as before just with the player
					self.landed = True
					self.rect[1] = player.rect[1] - 70
					self.jumping = False
					if self.y_speed <= HEALTH_DAMAGE:
						self.health -= 1
					self.y_speed = 0
					# Test for later - possible addition?
					# self.facing = player.facing
					
					self.animation_type = "idle"
					
					# Move velociryy along with the other dino
					self.rect[0] += player.speed * player.x_direction
					if player.animation_type == "slow":
						self.rect[0] += 2 * player.facing * player.speed / (player.frame_ID + 1)
					break
		
		# Check if the player is on top of an object
		for object in item_list:
			if object.test_landed(self, map_loc) == True:
				self.landed = True
		
		# If the player was on the ground and is now falling
		if self.landed == False and self.jumping == False:
			self.jumping = True
			# automatically jumps to the down fall image
			if self.animation_type != "jump2":
				self.animation_type = "jump2"
				self.frame_ID = 0
				if self.ID != 2:
					self.image = change_image("jump2", self.facing, str(self.ID))

	def play_dead(self):
		if self.animation_type == "sinking":
			if self.frame_ID < 15:
				self.frame_ID += 1
				self.image = change_image("Sinking/sinking-" + str(10000 + self.frame_ID)[1:], self.facing, str(self.ID))
			elif self.frame_ID < 30:
				self.image = change_image("Sinking/sinking-" + str(10000 + int(self.frame_ID / 2))[1:], self.facing, str(self.ID))
				self.frame_ID += 1
				#play sinking shit
			else:
				self.health -= 1
				self.dead = 2
				self.animation_type = "idle"
				self.facing = 1
				self.frame_ID = 0
		elif self.animation_type == "squashed":
			self.image = change_image("squished/squished-" + str(10000 + self.frame_ID)[1:], self.facing, str(self.ID))
			self.frame_ID += 1
			
			if self.frame_ID > 15:
				self.dead = 2
				self.animation_type = "idle"
				self.facing = 1
				self.frame_ID = 0	
				
		elif self.animation_type == "pickup":
				self.image = change_image("bomb-lift-frames/bomb-pick-up" + str(10000 + self.frame_ID)[1:], self.facing, str(self.ID))
				self.frame_ID += 1
				self.dropping = False
				self.x_direction = 0
				self.run_sfx.stop()
				if self.frame_ID > 22:
					self.animation_type = "idle"
					self.dead = 0
					self.frame_ID = 0
		elif self.animation_type == "boom":
			self.image = change_image("explosion-death/explosion-" + str(10000 + self.frame_ID)[1:], self.facing, str(self.ID))
			self.frame_ID += 1
			self.x_direction = 0
			if self.frame_ID > 72:
				self.dead = 2
				self.animation_type = "idle"
				self.facing = 1
				
				self.frame_ID = 0	
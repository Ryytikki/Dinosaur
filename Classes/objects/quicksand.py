import pygame, sys, math, os
from pygame.locals import *

def load_image(name):
	full_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	image = pygame.image.load(full_path + "\\"+ name)
	return(image)
	

class Quicksand(pygame.sprite.Sprite):
		
	def __init__(self, location, width):
		pygame.sprite.Sprite.__init__(self)
		
		# Images to be used
		self.tile = [load_image("Images\\maps\\sand\\sand-tile" + str(i) + ".png") for i in range (1,3)]
		start_img = load_image("Images\\maps\\sand\\begin-sand.png")
		end_img = load_image("Images\\maps\\sand\\end-sand.png")
				
		self.image = pygame.Surface((200 * width, 200), pygame.SRCALPHA, 32)
		self.overlay = pygame.Surface((200 * (width), 200), pygame.SRCALPHA, 32)
		placeholder = pygame.Surface((200 * (width - 2), 600), pygame.SRCALPHA, 32)
		
		# Blit the start and end onto the overlay
		self.overlay.blit(start_img, (0,0))
		self.overlay.blit(end_img, ((width - 1) * 200, 0))
		
		# Draw the main blocks into the placeholder
		for i in range(0, width - 2):
			placeholder.blit(self.tile[0], (200 * i, 0))
		
		# Only want to collide with the main blocks
		self.hit_rect = placeholder.get_rect()
		# Print the sand and then the start/end over the top
		self.image.blit(placeholder, (200,145))
		self.image.blit(self.overlay, (0,0))	
		
		# Define the rect and width for positioning purposes
		self.rect = self.image.get_rect()
		self.rect.topleft = (location[0] - 200, location[1])
		self.width = width
		
		self.type = "quicksand"
		
		# Frame ID for animating
		self.frame_ID = 0
		self.dirty = True
	def update(self, player_list, object_list, offset):
			# Update the collision rect for the quicksand block
			self.hit_rect = (self.rect[0] + 200, self.rect[1] + 175, self.hit_rect[2] ,self.rect[3] *2 - 130	)
			
			# Update the image
			self.frame_ID += 1
			if self.frame_ID == 20:
				self.update_image()
			elif self.frame_ID == 40:
				self.frame_ID = 0
				self.update_image()
					
			
			
			# Run collisions
			self.player_sinking(player_list, offset)
			self.object_sinking(object_list, offset)
	
	def update_image(self):

			
			placeholder = pygame.Surface((200 * (self.width), 600), pygame.SRCALPHA, 32)
			
			for i in range (0, self.width):
				placeholder.blit(self.tile[int(self.frame_ID/20)], (200 * i, 0))
			
			self.image = pygame.Surface((200 * self.width, 200), pygame.SRCALPHA, 32)
			self.image.blit(placeholder, (0,130))
			self.image.blit(self.overlay, (0,0))
	
	def player_sinking(self, player_list, offset):
		
		test_rect = [self.rect[0] + offset[0], self.rect[1] + offset[1] - 1200, self.rect[2], self.rect[3]]
		test_hit_rect = [self.hit_rect[0] + offset[0], self.hit_rect[1] + offset[1] - 1200, self.hit_rect[2], self.hit_rect[3]]
		for player in player_list:
			if player.rect.colliderect(test_rect) and player.rect[1] >= test_rect[1] + 30:
				player.landed = True
				if player.y_speed < 0:
					player.rect[1] = test_rect[1] + 30
					player.jumping = False
					player.animation_type = "land"
					player.y_speed = 0
					player.frame_ID = 0		
			if player.ID != 2 and player.hit_rect.colliderect(test_hit_rect):
				if player.animation_type != "sinking":
					player.animation_type = "sinking"
					player.x_direction = 0
					player.frame_ID = 0
					player.dead = 1 
					print "Test"
					
	def object_sinking(self, object_list, offset):
		test_hit_rect = [self.hit_rect[0] + offset[0], self.hit_rect[1] + offset[1] - 1200, self.hit_rect[2], self.hit_rect[3]]

		for object in object_list:
			if object.type == "block":
				if object.rect.colliderect(test_hit_rect) and object.rect[1] >= test_hit_rect[1] + 30 and object.y_speed != 0:
					object.y_speed = 0.1
					
	def test_landed(self, player, offset):
		return(False)
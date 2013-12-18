import pygame, sys, math, os
from pygame.locals import *
from Classes.play_music import Play_Music

def load_image(name):
	full_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	image = pygame.image.load(full_path + "\\"+ name).convert_alpha()
	return(image)
	
class Gate(pygame.sprite.Sprite):
		
	def __init__(self, location, ID):
		pygame.sprite.Sprite.__init__(self)	
		if ID != 0 and ID != 4:
			self.gate = load_image("Images\\gate.png")
			self.base = load_image("Images\\gate-portal.png")
		
			self.image = pygame.Surface((135,430), pygame.SRCALPHA, 32)
			self.image.blit(self.gate, (35,0))
			self.image.blit(self.base, (0, 390))
			
		elif ID == 0:
			self.gate = load_image("Images\\lift.png")
			self.base = load_image("Images\\lift-wall.png")
			self.gate_sfx = Play_Music("\\sfx\\crane-lifting.ogg", -1)
			self.image = pygame.Surface((319, 550), pygame.SRCALPHA, 32)
			self.image.blit(self.gate, (40,0))
			self.image.blit(self.base, (0,330))
			location[1] -= 70
		else:
			self.image = pygame.Surface((250,750), pygame.SRCALPHA, 32)
			self.image.blit(load_image("Images\\crumbly-wall.png"), (0,0))
			self.boom = []
			for i in range(1, 25):
				self.boom.append(load_image("Images\\crumble-wall\\cumble-wall-" + str(10000 + i)[1:] + ".png"))
		
		self.rect = self.image.get_rect()
		self.rect.center = location
		
		self.gate_timer = -1
		self.ID = ID
		self.activation_confirmation = 0
		self.transition_counter = 0
		self.type = "gate"
		
		self.open = False
		
		self.animating = 0
		self.frame_ID = 0
		
	def update(self, players, map_location):

		if self.activation_confirmation == 10 and (self.transition_counter > 300 or self.ID == 0):
			self.open = True
		else:
			self.open = False
			test_rect = [self.rect[0] + map_location[0], self.rect[1] + map_location[1] - 832, self.rect[2], self.rect[3]]
			for player in players:
				if player.hit_rect.colliderect(test_rect):
					if player.hit_rect[0] < test_rect[0]:
						player.rect[0] -= player.speed
					else:
						player.rect[0] += player.speed
						
		if self.ID == 0:
			for player in players:
				if player.player_ID == player.ID:
					test_rect = [self.rect[0] + map_location[0], self.rect[1] + map_location[1] - 832, self.rect[2], self.rect[3]]
					self.gate_sfx.locate(test_rect[0] - player.rect[0], test_rect[1] - player.rect[1] / 2)
						
		if self.animating == 1:
			self.open_gate()
		elif self.animating == -1:
			self.close_gate()
	
					
	def trigger(self, trigger_code):
		print trigger_code
		if trigger_code == 10:
			self.activation_confirmation = 10
			self.gate_timer = 99999
			self.animating = 1
			self.transition_counter = 0
			if self.ID == 0:
				self.gate_sfx.play_once()
		elif trigger_code > 0:
			self.activation_confirmation += trigger_code
			print self.activation_confirmation
			if self.activation_confirmation >= 10:
				self.activation_confirmation = 10
				self.gate_timer = 99999
				self.animating = 1
				self.transition_counter = 0
		else:
			self.activation_confirmation += trigger_code
			print self.activation_confirmation
			if self.activation_confirmation < 10:
				self.gate_timer = 0
				if self.activation_confirmation - trigger_code == 10 or trigger_code == -10:
					self.animating = -1
				self.transition_counter = 0
				
			elif self.activation_confirmation == 10:
				self.activation_confirmation = 10
				self.gate_timer = 99999
				self.animating = 1
				self.transition_counter = 0

				
	def open_gate(self):
		if self.ID != 0 and self.ID != 4:
			self.image = pygame.Surface((135,430), pygame.SRCALPHA, 32)
			self.image.blit(self.gate, (35, self.transition_counter))
			self.image.blit(self.base, (0, 390))
			self.transition_counter += 10
			
			if self.transition_counter > 400:
				self.animating = 0
		elif self.ID != 4:
			self.image = pygame.Surface((319, 550), pygame.SRCALPHA, 32)
			self.image.blit(self.gate, (40,0))
			self.image.blit(self.base, (0,330 - self.transition_counter))
			self.transition_counter += 3.25
			if self.transition_counter > 330:
				self.animating = 0
		else:
			self.image.fill(0)
			self.image = pygame.Surface((250, 750), pygame.SRCALPHA, 32)
			self.transition_counter = 500
			self.image.blit(self.boom[self.frame_ID], (10,0))
			self.frame_ID += 1
			if self.frame_ID > 23:
				self.animating = 0
				self.frame_ID = 0
				
	def close_gate(self):
		if self.ID != 0:
			print "Closing"
			self.image = pygame.Surface((135,430), pygame.SRCALPHA, 32)
			self.image.blit(self.gate, (35, 400 - self.transition_counter))
			self.image.blit(self.base, (0, 390))
			self.transition_counter += 10
			
			if self.transition_counter > 400:
				self.animating = 0
				
		elif self.ID != 4:
			
			self.image = pygame.Surface((319, 550), pygame.SRCALPHA, 32)
			self.image.blit(self.gate, (40,0))
			self.image.blit(self.base, (0,self.transition_counter))
			self.transition_counter += 10
			
			if self.transition_counter > 330:
				self.animating = 0	
		else:
			self.animating = 0
	def test_landed(self, player, offset):
		return(False)
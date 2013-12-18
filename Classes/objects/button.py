import pygame, sys, math, os
from pygame.locals import *
from Classes.play_music import Play_Music

def load_image(name):
	full_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	image = pygame.image.load(full_path + "\\"+ name).convert_alpha()
	return(image)
	
class Button(pygame.sprite.Sprite):
		
	def __init__(self, location, type, gate, trigger, gates):
		pygame.sprite.Sprite.__init__(self)	

		for item in gates:
			if item.ID == gate:
				self.gate = item
				break;
		
		self.trigger_ID = trigger
		self.activated = False
		self.activation_delay = 0
		
		self.type = "button"
		self.float = False
		self.float_hit = 0
		
		self.button_type = type
		
		self.plugged = []
		self.unplugged = []
		self.frame_ID = 0
		self.img_type = "unplugged"
		
		self.prebuffer()
		
		
		if type == 2:
			self.geyser = Play_Music("//sfx//geyser-flow.ogg", -1)
			self.geyser.play()
			self.plugged_sfx = Play_Music("//sfx//plugged-geyser.ogg", -1)
		else:
			self.switch_sfx = Play_Music("//sfx//switch.ogg", -1)
		
		if type != 2:
			self.image = load_image("Images\\button" + str(type) + ".png")

		else:
			self.image = self.unplugged[0]
		
		self.rect = self.image.get_rect()
		self.rect.center = location
		
	def update(self, players, objects, map_location):
		test_rect = [self.rect[0] + map_location[0], self.rect[1] + map_location[1] - 832, self.rect[2], self.rect[3]]
		# Standard wall button
		if self.button_type == 0:
			for player in players:
				if player.rect.colliderect(test_rect):
					if player.interacting == True:
						self.button_pressed()
		# Floor button					
		else:
			hit = False
			for player in players:
				if player.hit_rect.colliderect(test_rect) and player.rect[0] - test_rect[0] > -150 and player.rect[0] - test_rect[0] < 50 and self.button_type != 2:
					hit = True
					if self.activated == False:
						self.button_pressed()
			
			for object in objects:
				if object.type == "block":
					if object.rect.colliderect(self.rect) and object.rect[0] - self.rect[0] > -150 and object.rect[0] - self.rect[0] < 50:
						hit = True
						if self.activated == False:
							if self.button_type != 2:
								self.switch_sfx.play_once()
							else:
								self.geyser.stop()
								self.plugged_sfx.play()
							self.button_pressed()

			if hit == False and self.activated == True:
				self.float_hit += 1
				if self.float_hit > 20:
					if self.button_type == 2:
						self.plugged_sfx.stop()
						self.geyser.play()
					self.button_pressed()
					self.float_hit = 0
					self.float = False
		self.activation_delay += 1
		
		if self.button_type == 2:
			self.run_animation()
			for player in players:
				if player.player_ID == player.ID:
					self.geyser.locate(test_rect[0] - player.rect[0], test_rect[1] - player.rect[1])
					self.plugged_sfx.locate(test_rect[0] - player.rect[0], test_rect[1] - player.rect[1])
		
			
	def button_pressed(self):
		if self.activated == False and self.activation_delay > 10:
			self.gate.trigger(self.trigger_ID)
			self.activation_delay = 0
			if self.button_type != 2:
				self.switch_sfx.play_once()
				self.image = load_image("Images\\button" + str(self.button_type) + "-pressed.png")
			self.frame_ID = 0
			self.activated = True
		elif self.activated == True and self.activation_delay > 10:
			self.gate.trigger(self.trigger_ID * -1)
			if self.button_type != 2:
				#self.switch_sfx.play_once()
				self.image = load_image("Images\\button" + str(self.button_type) + ".png")
			self.frame_ID = 0
			self.activated = False
			self.activation_delay = 0
			
	def run_animation(self):
		if self.activated == True:
			self.image = self.plugged[self.frame_ID]
			self.frame_ID += 1
			if self.frame_ID > 7:
				self.frame_ID = 0
			
		else:
			self.float = False
			self.image = self.unplugged[self.frame_ID]
			self.frame_ID += 1
			if self.frame_ID > 9:
				self.frame_ID = 0
				
	def prebuffer(self):
		for i in range(1, 9):
			self.plugged.append(load_image("Images//plugged//plugged-" + str(10000 + i)[1:] + ".png"))
		for i in range(1, 11):
			self.unplugged.append(load_image("Images//unplugged//geyser-" + str(10000 + i)[1:] + ".png"))
			
	def test_landed(self, player, offset):
		return(False)
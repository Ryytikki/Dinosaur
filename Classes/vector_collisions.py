import pygame
from pygame.sprite import *
###############################################################
# Vector based collision system built for cocos2d by Ryytikki #
# Made of 2 parts, the ground map and the entity map          #
# You need to reconvert the map every time it changes with    #
# the convert_map and convert_entities functions. I split     #
# them on the offchance that you'll only want to update one   #
# In this case, entities refer to non-ground platforms or     #
# other floating objects you can stand on                     #
###############################################################

class Collision_map():
	
	def __init__(self, map_file, entity_file, screen_width):	
	
		# Need screen width for later optimisatio
		self.screen_width = screen_width
		
		# Holding arrays for the collision map
		self.x_coord = []
		self.y_coord = []
		# Min/max IDs of the vectors currently on the screen
		self.map_range = [0,0]
		
		# Current location of the collision map
		self.location = [0.0,0.0]
		
		self.convert_map(map_file)
		#convert_entities(map_file)
		
	def convert_map(self, map_file):
		# Convert the collision map to an array of floats
		i = -1
		coord = []
		for coord in map_file:
			i += 1
			# Coordinates stored as strings allows you to hold more info, max coordinate (99999,99999)
			self.x_coord.append(float(coord[0]))
			self.y_coord.append(float(coord[1]))
		# Reset size of the range

		self.map_range[0] = 0
		self.map_range[1] = i 
		
		#self.calc_offset(0)
		
	def calc_offset(self, offset):
		# Calculates the range of vectors that are currently displayed on the screen
		# You wanna run this every time the position of the player is updated

		# Left hand side
		# Point moving off of screen
		if self.x_coord[self.map_range[0]] + offset < 0:
			self.map_range[0] += 1
			# itterates until everything is done
			self.calc_offset(offset)
		
		#Point moving onto screen
		if self.map_range[0] != 0:
			if self.x_coord[self.map_range[0] - 1] + offset > 0:
				self.map_range[0] -= 1
				self.calc_offset(offset)
		
		# Right hand side
		# Off
		if self.x_coord[self.map_range[1]] + offset> self.screen_width:
			self.map_range[1] -= 1
			self.calc_offset(offset)
		# On
		if self.map_range[1] != len(self.x_coord) - 1:
			if self.x_coord[self.map_range[1] + 1] + offset < self.screen_width:
				self.map_range[1] += 1
				self.calc_offset(offset)
	
	# Draws the map as a set of dots connected by lines
	def draw_map(self):
		map_image = pygame.Surface((7000,2400), pygame.SRCALPHA, 32)
		for i in range(self.map_range[0], self.map_range[1]):
			pygame.draw.circle(map_image, (255,255,255), (int(self.x_coord[i]), int(self.y_coord[i])), 5)
			pygame.draw.line(map_image, (255,255,255), (self.x_coord[i], self.y_coord[i]), (self.x_coord[i+1], self.y_coord[i+1]))
		return(map_image)
	
	def ground_collision(self, target, offset):
		# Double check offset for this object
	#	self.calc_offset(offset[0])
		# basic counter for the loops
		i = -1 
		# Location of the vector under the target in the above arrays
		array_ID = 0

		gradient = 0.0
		vector_y = 0.0
		dy = -1.0
		
		# Now to find the vector that the target is over
		i = self.map_range[0]	
		for i in range(self.map_range[0], self.map_range[1]):
			if target.rect[0] >= self.x_coord[i] + offset[0]:
				if target.rect[0] < self.x_coord[i+1] + offset[0]:
					array_ID = i

		# Calculate the gradient of the vector (dy/dx)
		gradient = (self.y_coord[array_ID+1] - self.y_coord[array_ID]) / (self.x_coord[array_ID + 1] - self.x_coord[array_ID])
		# Added this to stop the player moving past immovable walls
		if gradient > -5 and gradient < 5 or 1 == 1:
			# Use the gradient to calculate the height of the vector where the target is
			vector_y = gradient * (target.rect[0]- self.x_coord[array_ID] - offset[0]) + self.y_coord[array_ID] + self.location[1] + offset[1]
			# And finally  calculate the displacement, if any is needed
			if target.rect[1] >= vector_y:
				dy = target.rect[1] - vector_y - 1
			
			if  abs(target.rect[1] - vector_y) < 10 and target.jumping == False:
				target.rect[1] = vector_y - 1
				return True

			# This can be applied to the target to move them above the map
			if dy != -1:
				target.rect[1] -= dy
				return True
			else:
				return False
		else:
			if target.type == "player":
				# Nudges the player back if they're trying to walk through a wall
				target.rect[0] -= target.x_direction * (target.speed + 1) 

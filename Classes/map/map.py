import pygame, sys, os
from pygame.locals import *

# Object classes
from Classes.objects.block import Block
from Classes.objects.quicksand import Quicksand
from Classes.objects.tree import Tree
from Classes.map.cloud import Cloud
from Classes.map.gust import Gust
from Classes.objects.bomb import Bomb
from Classes.objects.gate import Gate
from Classes.objects.button import Button
from Classes.objects.spawner import Spawner
from Classes.objects.water import Water
from Classes.objects.robot import Robot
from Classes.objects.barrier import Barrier

def load_image(name):
	full_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	image = pygame.image.load(full_path+ "\\" + name).convert_alpha()
	rect = image.get_rect()
	return(image)

# Stores and renders the map each time the frame is incrimented
class Map_Image(pygame.sprite.Sprite):
	#Initialization
	def __init__(self, map_code):
		pygame.sprite.Sprite.__init__(self)
		
		self.map_size = map_code[0]
		
		# Sprite holder for dynamic objects and colliding objects
		self.dynamic_objects = pygame.sprite.Group()
		self.collision_objects = pygame.sprite.Group()
		self.robots = pygame.sprite.Group()

		# Draw the static and active as two seperate images. Can overlay later
		self.foreground_dynamic = self.generate_dynamic(map_code[2])
		self.treeline = self.generate_trees()
		self.rect = self.foreground_dynamic.get_rect()
		self.water = [0,0]

	def generate_dynamic(self, map_code):
		# Same as before
		image = pygame.Surface((1000 * (self.map_size + 1), 2400), pygame.SRCALPHA, 32)
		# Have to hold the gates for the button code
		gates = pygame.sprite.Group()
		
		for item in map_code:
			# Block
			if item[0] == 0:
				obj = Block(item[1], item[2])
				#image.blit(obj.image, obj.rect)
				self.dynamic_objects.add(obj)
			# Quicksand
			elif item[0] == 1:
				obj = Quicksand(item[1], item[2])
				image.blit(obj.image, obj.rect)
				self.dynamic_objects.add(obj)
			# Gate
			elif item[0] == 2:
				obj = Gate(item[1], item[2])
				gates.add(obj)
				#image.blit(obj.image, obj.rect)
				self.dynamic_objects.add(obj)
			# Button	
			elif item[0] == 3:
				obj = Button(item[1], item[2], item[3], item[4], gates)
				image.blit(obj.image, obj.rect)
				self.dynamic_objects.add(obj)
			# Bomb
			elif item[0] == 4:
				obj = Bomb(item[1])
				image.blit(obj.image, obj.rect)
				self.dynamic_objects.add(obj)
			# Spawner
			elif item[0] == 5:
				obj = Spawner(item[1])
				self.dynamic_objects.add(obj)
			# Water
			elif item[0] == 6:
				obj = Water(item[1], item[2], item[3])
				image.blit(obj.image, obj.rect)
				self.dynamic_objects.add(obj)
				gates.add(obj)
			# Robot	
			elif item[0] == 7:
				obj = Robot(item[1])
				image.blit(obj.image, obj.rect)
				self.dynamic_objects.add(obj)
				self.robots.add(obj)
			# Barrier
			elif item[0] == 8:
				obj = Barrier(item[1], item[2])
				self.dynamic_objects.add(obj)
				
		self.collision_objects.add(self.dynamic_objects)		

		return(image)
		
	def generate_trees(self):
		image = pygame.Surface((500 * (self.map_size + 2), 768), pygame.SRCALPHA, 32)
		tree = load_image("Images/Maps/treeline.png")
		for i in range(0,self.map_size + 1):
			image.blit(tree, [i * 1000, 175 + 200])
		del tree	
		return(image)
				
	def update(self, players, map, map_location):
		#self.foreground_dynamic.fill(0)
		top_blit = [pygame.Surface((1,1)),[0,0,0,0]]
		for object in self.dynamic_objects:
			
			if object.type == "block":
				object.update(players, map, map_location, self.dynamic_objects, self.robots)
				if object.show_health == True:
					self.foreground_dynamic.blit(object.health_image, [object.rect[0], object.rect[1] - 100])
				if object.active == True:
					top_blit = [object.image, object.rect]
			elif object.type == "quicksand":
				object.update(players, self.collision_objects, map_location)
			elif object.type == "bomb":
				object.update(players, map[1], map_location, self.dynamic_objects)
			elif object.type == "gate":
				object.update(players, map_location)
			elif object.type == "button":
				object.update(players, self.dynamic_objects, map_location)
			elif object.type == "spawner":
				object.update(map_location, players, map[1])
				for item in object.blocks:
					if item.rect[0] < 1336 - map_location[0] and item.rect[0] > -1000 - map_location[0] and item.rect[1] > 500 - map_location[1] and item.rect[1] < 1500 - map_location[1]:
						self.foreground_dynamic.blit(item.image, item.rect)
			elif object.type == "water":
				object.update(players, map_location)
				self.water = [object.water, object.water_rect]
				plank = [object.plank, object.plank_rect]
				trans_blit = object.blit_rect
			elif object.type == "robot":
				object.update(map_location, map[0], players)
			elif object.type == "barrier":
				object.update(map_location, players)
				
			if abs(object.rect[0] + map_location[0]) < 1500 and abs(object.rect[1] + map_location[1]) > 900 - object.rect[3] and object.type != "spawner" or object.type == "button":
				self.foreground_dynamic.blit(object.image, object.rect)
		
		self.foreground_dynamic.fill(0, trans_blit)	
		self.foreground_dynamic.blit(top_blit[0], top_blit[1])
		self.foreground_dynamic.blit(plank[0], plank[1])
				
	def clear_screen(self, map_location):
		for object in self.dynamic_objects:
			if abs(object.rect[0] + map_location[0]) < 1500 and abs(object.rect[1] + map_location[1])  > 900 - object.rect[3]:
				if object.type == "spawner":
					for item in object.blocks:
						self.foreground_dynamic.fill(0, item.rect)
				elif object.type == "water":
					self.foreground_dynamic.fill(0, object.plank_rect)
					self.foreground_dynamic.fill(0, object.rect)
				elif object.type == "robot":
					wide_rect = [object.rect[0], object.rect[1], object.rect[2] + 30, object.rect[3]]
					self.foreground_dynamic.fill(0, wide_rect)
				elif object.type == "block":
					self.foreground_dynamic.fill(0, [object.rect[0], object.rect[1] - 100, 169, 45])
					self.foreground_dynamic.fill(0, object.rect)
				elif object.type != "barrier":
					self.foreground_dynamic.fill(0, object.rect)
			elif object.type == "water":
					self.foreground_dynamic.fill(0, object.plank_rect)
			elif object.type == "spawner":
					for item in object.blocks:
						self.foreground_dynamic.fill(0, item.rect)
			elif object.type == "gate":
				self.foreground_dynamic.fill(0, object.rect)	
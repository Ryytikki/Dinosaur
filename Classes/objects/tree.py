import pygame, sys, math, os
from pygame.locals import *

def load_image(name):
	full_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	image = pygame.image.load(full_path + "\\"+ name).convert_alpha()
	return(image)

class Tree(pygame.sprite.Sprite):
		
	def __init__(self, location, branches):
	
		pygame.sprite.Sprite.__init__(self)
		
		tree_surface = pygame.Surface((1100, 1000), pygame.SRCALPHA, 32)
		tree = load_image("Images\\trunk.png")
		branch = load_image("Images\\branch.png")
		platform = load_image("Images\\branch_bar.png")
		self.vine = load_image("Images\\hanging_vine.png")
		branch2 = pygame.transform.flip(branch, 1, 0)
		
		self.branch_rect = []
		platform_rect = platform.get_rect();
		
		for item in branches:
			if item > 0:
				tree_surface.blit(branch, (450, 975 - item))
				self.branch_rect.append([450, 1115 - item, 285, 17])
				#tree_surface.blit(platform, (450, 1115 - item))
			else:
				tree_surface.blit(branch2, (0, 975 + item))
				self.branch_rect.append([0, 1115 - item, platform_rect[2], platform_rect[3]])
				#.blit(platform, (165, 1115 + item))
				
		self.image = tree_surface
		self.image.blit(tree, (385,50))
		self.branches = branches
		self.rect = self.image.get_rect()
		self.rect.center = location
		
		self.type = "Tree"
	
	def test_landed(self, player, offset):
		i = 0
		for item in self.branches:
			test_rect = self.branch_rect[i]
			if item > 0:
				test_rect[0] = self.rect[0] + 450 + offset[0]
				test_rect[1] = self.rect[1] + 1115 - item + offset[1]
			else:
				test_rect[0] = self.rect[0] + 165 + offset[0]
				test_rect[1] = self.rect[1] + 1115 + item + offset[1]
			if player.hit_rect.colliderect(test_rect) and player.y_speed <= 0 and player.dropping == 10:
				if player.y_speed < 0:
					player.rect[1] = test_rect[1] - 150
					player.jumping = False
					player.animation_type = "land"
					player.y_speed = 0
					player.frame_ID = 0

				
				return(True) 
			
			

			i += 1
		return(False)
			
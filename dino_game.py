import pygame, sys, os, time, ctypes
from pygame.locals import *
from Classes.player import Player
from Classes.map.cloud import Cloud
from Classes.map.map import Map_Image
from Classes.vector_collisions import Collision_map
from Classes.play_music import Play_Music
from Classes.vlc import *

def load_image(name):
	full_path = os.path.dirname(os.path.realpath(sys.argv[0]))
	image = pygame.image.load(full_path+ "\\" + name).convert_alpha()
	return(image)
	
def convert(Image):    
    pygame.init()
    pygame.display.set_mode()
    image = Image
    for x in range(image.get_width()):
        for y in range(image.get_height()):
                image.set_at((x, y), (255, 255, 255, 0))
    return image
	
def main():
	pygame.init()
	pygame.mouse.set_visible(False)
	music = Play_Music("/menu.ogg", -1)
	music.play()
	music.set_volume(0.4)
	frame_ID = 0
	running = True
	window_surface = pygame.display.set_mode((1336,768),  pygame.FULLSCREEN)
	menu = [load_image("Menus//menu-art1.png"), load_image("Menus//menu-art2.png")]
	
	while running == True:
		window_surface.blit(menu[int(frame_ID / 80)], (0,0))
		pygame.display.flip()
		frame_ID += 1
		if frame_ID >= 160:
			frame_ID = 0
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_RETURN:
					running = False
				if event.key == K_F12:
					pygame.event.post(pygame.event.Event(QUIT))
					
			if event.type == QUIT: 
				pygame.quit()

				
					
					
	pygame.mixer.quit()
	cutscene(window_surface, "Cutscenes/Cutscene1.avi")		
	run_game(window_surface)
	cutscene(window_surface, "Cutscenes/Cutscene2.avi")
	tbc()
	main()
def callback(self, player):

	print
	print 'FPS =',  player.get_fps()
	print 'time =', player.get_time(), '(ms)'
	print 'FRAME =', .001 * player.get_time() * player.get_fps()
	
def cutscene(window_surface, movie):
	
	window_surface = pygame.display.set_mode((1336,768),  pygame.FULLSCREEN)
	
	window_surface.blit(load_image("Menus//loading.png"), (0,0))
	pygame.display.flip()
	
	pygame.display.get_wm_info()
	
	# Create instane of VLC and create reference to movie.
	vlcInstance = Instance("--no-video-title")
	media = vlcInstance.media_new(movie)

	# Create new instance of vlc player
	player = vlcInstance.media_player_new()

	# Add a callback
	em = player.event_manager()
	em.event_attach(EventType.MediaPlayerTimeChanged, \
		callback, player)

	# Pass pygame window id to vlc player, so it can render its contents there.
	win_id = pygame.display.get_wm_info()['window']
	if sys.platform == "linux2": # for Linux using the X Server
		player.set_xwindow(win_id)
	elif sys.platform == "win32": # for Windows
		player.set_hwnd(win_id)
	elif sys.platform == "darwin": # for MacOS
		player.set_agl(win_id)

	# Load movie into vlc player instance
	player.set_media(media)

	# Quit pygame mixer to allow vlc full access to audio device (REINIT AFTER MOVIE PLAYBACK IS FINISHED!)
	pygame.mixer.quit()

	# Start movie playback
	player.play()

	while player.get_state() != State.Ended:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(2)
			if event.type == pygame.KEYDOWN:
				print "OMG keydown!"
			if event.type == pygame.MOUSEBUTTONDOWN:
				print "we got a mouse button down!"
	
	player.release()

def run_game(window_surface):
	window_surface = pygame.display.set_mode((1336,768),  pygame.FULLSCREEN)
	music = Play_Music("/loading.ogg", -1)
	music.play()
	music.set_volume(0.2)	
	# Variables
	f = pygame.font.Font("arial.ttf", 16)
	black_colour = pygame.Color(0,0,0)

	foreground_X = 0.0
	foreground_Y = 0.0
	prev_y = 0.0
	sliding = False
	
	map_size = 5.55 # 0 = 1000px, etc
	map_file = [[0,500], [1500, 500], [2200, 350], [2600, 325], [4100, 325], [4700, 300], [5200, 350], [5800, 710], [6500, 760], [8000, 750], [10000, 750]]
	map_file_2 = [[0,1550], [1100, 1550], [2350, 1500], [2800, 1500], [3050, 1600], [3150, 1650], [4000, 1650], [4100, 1450], [5315, 1450], [6310, 900], [7000, 750], [10000, 750]]
	map_code = [6, [], [[8, [4100, 2010, 150, 300], [-1, 0]], [8, [200, 1075, 1000, 100], [0, 1]], [8, [100, 1000, 100, 1010], [-1,0]], [0, [1100, 1200], 0], [0, [1400, 1200], 0], [0, [1700, 1200], 0], [7, [1000, 800]], [7, [1200, 800]], [7, [1400, 800]], [2, [850, 930], 0], [2, [4600, 1800], 2], [2, [4900, 1800], 3], [5, [1850,1550]],[6, [3700,2050], 1, 1], [3, [2800, 750],2, 1, 10], [3, [920, 2000], 0, 0, 10], [2, [6900, 1050], 4], [3, [4000, 880], 1, 2, 10], [3, [4250, 880], 1, 3, 5], [3, [4500, 880], 1, 3, 5], [4, [700, 5000]]]]
	entity_file = []
	collision_map = Collision_map(map_file, entity_file, 1000)
	collision_map_2 = Collision_map(map_file_2, entity_file, 1000)
	hit_maps = [collision_map, collision_map_2]
	
	fpsclock = pygame.time.Clock()
	pygame.display.set_caption("Rawr")
	
	window_surface.blit(load_image("Menus//loading.png"), (0,0))
	pygame.display.flip()

	bg_image = load_image("Images/Maps/background.png")
	bg_image = pygame.transform.scale(bg_image, (1336,768))
	cave = load_image("Images/Maps/cave.png")
	cave_ground = load_image("Images/Maps/cave-ground.png")
	fence = load_image("Images/Maps/mining-layer.png")
	rocks = load_image("Images/Maps/rock-mound.png")
	grass = load_image("Images/Maps/grass.png")
	hut = load_image("Images/Maps/hut.png")
	tunnel = load_image("Images/Maps/tunnel.png")
	other_rocks = load_image("Images//Maps//boulder-pile-lift.png")
	tnt_box = load_image("Images//Maps//TNT-box.png")
	hanging_light = load_image("Images//hanging-lights1.png")
	spawner = load_image("Images//spawner.png")
	tile = []
	for i in range(1,5):
		tile.append(load_image("Images/Maps/ground/" + str(i) + ".png"))
	map = Map_Image(map_code)
	
	# Current player	
	player_ID = 1 
		
	# Set up sprites and objects
	plr = Player(1)	
	plr2 = Player(2)
	
	players = pygame.sprite.Group()
	players.add((plr, plr2))
	clouds = pygame.sprite.Group()
	for a in range(1,5):
		for i in range(1, 3):
				clouds.add((Cloud(i))) 
	
	current_player = plr 
	running = True
	music.stop()
	music2 = Play_Music("/test.ogg", -1)
	music2.play()
	music2.set_volume(0.2)

	while running == True:
		rect_change = 0
		for player in players:
			if player.dead == 1:
				current_player.player_ID = player.ID
			elif player.dead == 2:
				print foreground_X
				print player.rect[1]
				plr2.rect[0] += foreground_X
				print foreground_X
				player.dead = 0
				print plr.rect
				
		# If the player swapped characters
		if current_player.player_ID is not player_ID:
			old_y = foreground_Y
			# Assign new player ID
			player_ID = current_player.player_ID
			health = current_player.health
			# Reset the movement
			current_player.x_direction = 0
			# Sets the new controllable sprite
			if current_player.player_ID == 1:
				current_player = plr
			elif current_player.player_ID == 2:
				current_player = plr2
			# Tells the current player what ID is selected
			current_player.player_ID = player_ID
			# Slides
			sliding = True
			
			#button correction
			for item in map.dynamic_objects:
				if item.type == "button" and item.button_type != 0:
					item.activation_delay = 11
					item.float = True
		
		# If the player is further than the right cutoff but not at the end of the map
		if current_player.rect[0] > 500.0 and foreground_X > -1000.0 * map_size:
			# Cloud movement correction
			for cloud in clouds:
				cloud.rect[0] -= current_player.speed * 0.25
			# Move the foreground and all objects
			foreground_X -= (current_player.rect[0] - 500)
			# Move the players
			for dino in players:
				if dino is not current_player:
					dino.rect[0] -= (current_player.rect[0] - 500)
			# Stop the player from moving farther than 600 till you reach the end of the map
			current_player.rect[0] = 500.0
			
			# keeps the foreground in place
			if foreground_X <= -1000 * map_size:
				# Corrector for all the objects on the screen when sliding
				if sliding == True:
					for dino in players:
						dino.rect[0] -= foreground_X + 1000 * map_size
					
				# Holds the foreground in place
				foreground_X = -1000 * map_size
		
		# Same for the left hand side
		if (current_player.rect[0] < 500.0) and (foreground_X < 0):
			for cloud in clouds:
				cloud.rect[0] += current_player.speed * 0.25
				
			foreground_X += (500 - current_player.rect[0])
			for dino in players:
				if dino is not current_player:
					dino.rect[0] += (500 - current_player.rect[0])	
			current_player.rect[0] = 500
			
			if foreground_X >= 0:
				if sliding == True:
					for dino in players:
						dino.rect[0] -= foreground_X
					
				foreground_X = 0
		
		# stop player moving past boundaries
		if current_player.rect[0] >= 0:
			current_player.rect[0] += current_player.speed * current_player.x_direction
		
		if current_player.rect[0] < 0:
			current_player.rect[0] = 0
			
		# Y stuff	
		if current_player.rect[1] < 500:
			if sliding == False:
				# Move the foreground and all objects
				foreground_Y -= current_player.rect[1] - 500
				for player in players:#
					if player != current_player:
						player.rect[1] -= current_player.rect[1] - 500
						rect_change = current_player.rect[1] - 500
				# Stop the player from moving farther than 600 till you reach the end of the map
				
				current_player.rect[1] = 500
				
			else:
				foreground_Y = 500 + current_player.rect[1]
				for player in players:
					player.rect[1] -= old_y - foreground_Y
				sliding == False
					
		# and down
		if current_player.rect[1] >= 500 and foreground_Y > -1050:
			
			if sliding == False:
				# Move the foreground and all objects
				foreground_Y -= current_player.rect[1] - 500
				for player in players:
					if player != current_player:
						player.rect[1] -= current_player.rect[1] - 500
						
				# Stop the player from moving farther than 600 till you reach the end of the map
						
				current_player.rect[1] = 500
			
			
			else:
				if current_player.rect[1] >= 500:
					
					for player in players:
						player.rect[1] -= foreground_Y
					foreground_Y = 0
		
		if foreground_Y < -1050:
			for dino in players:
				dino.rect[1] -= foreground_Y + 1050
			foreground_Y = -1050
					
					
		if foreground_Y != prev_y and current_player.jumping == False:
			for item in map.dynamic_objects:
				if item.type == "button" and item.button_type != 0:
					item.float = True
					
		prev_y = foreground_Y
			
		# Update everything and refresh the screen
		sliding = False
		map_location = [foreground_X, 432 + foreground_Y, rect_change]
		map.update(players, hit_maps, map_location)
	
		players.update(player_ID, map.collision_objects, players, hit_maps, [foreground_X, foreground_Y])

		window_surface.blit(bg_image, (0,0))
		window_surface.blit(map.treeline, [foreground_X * 0.5,-150 + foreground_Y * 0.5])
		window_surface.blit(fence, [foreground_X * 0.8, 250 + foreground_Y * 0.8])
		window_surface.blit(rocks, (1030 + foreground_X,210 + foreground_Y))
		for i in range(0,4):
			window_surface.blit(tile[i], ((i * 1750) + foreground_X, foreground_Y + 375))
		window_surface.blit(map.water[0], [map.water[1][0] + foreground_X, map.water[1][1] + foreground_Y])
		window_surface.blit(cave_ground, [foreground_X, 900 + foreground_Y])
		window_surface.blit(tnt_box, [foreground_X + 350, foreground_Y + 1500])
		#for cloud in clouds:	
			#if current_player.rect[0] > ((foreground_X  + 1000) * 0.25) - 3000 and  current_player.rect[0] < ((foreground_X  + 1000) * 0.95) + 3000 : 
				#window_surface.blit(cloud.image, (cloud.rect[0] + foreground_X * 0.25 , 125 + foreground_Y * 0.))
			#cloud.update(foreground_X, map_size)
		window_surface.blit(map.foreground_dynamic,[0,0], (-1 * foreground_X, 432 - foreground_Y, 1336, 768))
		for player in players:
			if player.ID != player_ID:
				if player.ID == 1:
					window_surface.blit(player.image, player.rect)
				elif (player.ID == 2 and player.rect[0] > 20):
					window_surface.blit(player.image, player.rect)
	
		window_surface.blit(spawner, [1350 + foreground_X,1018 + foreground_Y])
		if current_player.ID == 1:
			window_surface.blit(current_player.image, current_player.rect)
		elif (current_player.ID == 2 and current_player.rect[0] > 20):
			window_surface.blit(current_player.image, current_player.rect)

		window_surface.blit(other_rocks, [600 + foreground_X, 600 + foreground_Y])
		window_surface.blit(hut, [foreground_X,foreground_Y + 150])
		window_surface.blit(other_rocks, [-200 + foreground_X, 600 + foreground_Y])
		window_surface.blit(tunnel, [foreground_X - 50, foreground_Y + 1060])
		window_surface.blit(hanging_light, [foreground_X + 550, foreground_Y + 1000])

		window_surface.blit(grass, [20 + foreground_X, 440+ foreground_Y])		
		window_surface.blit(cave, [-200 + foreground_X * 1.25,894 + foreground_Y])

		timer = fpsclock.get_fps()
		x = foreground_Y
		#text_surface2 = f.render(str(timer) + " " + str(x), 1, (255,0,0))
		#window_surface.blit(text_surface2,(0,0))

		#tracer = hit_maps[1].draw_map()
		#window_surface.blit(tracer, (foreground_X,foreground_Y))

		pygame.display.update()
		map.clear_screen(map_location)
		fpsclock.tick(30)
		
		if current_player.reset == True:
			pygame.mixer.quit()
			main()
		if current_player.rect[0] > 1336:
			pygame.mixer.quit()
			running = False
		 
	
	
def tbc():
	frame_ID = 0
	counter = 0
	running = True
	window_surface = pygame.display.set_mode((1336,768),  pygame.FULLSCREEN)
	menu = [load_image("Menus//continue-1.png"), load_image("Menus//continue-2.png")]
	
	while running == True:
		window_surface.blit(menu[int(frame_ID / 80)], (0,0))
		pygame.display.flip()
		frame_ID += 1
		counter += 1
		if frame_ID >= 160:
			frame_ID = 0
			
		if counter > 900:
			running = False
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				if event.key == K_RETURN:
					running = False
				if event.key == K_F12:
					pygame.event.post(pygame.event.Event(QUIT))
					
			if event.type == QUIT: 
				pygame.quit()

if __name__ == '__main__':
	main()
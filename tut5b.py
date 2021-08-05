import random
import pygame
import winsound
from time import sleep


frequency = 2500  # Set Frequency To 2500 Hertz
duration = 100  # Set Duration To 1000 ms == 1 second

tile_size = 84

class Generator:
	def __init__(self):
		self.lyt = [
			[0,0,0,0,0,0,0,0,],
			[0,0,0,0,0,0,0,0,],
			[0,0,0,0,0,0,0,0,],
			[0,0,0,0,0,0,0,0,],
			[0,0,0,0,0,0,0,0,],
			[0,0,0,0,0,0,0,0,],
			[0,0,0,0,0,0,0,0,],
			[0,0,0,0,0,0,0,0,]
		]

		ncells = len(self.lyt)*len(self.lyt[0])
		print(f"{ncells=}")
		clrs = []
		self.populate_color()
		# print(self.lyt)
		# print(self.lyt_surfaces)

	def clr(self):
		return random.randrange(50, 255, 10)
	
	def populate_color(self):
		''' creates 32 random color + 32 like the first 32 '''
		for r, line in enumerate(self.lyt):
			for c, x in enumerate(line):
				color = [self.clr(), self.clr(), self.clr()]
				self.lyt[r][c] = color
				# surf = pygame.Surface((tile_size,tile_size))
				# surf.fill(color)
				# self.lyt_surfaces.append(surf)
		self.lyt[:4] = self.lyt[4:9]
		self.shuffle_colors()
		self.set_surfaces()

	def shuffle_colors(self):
		for n, line in enumerate(self.lyt):
			self.lyt[n] = random.sample(line, len(line))
		random.shuffle(self.lyt)
		print(*self.lyt, sep="\n")

	def set_surfaces(self):
		self.lyt_surfaces = [] # contains surfaces
		self.drk_surfaces = [] # contains surfaces
		for r, line in enumerate(self.lyt):
			row_clr = []
			row_drk = []
			for c, color in enumerate(line):
				surf = pygame.Surface((tile_size,tile_size))
				surf.fill(color)
				row_clr.append(surf)
				drk = pygame.Surface((tile_size, tile_size))
				drk.fill((0,0,0))
				row_drk.append(drk)
			self.lyt_surfaces.append(row_clr)
			self.drk_surfaces.append(row_drk)
		# print(self.lyt_surfaces)
		


first_try = 0
couple = 0
class Win:
	def __init__(self):
		pygame.init()
		couples = 32
		cols, rows = (8,8)
		# tile_size = tile_size
		size = cols*tile_size, rows*tile_size 
		self.screen = pygame.display.set_mode(size)
		self.clock = pygame.time.Clock()
		self.particles = []
		self.game_loop()

	def draw_screen(self):
		# self.screen.blit(bg, (0, 0))
		self.screen.fill(0)
		self.particles_run(random.randint(0, 500), (255, 255, 255))
		for nrow, row in enumerate(grid.drk_surfaces):
			for ncol, col in enumerate(row):
				self.screen.blit(col, (ncol*tile_size, nrow*tile_size))
		for x in range(8):
			pygame.draw.line(self.screen, (255, 255, 255), (tile_size*x, 0), (tile_size*x, 8 * tile_size))
			pygame.draw.line(self.screen, (255, 255, 255), (0, tile_size * x), (8 * tile_size, tile_size * x))
		pygame.draw.line(self.screen, (255, 255, 255), (tile_size * 8 - 1, 0), (tile_size * 8- 1, 8 * tile_size))
		pygame.draw.line(self.screen, (255, 255, 255), (0, tile_size * 8 - 1), (8 * tile_size, tile_size * 8 - 1))

	def particles_run(self, pos, color):
	    """ Creates particles starting from pos with a color """
	    self.particles.append([
	        [pos, 0],
	        [random.randint(0, 20) / 10 - 1, 2],
	        random.randint(4,6)])
	    # Moving the coordinates and size of self.particles
	    for particle in self.particles[:]:
	        particle[0][0] += particle[1][0]
	        particle[0][1] += particle[1][1]
	        particle[2] -= 0.005 # how fast circles shrinks
	        particle[1][1] += 0.01 # circles speed
	        # if particle[2] <= 0:
	        if particle[0][1] > 512:
	            self.particles.remove(particle)
	    # Draw circles
	    for particle in self.particles:
	        pygame.draw.circle(
	            self.screen, (color),
	        (round(particle[0][0]), round(particle[0][1])),
	         round(particle[2]))
	def delete(self, r1, c1, r2, c2):
		srf_black = pygame.Surface((tile_size, tile_size))
		srf_black.fill((0,0,0))
		grid.drk_surfaces[r1][c1] = srf_black
		srf_black = pygame.Surface((tile_size, tile_size))
		srf_black.fill((0,0,0))
		grid.drk_surfaces[r2][c2] = srf_black
	def game_loop(self):
		global first_try

		loop = 1
		count_taken = 0
		score = 0
		while loop:
			if score == 32:
				print("YOU WIN!")
				winsound.Beep(150, 200)
				winsound.Beep(1500, 200)
				winsound.Beep(150, 200)
				winsound.Beep(1500, 200)
				winsound.Beep(1500, 200)
				winsound.Beep(1500, 200)
				loop = 0
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					loop = 0
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = pygame.mouse.get_pos()
					col, row = x//tile_size,  y//tile_size

					if grid.lyt[row][col] != [0,0,0]:
						print(grid.lyt[row][col])
						count_taken += 1
						print(f"{count_taken=}")
						# ===================================== [ 1 ] === #
						if count_taken == 1 :
							try:
								if couple == 0:
									self.delete(r1, c1, r2, c2)
							except:
								pass
							winsound.Beep(200, 100)
							first = grid.lyt[row][col]
							r1, c1 = row, col
							surf1 = grid.lyt_surfaces[r1][c1].copy()
							grid.drk_surfaces[r1][c1] = surf1
						# ===================================== [ 2 ] === #
						if count_taken == 2:
							winsound.Beep(200, 100)
							second = grid.lyt[row][col]
							r2, c2 = row, col
							surf2 = grid.lyt_surfaces[r2][c2].copy()
							grid.drk_surfaces[r2][c2] = surf2

							if (r2, c2) != (r1, c1):
								print(r2, c2, "-", r1, c1)
								if first == second:
									print("Hai trovato una coppia")
									score += 1
									winsound.Beep(1500, 100)
									count_taken = 0
									grid.lyt[r1][c1] = [0,0,0]
									grid.lyt[r2][c2] = [0,0,0]
									couple = 1
								else:
									print("Sono diversi")
									count_taken = 0
									grid.lyt_surfaces[r1][c1] = surf1.copy()
									grid.lyt_surfaces[r2][c2] = surf2.copy()
									couple = 0

									
							else:
								print("Devi cliccare su un'altra casella")
								# pygame.mixer.Sound.play(self.snd_whip)
								winsound.Beep(200, 400)
								grid.lyt_surfaces[r1][c1] = surf1.copy()
								count_taken = 0


					print(row, col)
			self.draw_screen()
			
			self.clock.tick(60)
			pygame.display.flip()
		pygame.quit()




grid = Generator()
# print(grid.lyt_surfaces)
Win()
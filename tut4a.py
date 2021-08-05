import random
import pygame
import winsound

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 100  # Set Duration To 1000 ms == 1 second

tile_size = 64

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
		return random.randrange(0, 255, 10)
	
	def populate_color(self):
		''' creates 32 random color + 32 like the first 32 '''
		for r, line in enumerate(self.lyt):
			for c, x in enumerate(line):
				color = [self.clr(), self.clr(), self.clr()]
				self.lyt[r][c] = color
				# surf = pygame.Surface((64,64))
				# surf.fill(color)
				# self.lyt_surfaces.append(surf)
		self.lyt_surfaces = [] # contains surfaces
		self.lyt[:4] = self.lyt[4:9]
		self.shuffle_colors()
		self.set_surfaces()

	def shuffle_colors(self):
		for n, line in enumerate(self.lyt):
			self.lyt[n] = random.sample(line, len(line))
		random.shuffle(self.lyt)
		print(*self.lyt, sep="\n")

	def set_surfaces(self):
		for r, line in enumerate(self.lyt):
			row_clr = []
			for c, color in enumerate(line):
				surf = pygame.Surface((64,64))
				surf.fill(color)
				row_clr.append(surf)
			self.lyt_surfaces.append(row_clr)
		# print(self.lyt_surfaces)
		




class Win:
	def __init__(self):
		pygame.init()

		# self.snd_win = pygame.mixer.Sound("sounds\\win.wav")
		# self.snd_click = pygame.mixer.Sound("sounds\\click.ogg")
		# self.snd_whip = pygame.mixer.Sound("sounds\\whip.ogg")
		card_num = 64
		couples = 32
		cols, rows = (8,8)
		tile_size = 64
		size = cols*tile_size, rows*tile_size 
		self.screen = pygame.display.set_mode(size)
		self.clock = pygame.time.Clock()
		self.particles = []
		self.game_loop()

	def draw_screen(self):
		# self.screen.blit(bg, (0, 0))
		self.screen.fill(0)
		self.particles_run(random.randint(0, 500), (255, 255, 255))
		for nrow, row in enumerate(grid.lyt_surfaces):
			for ncol, col in enumerate(row):
				self.screen.blit(col, (ncol*64, nrow*64))

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
	
	def game_loop(self):
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
					# pygame.mixer.Sound.play(self.snd_win)
					# pygame.mixer.Sound.play(self.snd_win)
					# pygame.mixer.Sound.play(self.snd_win)
					loop = 0
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						loop = 0
					if event.type == pygame.MOUSEBUTTONDOWN:
						x, y = pygame.mouse.get_pos()
						col, row = x//tile_size,  y//tile_size

						if grid.lyt[row][col] != [0,0,0]:
							# pygame.mixer.Sound.play(self.snd_click)
							print(grid.lyt[row][col])
							count_taken += 1
							print(f"{count_taken=}")
							if count_taken == 1 :
								winsound.Beep(200, 100)
								first = grid.lyt[row][col]
								r1, c1 = row, col
								surf1 = grid.lyt_surfaces[r1][c1].copy()
								pygame.draw.rect(grid.lyt_surfaces[r1][c1], (255,255,255), (1,1,tile_size - 2,tile_size - 2), 3)

							elif count_taken == 2:
								second = grid.lyt[row][col]
								r2, c2 = row, col
								# surf2 = grid.lyt_surfaces[r2][c2].copy()
								# pygame.draw.rect(grid.lyt_surfaces[r2][c2], (255,255,255), (1,1,62,62), 3)
								# winsound.Beep(200, 400)
								if (r2, c2) != (r1, c1):
									print(r2, c2, "-", r1, c1)
									if first == second:
										print("Hai trovato una coppia")
										score += 1
										# pygame.mixer.Sound.play(self.snd_win)
										winsound.Beep(1500, 100)
										count_taken = 0
										grid.lyt_surfaces[r1][c1].fill((0,0,0,0))
										grid.lyt_surfaces[r1][c1].set_colorkey((0,0,0))
										grid.lyt[r1][c1] = [0,0,0]
										grid.lyt_surfaces[r2][c2].fill((0,0,0,0))
										grid.lyt_surfaces[r2][c2].set_colorkey((0,0,0))
										grid.lyt[r2][c2] = [0,0,0]
										# grid.set_surfaces()
									else:
										print("Sono diversi")
										count_taken = 0
										# pygame.mixer.Sound.play(self.snd_whip)
										# winsound.Beep(400, 100)
										winsound.Beep(150, 400)
										grid.lyt_surfaces[r1][c1] = surf1.copy()
										# grid.lyt_surfaces[r2][c2] = surf2.copy()
										# winsound.PlaySound("err.wav", winsound.SND_ALIAS | winsound.SND_ASYNC)
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
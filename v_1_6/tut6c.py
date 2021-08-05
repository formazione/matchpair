import random
import pygame
from glob import glob

# tut5e: colors chosen not random
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(32)
music = [x for x in glob("sounds\\*.mp3")]
# "sounds\\gentleman.mp3",
# "sounds\\digitalghost.mp3",
# "sounds\\electric.mp3",
# ]
num_music = 1
pygame.mixer.music.load(random.choice(music))
pygame.mixer.music.play()
snd_click = pygame.mixer.Sound("sounds\\click.ogg")
snd_whip = pygame.mixer.Sound("sounds\\whip.ogg")
snd_win = pygame.mixer.Sound("sounds\\yeah.wav")
play = pygame.mixer.Sound.play
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 100  # Set Duration To 1000 ms == 1 second

tile_size = 100
time_level = 2000

colors = '''66, 102, 245
245, 221, 66
245, 138, 66
245, 66, 66
66, 245, 170
245, 66, 167
75, 66, 245
81, 131, 255'''.split("\n")


clr = {
"66, 102, 245":0,
"245, 221, 66":1,
"245, 138, 66":2,
"245, 66, 66":3,
"66, 245, 170":4,
"245, 66, 167":5,
"75, 66, 245":6,
"81, 131, 255":7,
}

print(colors)
for n, i in enumerate(colors):
	colors[n] = [int(x) for x in i.split(",")]
print(colors)
colors = colors + colors + colors + colors + colors + colors + colors + colors
print(colors)
tiles = pygame.image.load("images\\diamonds3.png")
class Generator:
	def __init__(self):

		self.lyt = self.list_zero(8)
		self.lyt_surfaces = self.list_zero(8)
		self.drk_surfaces = self.list_zero(8)

		ncells = len(self.lyt)*len(self.lyt[0])
		print(f"{ncells=}")
		clrs = []
		self.populate_color()
		# print(self.lyt)
		# print(self.lyt_surfaces)

	def list_zero(self, num_item):
		return [[[0] for x in range(num_item)] for x in range(num_item)]

	def clr(self):
		return random.randrange(50, 255, 10)
	
	def populate_color(self):
		''' put the colors into lyt '''
		
		ccnt = 0
		random.shuffle(colors)


		for rw, row in enumerate(self.lyt):
			for cl, col in enumerate(self.lyt):
				self.lyt[rw][cl] = colors[ccnt]
				self.lyt_surfaces[rw][cl] = pygame.Surface((tile_size, tile_size))
				self.lyt_surfaces[rw][cl].fill(colors[ccnt])
				if random.random() > 0:
					# print images
					xstr =[str(x) for x in colors[ccnt]]
					key = ", ".join(xstr)
					self.lyt_surfaces[rw][cl].blit(tiles, (25,25), (0, clr[key]*57, 57, 57))
				self.drk_surfaces[rw][cl] = pygame.Surface((tile_size, tile_size))
				self.drk_surfaces[rw][cl].fill((0,0,0))
				print(ccnt)
				ccnt += 1

first_try = 0
attempt = 0 # number of try
won = 0 # number of matches
score = 0
couple = 0
start = pygame.time.get_ticks()
font = pygame.font.SysFont("Arial", 14)

def message(text) -> pygame.Surface:
	t = font.render(text, 1, (255, 255, 255))
	return t

class Win:
	def __init__(self):
		couples = 32
		cols, rows = (8,8)
		# tile_size = tile_size
		size = cols*tile_size, rows*tile_size 
		self.screen = pygame.display.set_mode(size)
		pygame.display.set_caption("MatchPair 1.6")
		self.clock = pygame.time.Clock()
		self.particles = []
		self.game_loop()


	def draw_screen(self):
		# self.screen.blit(bg, (0, 0))
		self.screen.fill(0)
		for nrow, row in enumerate(grid.drk_surfaces):
			for ncol, col in enumerate(row):
				self.screen.blit(col, (ncol*tile_size, nrow*tile_size))
		# self.particles_run(random.randint(0, 8*tile_size), (255, 255, 255))
		self.draw_lines()
		self.screen.blit(message(f"SCORE {score} - TIME {pygame.time.get_ticks()//720}"), (0,0))

	def draw_lines(self):
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
	        random.randint(2,4)])
	    # Moving the coordinates and size of self.particles
	    for particle in self.particles[:]:
	        particle[0][0] += particle[1][0]
	        particle[0][1] += particle[1][1]
	        particle[2] -= 0.005 # how fast circles shrinks
	        particle[1][1] += 0.01 # circles speed
	        # if particle[2] <= 0:
	        if particle[0][1] > 8*tile_size or particle[0][0] > 8*tile_size:
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
	
	def pick(self):
		if pygame.time.get_ticks() - start < time_level:
			for nrow, row in enumerate(grid.lyt_surfaces):
				for ncol, col in enumerate(row):
					self.screen.blit(col, (ncol*tile_size, nrow*tile_size))
			self.particles_run(random.randint(0, 8*tile_size), (255, 255, 255))
			self.draw_lines()
		self.screen.blit(message(f"SCORE {score} - TIME {pygame.time.get_ticks()//720}"), (0,0))

	def game_loop(self):
		global first_try, start, attempt, score, music

		loop = 1
		count_taken = 0
		score = 0
		music_on = 0
		try_start = 0
		while loop:
			if music_on:
					pygame.mixer.music.play()
					music_on = 0
			if pygame.time.get_ticks()//720 % (100 + try_start) == 0 and pygame.time.get_ticks()//720 > 10:
				pygame.mixer.music.stop()
				if pygame.mixer.get_busy() == False:
					pygame.mixer.music.load(random.choice(music))
					music_on = 1
					try_start = 0
				else:
					try_start += 2
					print(try_start)

			if score == 320:
				print("YOU WIN!")
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
							play(snd_click)
							# winsound.Beep(200, 100)
							first = grid.lyt[row][col]
							r1, c1 = row, col
							surf1 = grid.lyt_surfaces[r1][c1].copy()
							grid.drk_surfaces[r1][c1] = surf1
							pygame.draw.rect(grid.lyt_surfaces[r1][c1], (255, 255, 255), (0,0,tile_size ,tile_size ), 6)
							
						# ===================================== [ 2 ] === #
						if count_taken == 2:
							# winsound.Beep(200, 100)
							second = grid.lyt[row][col]
							r2, c2 = row, col
							surf2 = grid.lyt_surfaces[r2][c2].copy()
							grid.drk_surfaces[r2][c2] = surf2

							if (r2, c2) != (r1, c1):
								print(r2, c2, "-", r1, c1)
								if first == second:
									print("Hai trovato una coppia")
									score += 10
									play(snd_win)
									# winsound.Beep(1500, 100)
									count_taken = 0
									# grid.drk_surfaces[r1][c1].set_alpha(128)
									# grid.drk_surfaces[r2][c2].set_alpha(128)
									grid.drk_surfaces[r1][c1].fill((50,50,50))
									grid.drk_surfaces[r2][c2].fill((50,50,50))
									grid.lyt_surfaces[r1][c1].fill(0)
									grid.lyt_surfaces[r2][c2].fill(0)
									# grid.drk_surfaces[r1][c1].fill((grid.lyt[r1][c1]))
									# grid.drk_surfaces[r1][c1].fill((grid.lyt[r1][c1]))
									# grid.lyt_surfaces[r1][c1].fill((grid.lyt[r1][c1]))
									# grid.lyt_surfaces[r2][c2].fill((grid.lyt[r2][c2]))

									grid.lyt[r1][c1] = [0,0,0]
									grid.lyt[r2][c2] = [0,0,0]
									grid.drk_surfaces[r1][c1].set_alpha(128)
									grid.drk_surfaces[r2][c2].set_alpha(128)
									# grid.lyt_surfaces[r1][c1].set_alpha(128)
									# grid.lyt_surfaces[r2][c2].set_alpha(64)
									# pygame.draw.rect(grid.lyt_surfaces[r1][c1], (250,250,250), (0,0,tile_size ,tile_size ), 40)
									# pygame.draw.rect(grid.lyt_surfaces[r2][c2], (250,250,250), (0,0,tile_size ,tile_size ), 40)
									pygame.draw.rect(grid.drk_surfaces[r1][c1], (250,250,250), (0,0,tile_size ,tile_size ), 40)
									pygame.draw.rect(grid.drk_surfaces[r2][c2], (250,250,250), (0,0,tile_size ,tile_size ), 40)
									couple = 1
									start = pygame.time.get_ticks()
									self.pick()
								else:
									print("Sono diversi")
									play(snd_whip)
									count_taken = 0
									grid.lyt_surfaces[r1][c1] = surf1.copy()
									grid.lyt_surfaces[r2][c2] = surf2.copy()
									couple = 0
									attempt += 1
									grid.drk_surfaces[r1][c1] = surf1
									if score > 0:
										score -= 1							
							else:
								print("Devi cliccare su un'altra casella")
								play(snd_whip)
								grid.lyt_surfaces[r1][c1] = surf1.copy()
								count_taken = 0

					print(row, col)
			self.draw_screen()
			self.pick()
				
			self.clock.tick(30)
			pygame.display.flip()
		pygame.quit()

grid = Generator()
# print(grid.lyt_surfaces)
Win()
import random
import pygame
from glob import glob
import locale
import math
from datetime import datetime
locale.setlocale(locale.LC_ALL, '')
daytime = datetime.today().strftime("%d.%m.%y %H:%M")
print(daytime)
# tut5e: colors chosen not random
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(32)
music = [x for x in glob("sounds\\*.mp3")]

num_music = 1
pygame.mixer.music.load(random.choice(music))
pygame.mixer.music.play()
snd_click = pygame.mixer.Sound("sounds\\click.ogg")
snd_whip = pygame.mixer.Sound("sounds\\whip.ogg")
snd_win = pygame.mixer.Sound("sounds\\yeah.wav")
play = pygame.mixer.Sound.play
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 100  # Set Duration To 1000 ms == 1 second
info = pygame.display.Info()
w, h = info.current_w, info.current_h
tile_size = 100
time_level = 2000

# https://htmlcolorcodes.com/color-picker/

levels = [{
"66, 102, 245":(0,0),
"245, 221, 66":(1,0),
"245, 138, 66":(2,0),
"245, 66, 66":(3,0),
"66, 245, 170":(4,0),
"245, 66, 167":(5,0),
"75, 66, 245":(6,0),
"81, 131, 255":(7,0),
},
{
"66, 102, 245":(0,0),
"245, 80, 66":(1,0),
"200, 138, 66":(2,0),
"160, 66, 66":(3,0),
"66, 215, 170":(4,0),
"245, 66, 167":(5,0),
"75, 66, 20":(6,0),
"81, 20, 255":(7,0),
"78, 191, 200":(0,1),
"50, 127, 255":(1,1),
"0, 50, 114":(2,1),
"26, 201, 0":(3,1),
"190, 100, 26":(4,1),
"150, 150, 150":(5,1),
"78, 191, 80":(6,1),
"14, 200, 58":(7,1)},
{
"66, 102, 245":(0,0),
"245, 221, 66":(1,0),
"245, 138, 66":(2,0),
"245, 66, 66":(3,0),
"66, 245, 170":(4,0),
"245, 66, 167":(5,0),
"75, 66, 245":(6,0),
"81, 131, 255":(7,0),
"78, 191, 200":(0,1),
"14, 127, 255":(1,1),
"14, 127, 114":(2,1),
"26, 201, 0":(3,1),
"190, 100, 26":(4,1),
"201, 124, 26":(5,1),
"78, 191, 80":(6,1),
"14, 200, 58":(7,1),
"232, 80, 204":(0,2),
"78, 191, 20":(1,2),
"14, 50, 58":(2,2),
"14, 127, 200":(3,2),
"26, 201, 200":(4,2),
"190, 201, 26":(5,2),
"232, 43, 204":(6,2),
"78, 191, 0":(7,2),
"14, 85, 58":(0,3),
"14, 127, 100":(1,3),
"26, 201, 116":(2,3),
"190, 100, 100":(3,3),
"232, 108, 204":(4,3),
"78, 191, 122":(5,3),
"14, 127, 58":(6,3),
"14, 100, 50":(7,3)
}]
def show(x):
    print(f"[show]: {x=}")

def difficulty(diff_level):
    colors = []
    # choose clr_easy for easy level
    # clr for hard level
    clr = levels[diff_level]
    for k in levels[diff_level]:
        colors.append([int(x) for x in k.split(",")])
        print([int(x) for x in k.split(",")])

    # if levels[0] * 8       easy
    # if levels[1] * 4       medium
    # if levels[2] * 2       hard
    if diff_level == 2:
        colors = colors * 2 #
    elif diff_level == 1:
        colors = colors * 4
    elif diff_level == 0:
        colors = colors *4
    return colors, clr

colors, clr = difficulty(diff_level=1)

show(len(colors))

tiles = pygame.image.load(random.choice(glob("images\\*.png")))
class Generator:
    def __init__(self):

        self.lyt = []
        self.lyt_surfaces = []
        self.drk_surfaces = []
        self.populate_color()

    def list_zero(self, num_item):
        return [[[0] for x in range(num_item)] for x in range(num_item)]

    def clr(self):
        return random.randrange(50, 255, 10)
    
    def populate_color(self):
        ''' put the colors into lyt '''

        ccnt = 0 # there are 16 colors
        random.shuffle(colors) # now they are mixed
        ccol = 0
        column2 = 0 # change the tiles column to get the image from
        for rw in range(8): # for 8 row
            self.lyt.append([])
            self.lyt_surfaces.append([])
            self.drk_surfaces.append([])
            for cl in range(8): # for 8 columns
                self.lyt[rw].append(colors[ccnt]) # the [0][0] lyt cell will have the color of the random colors list
                self.lyt_surfaces[rw].append(
                    pygame.Surface((tile_size, tile_size))) # create a surface in lyt_surfaces[0][0]
                self.lyt_surfaces[rw][cl].fill(colors[ccnt]) # with the color of the first... colors list random, same as lyt
                xstr =[str(x) for x in colors[ccnt]]
                key = ", ".join(xstr)

                self.lyt_surfaces[rw][cl].blit(tiles, (0,0), (clr[key][1]*tile_size, clr[key][0]*tile_size, tile_size, tile_size))
                # create the dark tile for the dark_surfaces list
                self.drk_surfaces[rw].append(pygame.Surface((tile_size, tile_size)))
                self.drk_surfaces[rw][cl].fill((0,0,0))
                # print(ccnt)
                ccnt += 1

first_try = 0
attempt = 0 # number of try
won = 0 # number of matches
score = 0
couple = 0
start = pygame.time.get_ticks()
font = pygame.font.SysFont("Arial", 14)
pygame.mouse.set_visible(False)
def message(text, middle=0) -> pygame.Surface:
    ''' to put it in the middle of the screen pass middle=1 '''
    t = font.render(text, 1, (255, 255, 255))
    if middle:
        trect = t.get_rect(center=(8*tile_size//2, 8*tile_size//2))
        return t, trect
    else:
        return t

# this are for the transform.scale in the particles
scaling = 0
scale_x = 0
class Win:
    def __init__(self):
        couples = 32
        cols, rows = (8,8)
        # tile_size = tile_size
        size = cols*tile_size, rows*tile_size
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        pygame.display.set_caption("MatchPair 1.6")
        self.clock = pygame.time.Clock()
        self.game_played = -1
        self.start_menu()

    def start_menu(self):
        score = 0
        # this is where the game starts to know how many seconds you play
        self.game_played += 1
        self.particles = []
        self.particles0 = []
        self.particles2 = []
        self.matches = 0
        ''' ------------------------- START MENU ------------------ '''
        tiles = pygame.image.load(random.choice(glob("images\\*.png")))
        self.grid = Generator()
        loop = 1
        while loop:

            self.screen.fill(0)
            
            self.particles_run_glitter(random.randint(0, 8*tile_size), (255, 255, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = 0
                elif pygame.mouse.get_pressed()[0]:
                    loop = 0
                    self.game_time = 0
                    self.game_loop()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        loop = 0
                        self.game_time = 0
                        self.game_loop()
            self.screen.blit(message("Press 1 for EASY"), (0,50))
            self.screen.blit(message("Press 2 for NORMAL"), (0,70))
            self.screen.blit(message("Press 3 for HARD"), (0,90))
            m, mrect = message("Match pair 1.6", middle=1)
            self.screen.blit(m, mrect)
            pygame.draw.circle(self.screen, (255, 255, 255), pygame.mouse.get_pos(), 10)
            if self.game_played > 0:
                self.screen.blit(message(f"SCORE {score} - TIME {self.game_time}"), (0,0))
            self.clock.tick(60)
            pygame.display.flip()
        pygame.quit()


    def draw_screen(self):
        # self.screen.blit(bg, (0, 0))
        self.screen.fill(0)
        for nrow, row in enumerate(self.grid.drk_surfaces):
            for ncol, col in enumerate(row):
                self.screen.blit(col, (ncol*tile_size, nrow*tile_size))
        self.particles_run_snow(random.randint(0, 8*tile_size), (255, 255, 255))
        self.draw_lines()
        self.screen.blit(message(f"SCORE {score} - TIME {pygame.time.get_ticks()//720}"), (0,0))
        self.particles_run_glitter(random.randint(0, 8*tile_size), (255, 255, 255))

    def draw_lines(self):
        for x in range(8):
            pygame.draw.line(self.screen, (255, 255, 255), (tile_size*x, 0), (tile_size*x, 8 * tile_size))
            pygame.draw.line(self.screen, (255, 255, 255), (0, tile_size * x), (8 * tile_size, tile_size * x))
        pygame.draw.line(self.screen, (255, 255, 255), (tile_size * 8 - 1, 0), (tile_size * 8- 1, 8 * tile_size))
        pygame.draw.line(self.screen, (255, 255, 255), (0, tile_size * 8 - 1), (8 * tile_size, tile_size * 8 - 1))

    def particles_run_snow(self, pos, color):
        """ Creates particles starting from pos with a color """
        self.particles0.append([
            [pos, 0],
            [random.randint(0, 20) / 10 - 1, 2],
            random.randint(2,4)])
        # Moving the coordinates and size of self.particles
        for particle in self.particles0[:]:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.005 # how fast circles shrinks
            particle[1][1] += 0.01 # circles speed
            # if particle[2] <= 0:
            if particle[0][1] > 8*tile_size or particle[0][0] > 8*tile_size:
                self.particles0.remove(particle)
        # Draw circles
        for particle in self.particles0:
            pygame.draw.circle(
                self.screen, (color),
            (round(particle[0][0]), round(particle[0][1])),
             round(particle[2]))

    def explosion_fx(self, r1, c1, r2, c2):     
        for i in range(10):

            # self.particles2.append(
            #     [
            #      [pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]],
            #      [random.randint(0, 42) / 6 - 3.5, random.randint(0, 42) / 6 - 3.5],
            #      random.randint(4, 6)])
            self.particles2.append(
                [
                 [c1*tile_size + 50, r1*tile_size + 50],
                 [random.randint(0, 42) / 6 - 3.5, random.randint(0, 42) / 6 - 3.5],
                 random.randint(4, 6)])
            self.particles2.append(
                [
                 [c2*tile_size + 50, r2*tile_size + 50],
                 [random.randint(0, 42) / 6 - 3.5, random.randint(0, 42) / 6 - 3.5],
                 random.randint(4, 6)])

    def particles_explosion(self, pcolor):
        ''' call this in a for i in range(10) '''
        ''' in the while loop:
        particles_explosion(particles)

        and this will ignite the esplosion
            if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in range(10):
                    particles.append(
                        [
                         [mx, my],
                         [random.randint(0, 42) / 6 - 3.5, random.randint(0, 42) / 6 - 3.5],
                         random.randint(4, 6)])
        
        I'll try with this function instead (4.8.2021)

        def explosion_fx():     
            for i in range(10):
                particles.append(
                    [
                     [mx, my],
                     [random.randint(0, 42) / 6 - 3.5, random.randint(0, 42) / 6 - 3.5],
                     random.randint(4, 6)])


            '''
        scale_x = 0
        for particle in self.particles2:
            particle[0][0] += particle[1][0]
            loc_str = str(int(particle[0][0] / tile_size)) + ';' + str(int(particle[0][1] / tile_size))
            # if loc_str in tile_map:
            #     particle[1][0] = -0.7 * particle[1][0]
            #     particle[1][1] *= 0.95
            #     particle[0][0] += particle[1][0] * 2
            particle[0][1] += particle[1][1]
            loc_str = str(int(particle[0][0] / tile_size)) + ';' + str(int(particle[0][1] / tile_size))
            # if loc_str in tile_map:
            #     particle[1][1] = -0.7 * particle[1][1]
            #     particle[1][0] *= 0.95
            #     particle[0][1] += particle[1][1] * 2
            particle[2] -= 0.035
            particle[1][1] += 0.15
            # self.surf.set_colorkey(pcolor)
            # ======================================= EXPLOSION ================================
            scaling = (100-int(particle[1][1]*10))
            if scaling > 0:
                scale_x = scaling
            self.screen.blit(
                pygame.transform.scale(self.surf, (scale_x, scale_x)), 
                (particle[0][0], particle[0][1]))
            pygame.draw.circle(self.screen, pcolor, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
            if particle[2] <= 0:
                self.particles2.remove(particle)

    def delete(self, r1, c1, r2, c2):
      srf_black = pygame.Surface((tile_size, tile_size))
      srf_black.fill((0,0,0))
      self.grid.drk_surfaces[r1][c1] = srf_black
      srf_black = pygame.Surface((tile_size, tile_size))
      srf_black.fill((0,0,0))
      self.grid.drk_surfaces[r2][c2] = srf_black
    
    def pick(self):
      if pygame.time.get_ticks() - start < time_level:
          for nrow, row in enumerate(self.grid.lyt_surfaces):
              for ncol, col in enumerate(row):
                  self.screen.blit(col, (ncol*tile_size, nrow*tile_size))
          self.particles_run(random.randint(0, 8*tile_size), (255, 255, 255))
          self.draw_lines()
      else:
          pass
          # put sound "change" in japanes
      self.screen.blit(message(f"SCORE {score} - TIME {pygame.time.get_ticks()//720}"), (0,0))

    def rnd(self):
        return random.randrange(0, 8*tile_size)


    def particles_rnd_positions(self):
        for n in range(100):
            self.particles.append([
                [self.rnd(), self.rnd()], # it starts from here, I want it to be anywhere in width and hight
                [random.randint(0, 20) / 10 - 1, 2],
                random.randint(2,4)])

    def particles_run_glitter(self, pos, color):
        """ Creates particles starting from pos with a color """

        # Moving the coordinates and size of self.particles
        for particle in self.particles[:]:
            # particle[0][0] += particle[1][0]
            # particle[0][1] += particle[1][1]
            particle[2] -= 0.5 # how fast circles shrinks
            # particle[1][1] += 0.01 # circles speed
            if particle[2] <= 0:
            # if particle[0][1] > 8*tile_size or particle[0][0] > 8*tile_size:
                self.particles.remove(particle)
        # Draw circles
        for particle in self.particles:
            pygame.draw.circle(
                self.screen, (color),
            (round(particle[0][0]), round(particle[0][1])),
             round(particle[2]))
        if self.particles == []:
            self.particles_rnd_positions()

    def delete(self, r1, c1, r2, c2):
        srf_black = pygame.Surface((tile_size, tile_size))
        srf_black.fill((0,0,0))
        self.grid.drk_surfaces[r1][c1] = srf_black
        srf_black = pygame.Surface((tile_size, tile_size))
        srf_black.fill((0,0,0))
        self.grid.drk_surfaces[r2][c2] = srf_black
    
    def pick(self):
        global count_taken

        if pygame.time.get_ticks() - start < time_level and not count_taken:
            for nrow, row in enumerate(self.grid.lyt_surfaces):
                for ncol, col in enumerate(row):
                    self.screen.blit(col, (ncol*tile_size, nrow*tile_size))
            self.particles_run_glitter(random.randint(0, 8*tile_size), (255, 255, 255))
            self.draw_lines()
        else:
            pass
            # put sound "change" in japanes
        self.screen.blit(message(f"SCORE {score} - TIME {self.game_time}"), (0,0))


    def game_loop(self):
        global first_try, start, attempt, score, music, hiding, count_taken


        start = pygame.time.get_ticks()

        count_taken = 0
        score = 0
        music_on = 0
        try_start = 0
        loop = 1
        while loop:
            if pygame.time.get_ticks() % 720 == 0:
                self.game_time += 1
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

            # ============================== EVENTS HANDLER =====================
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = 0
                if pygame.mouse.get_pos()[0] < 8*tile_size and pygame.mouse.get_pos()[1] < 8*tile_size: 
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        col, row = x//tile_size,  y//tile_size

                        if self.grid.lyt[row][col] != [0,0,0]:
                            print(self.grid.lyt[row][col])
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
                                first = self.grid.lyt[row][col]
                                self.pointer_clr = self.grid.lyt[row][col]
                                r1, c1 = row, col
                                surf1 = self.grid.lyt_surfaces[r1][c1].copy()
                                
                                self.grid.drk_surfaces[r1][c1] = surf1
                                pygame.draw.rect(self.grid.lyt_surfaces[r1][c1], (255, 255, 255), (0,0,tile_size ,tile_size ), 6)
                                
                            # ===================================== [ 2 ] === #
                            if count_taken == 2:
                                # winsound.Beep(200, 100)
                                second = self.grid.lyt[row][col]
                                r2, c2 = row, col
                                self.surf = self.grid.lyt_surfaces[r2][c2].copy()
                                self.surf.set_colorkey(self.grid.lyt[row][col])
                                surf2 = self.grid.lyt_surfaces[r2][c2].copy()
                                self.grid.drk_surfaces[r2][c2] = surf2

                                if (r2, c2) != (r1, c1):
                                    print(r2, c2, "-", r1, c1)
                                    if first == second:
                                        print("Hai trovato una coppia")
                                        score += 10
                                        play(snd_win)
                                        # winsound.Beep(1500, 100)
                                        count_taken = 0
                                        # self.grid.drk_surfaces[r1][c1].set_alpha(128)
                                        # self.grid.drk_surfaces[r2][c2].set_alpha(128)
                                        self.grid.drk_surfaces[r1][c1].fill((50,50,50))
                                        self.grid.drk_surfaces[r2][c2].fill((50,50,50))
                                        self.grid.lyt_surfaces[r1][c1].fill(0)
                                        self.grid.lyt_surfaces[r2][c2].fill(0)
                                        # self.grid.drk_surfaces[r1][c1].fill((self.grid.lyt[r1][c1]))
                                        # self.grid.drk_surfaces[r1][c1].fill((self.grid.lyt[r1][c1]))
                                        # self.grid.lyt_surfaces[r1][c1].fill((self.grid.lyt[r1][c1]))
                                        # self.grid.lyt_surfaces[r2][c2].fill((self.grid.lyt[r2][c2]))

                                        self.pcolor = self.grid.lyt[r1][c1]
                                        self.grid.lyt[r1][c1] = [0,0,0]
                                        self.grid.lyt[r2][c2] = [0,0,0]
                                        self.grid.drk_surfaces[r1][c1].set_alpha(128)
                                        self.grid.drk_surfaces[r2][c2].set_alpha(128)
                                        # self.grid.lyt_surfaces[r1][c1].set_alpha(128)
                                        # self.grid.lyt_surfaces[r2][c2].set_alpha(64)
                                        # pygame.draw.rect(self.grid.lyt_surfaces[r1][c1], (250,250,250), (0,0,tile_size ,tile_size ), 40)
                                        # pygame.draw.rect(self.grid.lyt_surfaces[r2][c2], (250,250,250), (0,0,tile_size ,tile_size ), 40)
                                        pygame.draw.rect(self.grid.drk_surfaces[r1][c1], (250,250,250), (0,0,tile_size ,tile_size ), 40)
                                        pygame.draw.rect(self.grid.drk_surfaces[r2][c2], (250,250,250), (0,0,tile_size ,tile_size ), 40)
                                        couple = 1
                                        start = pygame.time.get_ticks()
                                        self.pick()
                                        self.matches += 1
                                        print(self.pcolor)
                                        self.explosion_fx(r1, c1, r2, c2)
                                       
                                        if self.matches == 32:
                                            print(f"Il tuo punteggio è {score} - raggiunto in {self.game_time} secondi ")
                                            with open("punteggi.txt", 'a') as scorefile:
                                                scorefile.write(f"""Punti: {score}, Time: {self.game_time} - {daytime}
                                                    """)
                                            self.start_menu()
                                    else:
                                        print("Sono diversi")
                                        play(snd_whip)
                                        count_taken = 0
                                        self.grid.lyt_surfaces[r1][c1] = surf1.copy()
                                        self.grid.lyt_surfaces[r2][c2] = surf2.copy()
                                        couple = 0
                                        attempt += 1
                                        self.grid.drk_surfaces[r1][c1] = surf1
                                        if score > 0:
                                            score -= 1
                
                                else:
                                    print("Devi cliccare su un'altra casella")
                                    play(snd_whip)
                                    # self.grid.lyt_surfaces[r1][c1] = surf1.copy()
                                    count_taken = 1
                                # couple = 0
                # if event.type == pygame.VIDEORESIZE:
                #     self.width, self.height = event.size
                #     # redraw win in new size
                #     pygame.display.set_mode((self.width, self.height))
            # mx, my = pygame.mouse.get_pos()
                #print(row, col)
            self.draw_screen()
            self.pick()
            #     # self.screen.blit(pygame.transform.scale(surf1, (50,50)), (mx-25, my-25))
            #     surf1.set_alpha(128)
            #     # self.screen.blit(surf1, (mx - 50, my - 50))
            mx, my = pygame.mouse.get_pos()
            mcol, mrow = mx//tile_size,  my//tile_size
            if self.grid.lyt[mrow][mcol] == [0,0,0]:
                pygame.draw.circle(self.screen, (255,0,0), pygame.mouse.get_pos(), 10, 2) 
            elif count_taken == 1: 
                pygame.draw.circle(self.screen, self.pointer_clr, pygame.mouse.get_pos(), 10, 10) 
                pygame.draw.circle(self.screen, (255, 255, 255), pygame.mouse.get_pos(), 20, 10) 
            else:
                pygame.draw.circle(self.screen, (255, 255, 255), pygame.mouse.get_pos(), 10)

            if self.matches > 0:
                self.particles_explosion(self.pcolor)
            self.clock.tick(60)
            pygame.display.flip()
        pygame.quit()












win = Win()
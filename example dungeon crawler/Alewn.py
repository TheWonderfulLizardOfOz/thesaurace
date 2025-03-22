#1234567890123456789012345678901234567890123456789012345678901234567890123456789
import random, copy, pygame, sys, os, math
class Board: # Board Class
    def __init__(self): # Board Class Initialisation
        self.grid = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        for j in range(len(self.grid)): # Setting up empty grid
            [self.grid[j].append("■") for i in range(15)]
        tun = [random.randint(1,13), random.randint(1,13)]
        for i in range(40): # Setting up the tunnels
            dir = random.randint(1, 4)
            for j in range(random.randint(2, 8)):
                tun[0] -= 1 if (dir == 1 and tun[0] != 1) else 0
                tun[0] += 1 if (dir == 2 and tun[0] != 13) else 0
                tun[1] -= 1 if (dir == 3 and tun[1] != 1) else 0
                tun[1] += 1 if (dir == 4 and tun[1] != 13) else 0
                self.grid[tun[0]][tun[1]] = " "
        self.grid[tun[0]][tun[1]] = "0" # Setting up exit
        self.map = copy.deepcopy(self.grid) # Making map copy
    def display(self, player):
        for i in range(15):
            for j in range(15):
                font = pygame.font.SysFont('Courier', 40, False, False)
                if self.grid[i][j] == "■":
                    game_window.blit(stone, (0+(j*40), 0+(i*40)))
                elif self.grid[i][j] == " ":
                    game_window.blit(grass, (0+(j*40), 0+(i*40)))
                elif self.grid[i][j] == "X":
                    game_window.blit(grass, (0+(j*40), 0+(i*40)))
                    game_window.blit(lord, (0+(j*40), 0+(i*40)))
                elif self.grid[i][j] == "S":
                    game_window.blit(grass, (0+(j*40), 0+(i*40)))
                    game_window.blit(sword, (0+(j*40), 0+(i*40)))
                elif self.grid[i][j] == "L":
                    game_window.blit(grass, (0+(j*40), 0+(i*40)))
                    game_window.blit(lance, (0+(j*40), 0+(i*40)))
                elif self.grid[i][j] == "0":
                    game_window.blit(grass, (0+(j*40), 0+(i*40)))
                    game_window.blit(stairs, (0+(j*40), 0+(i*40)))
        font = pygame.font.SysFont('Impact', 60, False, False)
        rect = pygame.Rect(0, 600, 600, 150)
        pygame.draw.rect(game_window, (0,0,0), rect)
        pygame.display.update()
        text = font.render("HEALTH: " + str(player.get_health()), True, (255, 255, 255))
        game_window.blit(text, (10, 600))
        text = font.render("FLOOR: " + str(player.get_floor()), True, (255, 255, 255))
        game_window.blit(text, (10, 660))
        pygame.display.update()
    def get_tile(self, location): # Getting the map tile
        return self.grid[location[0]][location[1]]
    def map_update(self, player, enemies): # Updating displayed map
        self.grid = copy.deepcopy(self.map) # Reverts to blank map
        self.grid[player.get_loc()[0]][player.get_loc()[1]] = "X"
        for i in range(len(enemies)): # Adds enemy icons
            enemy_loc = enemies[i].get_loc()
            self.grid[enemy_loc[0]][enemy_loc[1]] = enemies[i].get_token()
class Player: # Player Class
    def __init__(self, health): # player object initialisation
        self.health = health # player health
        self.score = 0
        self.loc = [7,7]
        self.floor = 1
    def new_loc(self, board):
        valid = False
        while valid == False: # Gets a valid starting location
            self.loc = [random.randint(1, 13), random.randint(1, 13)]
            valid = True if board.get_tile(self.loc) == " " else False
    def get_loc(self): # Getter for player location
        return self.loc
    def get_floor(self): # Getter for player floor
        return self.floor
    def get_score(self): # Getter for player score
        return self.score
    def get_health(self): # Getter for player health
        return self.health
    def mult_health(self):
        self.score += (self.health * 200)
    def lose_health(self, health_loss):
        self.health -= health_loss
    def turn(self, board, enemies, choice): # Player turn
        cur_loc = copy.deepcopy(self.loc)
        if 1==1:
            self.loc[0] -= 1 if (choice == "W" and self.loc[0] != 1) else 0
            self.loc[0] += 1 if (choice == "S" and self.loc[0] != 13) else 0
            self.loc[1] -= 1 if (choice == "A" and self.loc[1] != 1) else 0
            self.loc[1] += 1 if (choice == "D" and self.loc[1] != 13) else 0
            if board.get_tile(self.loc) == "■": # Checking the tile's empty
                self.loc = copy.deepcopy(cur_loc)
            for enemy in enemies:
                if enemy.get_loc() == self.loc:
                    self.score += 100
                    enemies.remove(enemy)
                    self.loc = copy.deepcopy(cur_loc)
            if board.get_tile(self.loc) == "0":
                enemies = "NewFloor"
                self.score += 500
                self.floor += 1
        return enemies
    def try_move(self, board, enemies, move):
        cur_loc = copy.deepcopy(self.loc)
        self.loc[0] -= 1 if (choice == "W" and self.loc[0] != 1) else 0
        self.loc[0] += 1 if (choice == "S" and self.loc[0] != 13) else 0
        self.loc[1] -= 1 if (choice == "A" and self.loc[1] != 1) else 0
        self.loc[1] += 1 if (choice == "D" and self.loc[1] != 13) else 0
        if board.get_tile(self.loc) == "■" or self.loc == cur_loc:
            self.loc = copy.deepcopy(cur_loc)
            return False
        else:
            self.loc = copy.deepcopy(cur_loc)
            return True
class Enemy(Player): # Enemy Class
    def __init__(self, board, pl, enemies):
        tokens = ["S", "L", "S"]
        self.token = random.choice(tokens)
        valid = False
        while valid == False: # Gets a valid starting location
            self.loc = [random.randint(1, 13), random.randint(1, 13)]
            valid=True if (board.get_tile(self.loc)==" " and self.loc!=pl) else False
            for enemy in enemies:
                if enemy.get_loc() == self.loc and valid == True:
                    enemies.remove(enemy)
    def get_token(self):
        return self.token
    def turn(self, board, player, enemies): # Enemy Turn Method
        atk = False
        mov = False
        cur_loc = copy.deepcopy(self.loc)
        pos = [[2,0],[-2,0],[0,2],[0,-2]]
        pl = player.get_loc()
        if self.token == "\033[0;91mS\033[0m" or self.token == "S": # Swordsman AI
            for it in pos:# Swordsman attack AI
                if pl[0]==self.loc[0]+(it[0]//2) and pl[1]==self.loc[1]+(it[1]//2):
                    atk = True
            if atk == True:
                player.lose_health(2)
                game_window.fill((77,0,0))
                pygame.display.update()
                board.display(player)
            if atk == False: 
                for it in pos: # Swordsman movement AI (Cardinal Direction)
                    if pl[0] == self.loc[0] + it[0] and pl[1] == self.loc[1] + it[1]:
                        nt = board.get_tile([self.loc[0]+(it[0]//2),self.loc[1]+(it[1]//2)])
                        if nt != "■":
                            self.loc=[self.loc[0]+(it[0]//2),self.loc[1]+(it[1]//2)]
                            mov = True
                if mov == False: # Swordsman movement AI (Diagonal Direction)
                    m1 = [[1,1],[1,-1],[-1,1],[-1,-1]]
                    m2 = [[1,0],[0,-1],[0,1],[-1,0], [0,1],[1,0],[-1,0],[0,-1]]
                    for i in range(0,4):
                        nt = board.get_tile([self.loc[0]+m2[i][0],self.loc[1]+m2[i][1]])
                        nt2=board.get_tile([self.loc[0]+m2[i+4][0],self.loc[1]+m2[i+4][1]])
                        if pl[0]==self.loc[0] + m1[i][0] and pl[1]==self.loc[1] + m1[i][1]:
                            if nt != "■":
                                self.loc = [self.loc[0] + m2[i][0], self.loc[1] + m2[i][1]]
                                mov = True
                            elif nt2 != "■":
                                self.loc=[self.loc[0] + m2[i+4][0], self.loc[1] + m2[i+4][1]]
                                mov = True
                    if mov == False and random.randint(1,3) == 1:
                        valid = False # Swordsman movement AI (Random Move)
                        fail_count = 0
                        while valid == False and fail_count < 5:
                            dir = random.randint(1,4)
                            self.loc[0] -= 1 if (dir == 1 and self.loc[0] != 1) else 0
                            self.loc[0] += 1 if (dir == 2 and self.loc[0] != 13) else 0
                            self.loc[1] -= 1 if (dir == 3 and self.loc[1] != 1) else 0
                            self.loc[1] += 1 if (dir == 4 and self.loc[1] != 13) else 0
                            if board.get_tile(self.loc) != " ":
                                valid = False
                                fail_count += 1
                                self.loc = copy.deepcopy(cur_loc)
                            else:
                                valid = True
                for enemy in enemies: # Checking for valid move
                    if enemy.get_loc() == self.get_loc() and enemy != self:
                        self.loc = copy.deepcopy(cur_loc)
        elif self.token == "\033[0;91mL\033[0m" or self.token == "L": # Lancer AI
            for it in pos: # Lancer attack AI
                if pl[0] == self.loc[0] + it[0] and pl[1] == self.loc[1] + it[1]:
                    nt = board.get_tile([self.loc[0]+(it[0]//2),self.loc[1]+(it[1]//2)])
                    if nt != "■":
                        atk = True
            if atk == True:
                player.lose_health(1)
                game_window.fill((77,0,0))
                pygame.display.update()
                board.display(player)
            if atk == False: # Lancer movement AI
                m1 = [[3,0],[-3,0],[0,3],[0,-3]]
                m2 = [[1,0],[-1,0],[0,1],[0,-1]]
                m3 = [[2,0],[-2,0],[0,2],[0,-2]]
                for i in range(0,4):
                    if pl[0]==self.loc[0] + m1[i][0] and pl[1]==self.loc[1] + m1[i][1]:
                        nt = board.get_tile([self.loc[0]+m2[i][0],self.loc[1]+m2[i][1]])
                        nt2 = board.get_tile([self.loc[0]+m3[i][0],self.loc[1]+m3[i][1]])
                        if nt != "■" and nt2 != "■":
                            self.loc=[self.loc[0]+m2[i][0],self.loc[1]+m2[i][1]]
                            mov = True
                for enemy in enemies: # Checking valid move
                    if enemy.get_loc() == self.get_loc() and enemy != self:
                        self.loc = copy.deepcopy(cur_loc)
# Create width and height constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 750
# Initialise all the pygame modules
pygame.init()
# Create a game window
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Set title
pygame.display.set_caption("Dungeon Rift: Alewn")
# PyGame Clock
clock = pygame.time.Clock()
# Blank Window
game_window.fill((0,0,0))
last_point = None
# Controller Setup
joysticks = []
pygame.joystick.init()
for i in range(pygame.joystick.get_count()):
    joysticks.append(pygame.joystick.Joystick(i))
    joysticks[-i].init()
grass = pygame.image.load('grass.png')
stone = pygame.image.load('stone.png')
stairs = pygame.image.load('stairs.png')
lord = pygame.image.load('lord.png')
sword = pygame.image.load('sword.png')
lance = pygame.image.load('lance.png')
logo = pygame.image.load('logo.png')
logotoo = pygame.image.load('DG.png')
game_window.blit(logo, (67, 35))
game_window.blit(logotoo, (25, 609))
pygame.display.update()
choice = False
game_window.blit(lord, (125,300))
font = pygame.font.SysFont('DejaVu Sans', 40, False, False)
text = font.render("START GAME", True, (255, 255, 255))
game_window.blit(text, (180, 295))
text = font.render("QUIT GAME", True, (255, 255, 255))
game_window.blit(text, (180, 395))
sel = 1
pygame.mixer.music.stop()
pygame.mixer.music.load("TTWY.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play()
while choice == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0 and sel == 1:
                choice = True
            if event.button == 0 and sel == 2:
                pygame.quit()
                sys.exit()              
        elif event.type == pygame.JOYHATMOTION:
            if event.value[1] == -1:
                rect = pygame.Rect(125, 300, 40, 40)
                pygame.draw.rect(game_window, (0,0,0), rect)
                game_window.blit(lord, (125,400))
                sel = 2
            if event.value[1] == 1:
                rect = pygame.Rect(125, 400, 40, 40)
                pygame.draw.rect(game_window, (0,0,0), rect)
                game_window.blit(lord, (125,300))
                sel = 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                rect = pygame.Rect(125, 400, 40, 40)
                pygame.draw.rect(game_window, (0,0,0), rect)
                game_window.blit(lord, (125,300))
                sel = 1
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                rect = pygame.Rect(125, 300, 40, 40)
                pygame.draw.rect(game_window, (0,0,0), rect)
                game_window.blit(lord, (125,400))
                sel = 2
            if event.key == pygame.K_RETURN and sel == 1:
                choice = True
            elif event.key == pygame.K_RETURN and sel == 2:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            choice = True
    pygame.display.update()
while True:
    pygame.mixer.music.load('DMFJ.mp3')
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(10)
    player = Player(10)
    enemies = "NewFloor"
    qui = False
    while player.get_health() > 0:
        clock.tick(60)
        if enemies == "NewFloor":
            board = Board()
            player.new_loc(board)
            enemies = []
            fl = player.get_floor()
            for i in range(random.randint(4+(fl//2), 6+(fl//2))):
                enemies.append(Enemy(board, player.get_loc(), enemies))
        board.map_update(player, enemies)
        board.display(player)
        pygame.event.clear()
        start = (0, 0)
        valid_move = False
        while valid_move == False:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 7:
                        pygame.quit()
                        sys.exit()
                    if event.button == 6:
                        qui = True
                        player.lose_health(player.get_health())
                        valid_move = True
                elif event.type == pygame.JOYHATMOTION:
                    if event.value[0] == -1:
                        choice = "A"
                        valid_move = True
                        enemies = player.turn(board, enemies, choice)
                    if event.value[0] == 1:
                        choice = "D"
                        valid_move = True
                        enemies = player.turn(board, enemies, choice)
                    if event.value[1] == -1:
                        choice = "S"
                        valid_move = True
                        enemies = player.turn(board, enemies, choice)
                    if event.value[1] == 1:
                        choice = "W"
                        valid_move = True
                        enemies = player.turn(board, enemies, choice)
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        choice = "W"
                        valid_move = True
                        enemies = player.turn(board, enemies, choice)
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        choice = "A"
                        valid_move = True
                        enemies = player.turn(board, enemies, choice)
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        choice = "S"
                        valid_move = True
                        enemies = player.turn(board, enemies, choice)
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        choice = "D"
                        valid_move = True
                        enemies = player.turn(board, enemies, choice)
                    if event.key == 27:
                        pygame.quit()
                        sys.exit()
                    if event.key == 13:
                        qui = True
                        player.lose_health(player.get_health())
                        valid_move = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    start = event.pos
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if start[0]-event.pos[0] >= 0:
                        if start[1]-event.pos[1]>=0:
                            if start[0]-event.pos[0] > start[1]-event.pos[1]:
                                choice = "A"
                                valid_move = True
                                enemies = player.turn(board, enemies, choice)
                            else:
                                choice = "W"
                                valid_move = True
                                enemies = player.turn(board, enemies, choice)
                        else:
                            if start[0]-event.pos[0] > (start[1]-event.pos[1]) * -1:
                                choice = "A"
                                valid_move = True
                                enemies = player.turn(board, enemies, choice)
                            else:
                                choice = "S"  
                                valid_move = True
                                enemies = player.turn(board, enemies, choice)
                    else:
                        if start[1]-event.pos[1]>=0:
                            if (start[0]-event.pos[0]) * -1 > start[1]-event.pos[1]:
                                choice = "D"
                                valid_move = True
                                enemies = player.turn(board, enemies, choice)
                            else:
                                choice = "W"
                                valid_move = True
                                enemies = player.turn(board, enemies, choice)
                        else:
                            if (start[0]-event.pos[0]) * -1 > (start[1]-event.pos[1]) * -1:
                                choice = "D"
                                valid_move = True
                                enemies = player.turn(board, enemies, choice)
                            else:
                                choice = "S"  
                                valid_move = True
                                enemies = player.turn(board, enemies, choice)
        if enemies != "NewFloor" and qui == False:
            [enemy.turn(board, player, enemies) for enemy in enemies]
    if player.get_health() <= 0 and qui == False:
        game_window.fill((0,0,0))
        font = pygame.font.SysFont('Impact', 220, False, False)
        text = font.render("GAME", True, (255, 0, 0))
        game_window.blit(text, (55, 0))
        text = font.render("OVER", True, (255, 0, 0))
        game_window.blit(text, (75, 220))
        font = pygame.font.SysFont('Tahoma', 80, False, False)
        if player.get_score() < 1000000:
            text = font.render("SCORE: "+ str(player.get_score()), True, (255, 0, 0))
        else:
            text = font.render("SCORE: 999999", True, (255, 0, 0))
        game_window.blit(text, (20, 500))
        pygame.display.update()
        pygame.mixer.music.stop()
        pygame.mixer.music.load("THA.mp3")
        pygame.mixer.music.play()
        while qui == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.JOYBUTTONDOWN and event.button == 7:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == 27:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.JOYBUTTONDOWN and event.button == 6:
                    qui = True
                if event.type == pygame.KEYDOWN and event.key == 13:
                    qui = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    qui = True


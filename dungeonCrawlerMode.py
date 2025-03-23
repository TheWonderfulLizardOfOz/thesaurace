import random, copy, pygame, sys
from gameTextPrototype import get_all_words, get_synonyms_of
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720
pygame.init()
game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dungeon Crawler Mode")
game_window.fill((0,0,0))
last_point = None

stone = pygame.image.load('stone.png')
heart = pygame.image.load('heart.png')
lord = pygame.image.load('lord.png')
wall = pygame.image.load('wall.png')
class Board:
    def __init__(self):

        self.grid = [["S" for _ in range(21)] for _ in range(10)]
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if ((i <= 6) and (j == 1 or j == 7 or j == 13 or j == 19)) or ((i == 0 or i == 6) and (j != 0 and j != 20)):
                    self.grid[i][j] = "W"

        self.grid[6][4] = "S"
        self.grid[6][10] = "S"
        self.grid[6][16] = "S"


    def display(self, player):
        game_window.fill((0, 0, 0))
        font = pygame.font.SysFont('Courier', 40, False, False)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == "S":
                    #game_window.blit(stone, (0+(j*40), 0+(i*40)))
                    pygame.draw.rect(game_window, (128, 255, 128), (0+(j*40), 0+(i*40), 40, 40))
                elif self.grid[i][j] == "W":
                    pygame.draw.rect(game_window, (128, 128, 128), (0+(j*40), 0+(i*40), 40, 40))
                    #game_window.blit(wall, (0 + (j * 40), 0 + (i * 40)))
        for i in range(player.lives):
            game_window.blit(heart, ((40 * i + 4), 4))
        game_window.blit(lord, (player.loc[0] * 40, player.loc[1] * 40))

        text = font.render(player.currentWord, True, (0, 0, 0))
        game_window.blit(text, (10*40 - (text.get_width() // 2), 8*40 - (text.get_height() // 2)))

        text = font.render("Score: {}".format(str(player.score)), True, (255, 255, 255))
        game_window.blit(text, (40, 11 * 40))

        font = pygame.font.SysFont('Courier', 30, False, False)
        for i in range(len(player.options)):
            text = font.render(player.options[i], True, (0, 0, 0))
            game_window.blit(text, ((4.5 + 6 * i) * 40 - text.get_width() // 2 , (2.5 + i) * 40 - (text.get_height() // 2)))


        pygame.display.update()

class Player:
    def __init__(self, lives):
        self.lives = lives
        self.score = 0
        self.loc = (10, 8)
        self.words = get_all_words()
        self.options = []
        self.correct = ""
        self.currentWord = "foundations"
        self.setWords()


    def move(self, board, choice): # Player turn
        directions = {"W": (0, -1), "A": (-1, 0), "S": (0, 1), "D": (1, 0)}
        move = directions[choice]

        newLoc = (self.loc[0] + move[0], self.loc[1] + move[1])
        if 0 <= newLoc[0] < len(board.grid[0]) and 0 <= newLoc[1] < len(board.grid) and board.grid[newLoc[1]][newLoc[0]] == "S":
            self.loc = newLoc
        self.selectOption()

    def enterRoom(self, option):
        if option == self.correct:
            self.score += 1
        else:
            self.lives -= 1

        self.currentWord = self.correct
        self.setWords()
        self.loc = (10, 8)

    def selectOption(self):
        if self.loc == (4, 6):
            self.enterRoom(self.options[0])
        if self.loc == (10, 6):
            self.enterRoom(self.options[1])
        if self.loc == (16, 6):
            self.enterRoom(self.options[2])

    def setWords(self):
        synonyms = get_synonyms_of(self.currentWord)
        self.correct = random.choice(synonyms)
        while len(get_synonyms_of(self.correct)) == 0:
            self.correct = random.choice(synonyms)
        synSet = set(synonyms)
        fakes = []
        i = 0
        while i < 2:
            word = random.choice(self.words)
            if word not in synSet:
                fakes.append(word)
                i += 1
        fakes.append(self.correct)
        random.shuffle(fakes)
        self.options = copy.deepcopy(fakes)

def game():
    currentWord = "foundations"

    words = get_all_words()
    player = Player(3)

    while player.lives > 0:
        board = Board()
        board.display(player)
        pygame.event.clear()

        valid_move = False
        choice = ""
        while not valid_move:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key in {pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d}:
                    choices = {pygame.K_w: "W", pygame.K_a: "A", pygame.K_s: "S", pygame.K_d: "D"}
                    choice = choices[event.key]
                    valid_move = True

        player.move(board, choice)
        end = False
        board.display(player)
        while player.lives <= 0 and not end:
            font = pygame.font.SysFont('Impact', 220, False, False)
            text = font.render("GAME", True, (255, 0, 0))
            game_window.blit(text, (55, 0))
            text = font.render("OVER", True, (255, 0, 0))
            game_window.blit(text, (75, 220))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    end = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    end = True
                if event.type == pygame.KEYDOWN:
                    end = True

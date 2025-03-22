#1234567890123456789012345678901234567890123456789012345678901234567890123456789
import random, pygame, sys, os, asyncio, requests, gameTextPrototype, time

### TEMPLATE FUNCTIONS
class Button:
    def __init__(self, font, text, loc, toState, colour=None):
        self.font = font
        self.text = text
        self.toState = toState
        if colour:
            self.colour = colour
        else:
            self.colour = (0, 0, 0)
        self.font.render(self.text, True, self.colour)
        self.loc = loc
        self.realLoc = (0, 0)
        self.width = 0
        self.height = 0

    def show(self, gameWindow):
        render = self.font.render(self.text, True, self.colour)
        self.realLoc = (self.loc[0] - render.get_width() // 2, self.loc[1] - render.get_height() // 2)
        self.width = render.get_width()
        self.height = render.get_height()
        gameWindow.blit(render, self.realLoc)

    def mouseInButton(self, mouseLoc):
        inWidth = self.realLoc[0] <= mouseLoc[0] <= self.realLoc[0] + self.width
        inHeight = self.realLoc[1] <= mouseLoc[1] <= self.realLoc[1] + self.height
        return inWidth and inHeight


def resource_path(relative_path):

    if PLAT_VER != "WEB":
    
        try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    else:

        return relative_path

def log(message):
    console_log.append([str(message), FRAMERATE * 10])

def window_resize():
    resized_window = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    resized_window.blit(game_window, (0, 0))

    if (true_window.get_height() / true_window.get_width()) > (WINDOW_HEIGHT / WINDOW_WIDTH): ## Needs to match the screen width
        resized_window = pygame.transform.scale(resized_window, (true_window.get_width(), true_window.get_width() / WINDOW_WIDTH * WINDOW_HEIGHT))
    elif (true_window.get_height() / true_window.get_width()) <= (WINDOW_HEIGHT / WINDOW_WIDTH): ## Needs to match the screen height
        resized_window = pygame.transform.scale(resized_window, (true_window.get_height() / WINDOW_HEIGHT * WINDOW_WIDTH, true_window.get_height()))

    font = pygame.font.Font(resource_path('Kenney Pixel.ttf'), 35)

    to_remove = []

    if console_data["Typing"]:
        text = font.render(console_data["Message"], True, (255,255,255))
        
        draw_trans_rect(resized_window, (0, 0, 0), 192, (15, resized_window.get_height() - 40, text.get_width() + 10, text.get_height()))
        resized_window.blit(text, (20, resized_window.get_height() - 40))

    if console_data["Typing"] or DEV_VER == "DEV":
        for i in range(len(console_log)):

            COLOUR = (255, 255, 0)
            TRANS = 160
            if console_log[len(console_log) - 1 - i][1] <= FRAMERATE:
                COLOUR = (192, 192, 0)
                TRANS = 128
            text = font.render(console_log[len(console_log) - 1 - i][0], True, COLOUR)

            draw_trans_rect(resized_window, (0, 0, 0), TRANS, (15, resized_window.get_height() - 67 - i * 27, text.get_width() + 10, text.get_height()))

            #pygame.draw.rect(resized_window, (0, 0, 0), (15, resized_window.get_height() - 67 - i * 25, text.get_width() + 10, text.get_height()))
            
            resized_window.blit(text, (20, resized_window.get_height() - 65 - i * 27))

            console_log[len(console_log) - 1 - i][1] -= 1
            if console_log[len(console_log) - 1 - i][1] == 0:
                to_remove.append(len(console_log) - 1 - i)

        for i in range(len(to_remove)):
            console_log.pop(0)

        if console_data["Last Command"] != "":

            text = font.render(str(console_data["Last Command"]), True, (0, 255, 255))
            draw_trans_rect(resized_window, (0, 0, 0), 192, (resized_window.get_width() - 10 - text.get_width(), 0, 10 + text.get_width(), text.get_height()))
            resized_window.blit(text, (resized_window.get_width() - 5 - text.get_width(), 0))

    if console_data["FPS"]:

        text = font.render(str(int(clock.get_fps())), True, (0, 255, 0))
        draw_trans_rect(resized_window, (0, 0, 0), 192, (resized_window.get_width() - 10 - text.get_width(), resized_window.get_height() - text.get_height(), 10 + text.get_width(), text.get_height()))
        resized_window.blit(text, (resized_window.get_width() - 5 - text.get_width(), resized_window.get_height() - text.get_height()))
    
    true_window.blit(resized_window, (true_window.get_width() // 2 - resized_window.get_width() // 2, true_window.get_height() // 2 - resized_window.get_height() // 2))

    pygame.display.update()

def global_inputs():

    non_global_inputs = []

    for event in pygame.event.get():
        handled_input = False
        
        if event.type == pygame.QUIT:
            handled_input = True
            quit_game()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                handled_input = True
                quit_game()

            if event.key == 96 or event.key == pygame.K_0:
                handled_input = True
                console_data["Typing"] = not console_data["Typing"]
                        
            elif event.key > 31 and event.key < 127 and event.key != 96 and console_data["Typing"]:#not backspace or weird characters
                handled_input = True
                console_data["Message"] += event.unicode #put character in text
            elif event.key == pygame.K_RETURN and console_data["Typing"]:#return
                handled_input = True
                log(console_data["Message"])
                console_data["Command"] = console_data["Message"]
                console_data["Message"] = ""
                console_data["Typing"] = False
            elif event.unicode == '\x08' and console_data["Typing"]:#backspace
                handled_input = True
                console_data["Message"] = console_data["Message"][:-1]#undo

        if handled_input == False:
            non_global_inputs.append(event)

    if console_data["Command"] == "fps":
        console_data["Last Command"] = "fps"
        console_data["Command"] = ""
        console_data["FPS"] = not console_data["FPS"]

    if console_data["Command"] == "help":
        console_data["Last Command"] = "help"
        console_data["Command"] = ""
        log("fps - turn on/off fps display")

    return non_global_inputs

def draw_trans_rect(window, colour, trans, rect):
    s = pygame.Surface((rect[2],rect[3]))
    s.set_alpha(trans)
    s.fill(colour)
    window.blit(s, (rect[0], rect[1]))

def true_mouse_loc():
    false_loc = pygame.mouse.get_pos()
    real_loc = [false_loc[0], false_loc[1]]

    if (true_window.get_height() / true_window.get_width()) > (WINDOW_HEIGHT / WINDOW_WIDTH): ## Needs to match the screen width
        bar_size = true_window.get_height() - (true_window.get_width() / WINDOW_WIDTH * WINDOW_HEIGHT)
        real_loc[1] -= (bar_size // 2)

        real_loc[0] = real_loc[0] / true_window.get_width() * WINDOW_WIDTH
        real_loc[1] = real_loc[1] / (true_window.get_width() / WINDOW_WIDTH * WINDOW_HEIGHT) * WINDOW_HEIGHT
        
    elif (true_window.get_height() / true_window.get_width()) <= (WINDOW_HEIGHT / WINDOW_WIDTH): ## Needs to match the screen height
        bar_size = true_window.get_width() - (true_window.get_height() / WINDOW_HEIGHT * WINDOW_WIDTH)
        real_loc[0] -= (bar_size // 2)   

        real_loc[1] = real_loc[1] / true_window.get_height() * WINDOW_HEIGHT    
        real_loc[0] = real_loc[0] / (true_window.get_height() / WINDOW_HEIGHT * WINDOW_WIDTH) * WINDOW_WIDTH 
    
    return real_loc

def quit_game():
    pygame.quit()
    sys.exit()

### GAME CLASSES / FUNCTIONS
def checkMouseClick(buttons, game_state):
    mouse_loc = true_mouse_loc()
    for button in buttons:
        if button.mouseInButton(mouse_loc):
            game_state = button.toState
            log(("new game state: " + game_state))
    return game_state

def setGoalWord(currentWord, difficulty):
    back = currentWord
    i = 0
    while i < 15:
        synonyms = gameTextPrototype.get_synonyms_of(currentWord)
        #print(currentWord, synonyms)
        if len(synonyms) == 0:
            currentWord = back
            i -= 1
        else:
            back = currentWord
            currentWord = random.choice(synonyms)
        i += 1
    return currentWord

### MAIN FUNCTION
async def main():

    options = ["START"]

    game_state = "MAIN MENU"
    
    while True:

        while game_state == "MAIN MENU": # the main menu
            buttons = []
            clock.tick(FRAMERATE)

            junk = random.randint(0, 20)

            ## display

            game_window.fill((255, 255, 255))

            #game_window.blit(logo, (WINDOW_WIDTH // 2 - logo.get_width() // 2, 0))
            #game_window.blit(logotoo, (25, WINDOW_HEIGHT - 20 - logotoo.get_height()))

            font = pygame.font.Font(resource_path('Kenney Pixel.ttf'), 120)

            # startText = font.render("START", True, (0, 0, 0))
            # startLoc = (WINDOW_WIDTH // 2 - startText.get_width() // 2, (WINDOW_HEIGHT // 2) - startText.get_height() // 2)
            # game_window.blit(startText, startLoc)
            startButton = Button(font, "START", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), "START")
            startButton.show(game_window)
            creditButton = Button(font, "CREDITS", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + startButton.height), "CREDITS")
            creditButton.show(game_window)
            buttons = [startButton, creditButton]

            window_resize()

            events = global_inputs()
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                                    
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        game_state = "START"
                        log(("new game state: " + game_state))    

                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = checkMouseClick(buttons, game_state)



        await asyncio.sleep(0)

        while game_state == "START": # the actual gameplay

            game_end = False

            current_word = "foundations"

            syn_list = gameTextPrototype.get_synonyms_of(current_word)

            goal_word = setGoalWord(current_word, 15)

            history = []
            
            font = pygame.font.Font(resource_path('Lora.ttf'), 80)
            
            fonter = pygame.font.Font(resource_path('Lora.ttf'), 50)

            fontest = pygame.font.Font(resource_path('Lora.ttf'), 65)

            scroll = 0

            timer = [0, 0, 0]

            while game_end == False:

                clock.tick(FRAMERATE)

                timer[0] += 1
                if timer[0] == FRAMERATE:
                    timer[0] = 0
                    timer[1] += 1
                    if timer[1] == 60:
                        timer[1] = 0
                        timer[2] += 1

                game_window.fill((255, 255, 255))

                text = font.render(current_word.upper(), True, (0, 0, 0))
                game_window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 75))

                if len(history) > 0:
                    undocol = (0, 0, 0)
                else:
                    undocol = (128,128,128)

                texter = fonter.render("UNDO", True, undocol)
                game_window.blit(texter, (90 - texter.get_width() // 2, 40 - texter.get_height() // 2))

                pygame.draw.rect(game_window, undocol, (5, 5, 170, 70), 5, 10)

                texter = fonter.render("QUIT", True, (0, 0, 0))
                game_window.blit(texter, (WINDOW_WIDTH - 90 - texter.get_width() // 2, 40 - texter.get_height() // 2))

                texter = fonter.render("goal: " + goal_word, True, (0, 0, 0))
                game_window.blit(texter, (WINDOW_WIDTH // 2 - texter.get_width() // 2, 40 - texter.get_height() // 2))

                pygame.draw.rect(game_window, (0, 0, 0), (WINDOW_WIDTH - 175, 5, 170, 70), 5, 10)

                min_str = str(timer[2])
                if len(min_str) < 2:
                    min_str = "0" + min_str

                sec_str = str(timer[1])
                if len(sec_str) < 2:
                    sec_str = "0" + sec_str

                time_str = min_str + ":" + sec_str

                texter = fonter.render(time_str, True, (0, 0, 0))
                game_window.blit(texter, (WINDOW_WIDTH // 2 - texter.get_width() // 2, WINDOW_HEIGHT - texter.get_height() - 10))

                j = 0
                for i in range(scroll, min(scroll + 6, len(syn_list) - 1)):
                    textest = fontest.render(syn_list[i], True, (0, 0, 0))
                    game_window.blit(textest, (100, 200 + j*65))
                    j += 1
        
                window_resize()

                events = global_inputs()
                
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        ml = true_mouse_loc()

                        if event.button < 4:

                            if ml[0] < 180 and ml[1] < 80:
                                if len(history) > 0:
                                    current_word = history.pop()
                            if ml[0] > WINDOW_WIDTH - 180 and ml[1] < 80:
                                game_end = True
                                game_state = "MAIN MENU"

                        if event.button == 5:
                            scroll += 1
                            if scroll > len(syn_list) - 1:
                                scroll = len(syn_list) - 1
                        elif event.button == 4:
                            scroll -= 1
                            if scroll < 0:
                                scroll = 0
                            
                await asyncio.sleep(0)

        while game_state == "CREDITS":
            clock.tick(FRAMERATE)

            ## display

            game_window.fill((255, 255, 255))

            font = pygame.font.Font(resource_path('Kenney Pixel.ttf'), 120)

            backButton = Button(font, "BACK TO MENU", (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2), "MAIN MENU")
            backButton.show(game_window)
            buttons = [backButton]

            window_resize()

            events = global_inputs()

            for event in events:
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        game_state = "MAIN MENU"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = checkMouseClick(buttons, game_state)

            await asyncio.sleep(0)



# Create width and height constants
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 720
# Initialise all the pygame modules
pygame.init()
# Create a game window
true_window = pygame.display.set_mode((960, 720), pygame.RESIZABLE)
game_window = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
# Set title
pygame.display.set_caption("TEMPLATE")
# PyGame Clock
clock = pygame.time.Clock()
# Blank Window
game_window.fill((255, 255, 255))
pygame.display.update()

console_log = []
console_data = {"Message": "",
                "Typing": False,
                "Command": "",
                "Last Command": "",
                "FPS": False}
    
PLAT_VER = "WIN"
DEV_VER = "DEV"
FRAMERATE = 60

if DEV_VER == "DEV":
    console_data["FPS"] = True
            
asyncio.run( main() )

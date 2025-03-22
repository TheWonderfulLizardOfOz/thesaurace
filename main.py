#1234567890123456789012345678901234567890123456789012345678901234567890123456789
import random, copy, pygame, sys, os, math, time, asyncio

### TEMPLATE FUNCTIONS

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

### MAIN FUNCTION

async def main():

    options = ["START", "TUTORIAL", "CREDITS"]

    game_state = "MAIN MENU"

    sel = 0
    count = 0
    mov = 0

    s_down = False
    w_down = False
    
    while True:
        
        count = 0
        mov = 0

        s_down = False
        w_down = False

        while game_state == "MAIN MENU": # the main menu
            clock.tick(FRAMERATE)

            count += 1
            if count >= FRAMERATE:
                count -= FRAMERATE

            junk = random.randint(0, 20)

            ## display

            game_window.fill((255, 255, 255))

            #game_window.blit(logo, (WINDOW_WIDTH // 2 - logo.get_width() // 2, 0))
            #game_window.blit(logotoo, (25, WINDOW_HEIGHT - 20 - logotoo.get_height()))
            
            font = pygame.font.Font(resource_path('Kenney Pixel.ttf'), 120)

            for i in range(len(options)):

                text = font.render(options[i], True, (0, 0, 0))
                game_window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 350 + (i * 90) - text.get_height() // 2))

                #if i == sel:

                    #game_window.blit(marrow, (WINDOW_WIDTH // 2 - text.get_width() // 2 - 15 - marrow.get_width(), 356 + (i * 90) - marrow.get_height() // 2))

                    #game_window.blit(pygame.transform.flip(marrow, True, True), (WINDOW_WIDTH // 2 + text.get_width() // 2 + 15, 356 + (i * 90) - marrow.get_height() // 2))
            
            font = pygame.font.Font(resource_path('Kenney Pixel.ttf'), 80)

            text = font.render((PLAT_VER + " v." + DEV_VER), True, (0, 0, 0))
            game_window.blit(text, (WINDOW_WIDTH - text.get_width() - 10, WINDOW_HEIGHT - text.get_height() - 10))

            window_resize()

            events = global_inputs()
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                                    
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        game_state = options[sel]
                        log(("new game state: " + game_state))

                    if event.key == pygame.K_w and w_down == False:
                        w_down = True
                        mov -= 1
                        count = 15

                    if event.key == pygame.K_s and s_down == False:
                        s_down = True
                        mov += 1
                        count = 15

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_w and w_down == True:
                        w_down = False
                        mov += 1

                    if event.key == pygame.K_s and s_down == True:
                        s_down = False
                        mov -= 1

            if count == 15:
                count = 0
                sel += mov
                if sel < 0:
                    sel = len(options) - 1
                if sel > len(options) - 1:
                    sel = 0         
                        
            await asyncio.sleep(0)
                    
        while game_state == "CREDITS": # game credits

            clock.tick(FRAMERATE)

            game_window.fill((255, 255, 255))
            
            font = pygame.font.Font(resource_path('Kenney Pixel.ttf'), 120)

            text = font.render("CREDITS", True, (0, 0, 0))
            game_window.blit(text, (WINDOW_WIDTH // 2- text.get_width() // 2, 20))

            pygame.draw.rect(game_window, (0, 0, 0), (WINDOW_WIDTH // 2 - text.get_width() // 2 - 5, 20 + text.get_height(), text.get_width() + 10, 20))
            
            font = pygame.font.Font(resource_path('Kenney Pixel.ttf'), 80)

            text = font.render("Programmed by Donian", True, (0, 0, 0))
            game_window.blit(text, (WINDOW_WIDTH // 2- text.get_width() // 2, 150))

            text = font.render("Designed by Donian", True, (0, 0, 0))
            game_window.blit(text, (WINDOW_WIDTH // 2- text.get_width() // 2, 225))

            text = font.render("Artwork from [X]", True, (0, 0, 0))
            game_window.blit(text, (WINDOW_WIDTH // 2- text.get_width() // 2, 300))

            text = font.render("Music / Sound from [X]", True, (0, 0, 0))
            game_window.blit(text, (WINDOW_WIDTH // 2- text.get_width() // 2, 375))

            text = font.render("Fonts from Kenney.nl", True, (0, 0, 0))
            game_window.blit(text, (WINDOW_WIDTH // 2- text.get_width() // 2, 450))

            text = font.render("[Asset links on itch.io]", True, (0, 0, 0))
            game_window.blit(text, (WINDOW_WIDTH // 2- text.get_width() // 2, 600))
     
            window_resize()

            events = global_inputs()
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                                    
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        game_state = "MAIN MENU"
                        log(("new game state: " + game_state))
                        
            await asyncio.sleep(0)
                    
        while game_state == "TUTORIAL": # the tutorial goes here

            clock.tick(FRAMERATE)

            game_window.fill((255, 255, 255))
            
            font = pygame.font.Font(resource_path('Kenney Pixel.ttf'), 120)

            text = font.render("TUTORIAL", True, (0, 0, 0))
            game_window.blit(text, (WINDOW_WIDTH // 2- text.get_width() // 2, 20))

            pygame.draw.rect(game_window, (0, 0, 0), (WINDOW_WIDTH // 2 - text.get_width() // 2 - 5, 20 + text.get_height(), text.get_width() + 10, 20))
            
            font = pygame.font.Font(resource_path('Kenney Pixel.ttf'), 80)

            text = font.render("Press buttons and things occur", True, (0, 0, 0))
            game_window.blit(text, (WINDOW_WIDTH // 2- text.get_width() // 2, 150))
     
            window_resize()

            events = global_inputs()
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                                    
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        game_state = "MAIN MENU"
                        log(("new game state: " + game_state))
                        
            await asyncio.sleep(0)
                    
        while "START" in game_state or game_state == "NEW GAME": # do all pre-game set up here, such as default variable states

            game_state = "MAIN GAME"

        while game_state == "LOAD" or game_state == "LOAD GAME": # do game loading here
            
            game_state = "MAIN GAME"

        while game_state == "MAIN GAME": # the actual gameplay

            clock.tick(FRAMERATE)

            game_window.fill((255, 255, 255))
     
            window_resize()

            events = global_inputs()
            
            for event in events:
                if event.type == pygame.KEYDOWN:
                                    
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        game_state = "MAIN MENU"
                        log(("new game state: " + game_state))
                        
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

import pygame
from  pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

#game window
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define colours
ORANGE = (255, 206, 0)
RED = (212, 43, 43)
WHITE = (246, 235, 235)
BLACK = (0, 0, 0)

# define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# define fighter variables
NINJA1_SIZE = 200
NINJA1_SCALE = 4
NINJA1_OFFSET = [90, 97]
NINJA1_DATA = [NINJA1_SIZE, NINJA1_SCALE, NINJA1_OFFSET]

NINJA2_SIZE = 200
NINJA2_SCALE = 4
NINJA2_OFFSET = [90, 102]
NINJA2_DATA = [NINJA2_SIZE, NINJA2_SCALE, NINJA2_OFFSET]

# load music and sounds
pygame.mixer.music.load("assets/audio/470654__blockfighter298__mean-machine.wav")
pygame.mixer.music.set_volume(0.30)
pygame.mixer.music.play(-1, 0.0, 5000)
katana1_fx = pygame.mixer.Sound("assets/audio/544508__busiuq__swing-the-katana.mp3")
katana1_fx.set_volume(0.75)
katana2_fx = pygame.mixer.Sound("assets/audio/547600__herkules92__sword-attack.wav")
katana2_fx.set_volume(0.15)

# load background
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
fr_image = pygame.image.load("assets/images/background/background-2.png").convert_alpha()

# function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# load sprite sheets
ninja1_sheet = pygame.image.load('assets/images/ninja1/Sprites/ninja1.png').convert_alpha()
ninja2_sheet = pygame.image.load('assets/images/ninja2/Sprites/ninja2.png').convert_alpha()

# load icons
victory_img = pygame.image.load('assets/icons/ko-png-3.png').convert_alpha()

# define number of steps in each animation
NINJA1_ANIMATION_STEPS = [6, 6, 6, 2, 8, 2, 8, 4, 4]
NINJA2_ANIMATION_STEPS = [4, 4, 7, 2, 4, 2, 8, 3]

# define font
counter_font = pygame.font.Font("assets/fonts/Act_Of_Rejection.ttf", 180)
score_font = pygame.font.Font("assets/fonts/Turok.ttf", 50)
score_font_2 = pygame.font.Font("assets/fonts/Turok.ttf", 48)

# draw text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# function for drawing foreground
def draw_fr():
    scaled_fr = pygame.transform.scale(fr_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_fr, (0, 0))

# function for drawing health bars
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x-4, y-4, 408, 58))
    pygame.draw.rect(screen, RED, (x, y, 400, 50))
    pygame.draw.rect(screen, ORANGE, (x, y, 400 * ratio, 50))


# create two instances of fighters
fighter_1 = Fighter(1, 400, 605, False, NINJA1_DATA, ninja1_sheet, NINJA1_ANIMATION_STEPS, katana1_fx)
fighter_2 = Fighter(2, 1100, 605, True, NINJA2_DATA, ninja2_sheet, NINJA2_ANIMATION_STEPS, katana2_fx)

#game loop
run = True
while run:

    clock.tick(FPS)

    # draw background
    draw_bg()

    # health bars
    draw_health_bar(fighter_1.health, 50, 30)
    draw_health_bar(fighter_2.health, 1150, 30)
    draw_text("Player 1: " + str(score[0]), score_font, BLACK, 50, 90)
    draw_text("Player 2: " + str(score[1]), score_font, BLACK, 1310, 90)
    draw_text("Player 1: " + str(score[0]), score_font_2, WHITE, 53, 88)
    draw_text("Player 2: " + str(score[1]), score_font_2, WHITE, 1313, 88)

    # update countdown
    if intro_count <= 0:
        # move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else:
        # display count timer
        draw_text(str(intro_count), counter_font, ORANGE, SCREEN_WIDTH / 2.25, SCREEN_HEIGHT / 2.5)
        # update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()


    # update fighters
    fighter_1.update()
    fighter_2.update()

    # draw figters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    # draw foreground
    draw_fr()

    # check for player defeat
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        # display victory image
        screen.blit(victory_img, (280, 120))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 400, 605, False, NINJA1_DATA, ninja1_sheet, NINJA1_ANIMATION_STEPS, katana1_fx)
            fighter_2 = Fighter(2, 1100, 605, True, NINJA2_DATA, ninja2_sheet, NINJA2_ANIMATION_STEPS, katana2_fx)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # update display
    pygame.display.update()

# exit pygame
pygame.QUIT()
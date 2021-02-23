import pygame
import random
import os
pygame.init()
pygame.mixer.init()

#COLOURS
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
orange = (255, 128, 0)
pink = (255, 50, 150)
green = (0, 255, 0)
blue = (0, 0, 255)

#CREATING WINDOW
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#BACKGROUND IMAGE
bgimg = pygame.image.load("bgimg.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()

wel_img = pygame.image.load("wel_img.jpg")
wel_img = pygame.transform.scale(wel_img, (screen_width, screen_height)).convert_alpha()

#GAME TITLE
pygame.display.set_caption("Naagin")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, green, [x, y, snake_size, snake_size])

#FOR WELCOME SCREEN (it is itself a game(kind of))
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        gameWindow.blit(wel_img, (0, 0))
        text_screen("WELCOME TO NAAGIN GAME", black, 200, 30)
        text_screen("PRESS SPACE BAR TO PLAY", pink, 200, 550)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('bg.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)

#GAME LOOP
def gameloop():
    # GAME SPECIFIC VARIABLE
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    init_velocity = 5
    snake_size = 20
    score_size = 10
    food_x = random.randint(50, screen_width - 100)
    food_y = random.randint(50, screen_height - 100)
    score = 0
    fps = 30

    snk_list = []
    snk_length = 1
# checks if highscore.txt file is present or not, if not then creates one
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        highscore = f.read()
    while not exit_game:
        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            gameWindow.fill(black)
            text_screen("NAAGIN MAR GYI!!", red, 100, 200)
            text_screen("ENTER THOK KE PHIR SE KHEL", orange, 100, 300)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_c: #cheat code
                        score = score + 2

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<15 and abs(snake_y - food_y)<15: #snake kitta pai khayega
                score += 1
                food_x = random.randint(50, screen_width - 100)
                food_y = random.randint(50, screen_height - 100)
                snk_length += 4
                if score>int(highscore):
                    highscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("score: " + str(score) + "  highscore: " + str(highscore), black, 470, 2)
            pygame.draw.rect(gameWindow, blue, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)> snk_length:
                del snk_list[0]

            if snake_x<0 or snake_y<0 or snake_x>screen_width or snake_y>screen_height:
                pygame.mixer.music.load("game_over.mp3")
                pygame.mixer.music.play()
                game_over = True

            if head in snk_list[:-1]: #it means every element except last one for snake overlapping
                pygame.mixer.music.load("game_over.mp3")
                pygame.mixer.music.play()
                game_over = True

            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

welcome()
pygame.quit()
quit()
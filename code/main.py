import random
import pygame
import tkinter
from tkinter import messagebox

WIDTH = 20*20+21
HEIGHT = 20*20+21
CUBE_WIDTH = 20
CUBE_HEIGHT = 20
MOVE = 0
pygame.init()
root = pygame.display.set_mode((WIDTH, HEIGHT))
logo = pygame.image.load('snake.png')
pygame.display.set_icon(logo)
pygame.display.set_caption('Snake by Matan Boas')
font = pygame.font.Font('PressStart2P-Regular.ttf', 14)
text = font.render('SCORE: 0', True, (255,255,255))
textRect = text.get_rect()
SEGEV = pygame.image.load('segev.png').convert_alpha()
JAHNOON = pygame.image.load('jahnoon.png').convert_alpha()

class Snake:

    def __init__(self):
        self.snake_length = 0
        self.cubes = []
        self.new_cubes = []
        self.head_x = 1
        self.head_y = 10
        self.cubes_locetions = []
        self.new_cubes_locetions = []
        while True:
            self.treat_x = random.randint(1, 20)
            self.treat_y = random.randint(1, 20)
            if not (self.treat_x == self.head_x) and not (self.treat_y == self.head_y):
                break
        self.timed_speed_x = 1
        self.timed_speed_y = 0
        self.speed_x = self.timed_speed_x
        self.speed_y = self.timed_speed_y
        self.treat = pygame.Rect((self.treat_x-1)*20+self.treat_x, (self.treat_y-1)*20+self.treat_y, CUBE_WIDTH, CUBE_HEIGHT)
        self.head = pygame.Rect((self.head_x-1)*20+self.head_x, (self.head_y-1)*20+self.head_y, CUBE_WIDTH, CUBE_HEIGHT)

    def speed(self, x, y):
        self.timed_speed_x = x
        self.timed_speed_y = y

    def getScore(self):
        return int(self.snake_length+1)

    def hit(self):
        self.regenarate()
        self.snake_length += 1

    def getSpeed(self):
        return [self.speed_x, self.speed_y]

    def regenarate(self):
        while True:
            self.treat_x = random.randint(1, 20)
            self.treat_y = random.randint(1, 20)

            if not True in [(x_y[0] == self.treat_x) and (x_y[1] == self.treat_y) for x_y in self.cubes_locetions] and not((self.treat_x == self.head_x) and not (self.treat_y == self.head_y)):
                break
        self.treat = pygame.Rect((self.treat_x-1)*20+self.treat_x, (self.treat_y-1)*20+self.treat_y, CUBE_WIDTH, CUBE_HEIGHT)

    def move(self):
        self.speed_x = self.timed_speed_x
        self.speed_y = self.timed_speed_y

        if self.snake_length > 0:
            self.new_cubes.append(pygame.Rect((self.head_x-1)*20+self.head_x, (self.head_y-1)*20+self.head_y, CUBE_WIDTH, CUBE_HEIGHT))
            self.new_cubes_locetions.append([(self.head_x-1)*20+self.head_x, (self.head_y-1)*20+self.head_y])

            for i in range(self.snake_length-1):
                self.new_cubes.append(self.cubes[i])
                self.new_cubes_locetions.append(self.cubes_locetions[i])

            self.treat_now = False

            self.cubes = self.new_cubes
            self.new_cubes = []
            self.cubes_locetions = self.new_cubes_locetions
            self.new_cubes_locetions = []

        self.head_x += self.speed_x
        self.head_y += self.speed_y

    def update_snake(self, to_return = True):
        self.head_x = int(self.head_x)
        self.head_y = int(self.head_y)

        for i in self.cubes_locetions:
            if i == [(self.head_x-1)*20+self.head_x, (self.head_y-1)*20+self.head_y]:
                to_return = False

        if (self.head_x == self.treat_x) and (self.head_y == self.treat_y):
            self.hit()

        if self.head_x > ((WIDTH-21)/20):
            self.head_x -= ((WIDTH-21)/20)

        if self.head_y > ((HEIGHT-21)/20):
            self.head_y -= ((HEIGHT-21)/20)

        if self.head_x < 1:
            self.head_x += ((WIDTH-21)/20)

        if self.head_y < 1:
            self.head_y += ((HEIGHT-21)/20)

        self.head = pygame.Rect((self.head_x-1)*20+self.head_x, (self.head_y-1)*20+self.head_y, CUBE_WIDTH, CUBE_HEIGHT)

        return to_return

retry = True
while retry:

    snake = Snake()
    Clock = pygame.time.Clock()
    run = True
    didnt_die = True

    def Update():
        run = snake.update_snake()
        pygame.display.update()

        return run

    def checkForPresses():
        keys = pygame.key.get_pressed()

        speed = snake.getSpeed()

        if keys[pygame.K_DOWN] and speed[1] != -1:
            snake.speed(0, 1)
        if keys[pygame.K_UP] and speed[1] != 1:
            snake.speed(0, -1)
        if keys[pygame.K_LEFT] and speed[0] != 1:
            snake.speed(-1, 0)
        if keys[pygame.K_RIGHT] and speed[0] != -1:
            snake.speed(1, 0)

    def draw():
        for cube in snake.cubes:
            pygame.draw.rect(root, (221, 221, 221), cube)

        root.blit(JAHNOON, ((snake.treat_x-1)*20+snake.treat_x, (snake.treat_y-1)*20+snake.treat_y))
        root.blit(SEGEV, ((snake.head_x-1)*20+snake.head_x-5, (snake.head_y-1)*20+snake.head_y))

        text = font.render(f'SCORE: {snake.getScore()}', True, (255,255,255))
        root.blit(text, textRect)

    while run and didnt_die:
        Clock.tick(60)
        root.fill((34, 40, 49))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        checkForPresses()

        MOVE += 1
        if MOVE == 12:
            snake.move()
            MOVE = 0

        draw()
        didnt_die = Update()

    if run == False:
        break

    win = tkinter.Tk()
    win.withdraw()
    win.iconbitmap("snake.png")

    MsgBox = messagebox.askquestion ('Retry?',f'Your score is: {snake.getScore()} Do you want to retry?',icon = 'warning')

    if MsgBox != 'yes':
       win.destroy()
       retry = False
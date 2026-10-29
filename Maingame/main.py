import pygame
import gif_pygame
import gif_pygame.transform
import random
from pygame.math import Vector2
import sys

def load_scaled(path):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.smoothscale(image, (cell_size, cell_size))

def load_scaled_gif(path):
    gif = gif_pygame.load(path)
    gif_pygame.transform.scale(gif, (cell_size, cell_size))
    return gif


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.drawfruit()
        self.snake.drawsnake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomise()
            self.snake.addblock()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.next_direction = Vector2(1,0)
        self.new_block = False

        self.head_up = load_scaled_gif("Assets/Snake/headup.gif")
        self.head_down = load_scaled_gif("Assets/Snake/headdown.gif")
        self.head_left = load_scaled_gif("Assets/Snake/headleft.gif")
        self.head_right = load_scaled_gif("Assets/Snake/headright.gif")

        self.tail_up = load_scaled("Assets/Snake/tail up.png")
        self.tail_down = load_scaled("Assets/Snake/tail down.png")
        self.tail_left = load_scaled("Assets/Snake/tail left.png")
        self.tail_right = load_scaled("Assets/Snake/tail right.png")

        self.body_vertical = load_scaled("Assets/Snake/mid vert.png")
        self.body_horizontal = load_scaled("Assets/Snake/mid horiz.png")

        self.body_tr = load_scaled("Assets/Snake/mid tr.png")
        self.body_tl = load_scaled("Assets/Snake/mid tl.png")
        self.body_br = load_scaled("Assets/Snake/mid br.png")
        self.body_bl = load_scaled("Assets/Snake/mid bl.png")

    def drawsnake(self):
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                if self.direction == Vector2(0, -1):
                    currenthead = self.head_up
                elif self.direction == Vector2(0, 1):
                    currenthead = self.head_down
                elif self.direction == Vector2(-1, 0):
                    currenthead = self.head_left
                else:
                    currenthead = self.head_right

                currenthead.render(screen, (x_pos, y_pos))
            elif index == len(self.body) - 1:
                tail_point = self.body[-2] - self.body[-1]
                if tail_point == Vector2(1, 0):
                    screen.blit(self.tail_right, block_rect)
                elif tail_point == Vector2(-1, 0):
                    screen.blit(self.tail_left, block_rect)
                elif tail_point == Vector2(0, 1):
                    screen.blit(self.tail_down, block_rect)
                else:
                    screen.blit(self.tail_up, block_rect)
            else:
                pygame.draw.rect(screen,(0, 128, 34), block_rect)

















        

    def move_snake(self):
        self.direction = self.next_direction

        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def addblock(self):
        self.new_block = True

class FRUIT:
    def __init__(self):
        self.randomise()

    def drawfruit(self):
        fruit_rect = pygame.Rect(
            int(self.pos.x * cell_size),
            int(self.pos.y * cell_size),
            cell_size,
            cell_size
        )
        screen.blit(self.image, fruit_rect)

    def randomise(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)
        self.image = random.choice(fruit_images)

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))
background = pygame.image.load("Assets/checkerboard.png").convert_alpha()
background = pygame.transform.smoothscale(background, (cell_number * cell_size, cell_number * cell_size))

clock = pygame.time.Clock()
fruit_images = []
for image_path in [
    "Assets/apple.png",
    "Assets/pear.png",
    "Assets/lime.png",
    "Assets/banana.png",
    "Assets/orange.png",
]:
    image = pygame.image.load(image_path).convert_alpha()
    image.set_colorkey((255, 255, 255))
    fruit_images.append(pygame.transform.smoothscale(image, (cell_size, cell_size)))

main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                if main_game.snake.direction.y != 1:
                    main_game.snake.next_direction = Vector2(0,-1)
            if event.key == pygame.K_a:
                if main_game.snake.direction.x != 1:
                    main_game.snake.next_direction = Vector2(-1,0)
            if event.key == pygame.K_s:
                if main_game.snake.direction.y != -1:
                    main_game.snake.next_direction = Vector2(0,1)
            if event.key == pygame.K_d:
                if main_game.snake.direction.x != -1:
                    main_game.snake.next_direction = Vector2(1,0)

    screen.blit(background, (0,0))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
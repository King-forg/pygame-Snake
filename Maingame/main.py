import pygame
import gif_pygame
import gif_pygame.transform
import random
from pygame.math import Vector2
import sys

totalassets = 20
loadedassets = 0
score = 0
length = 3


def fpsmonitor():
    if int(clock.get_fps()) > 55:
        fps_text = small_font.render(f"Stable", True, (0, 184, 6))
    else:
        fps_text = small_font.render(f"Unstable", True, (184, 31, 0))
    rect = fps_text.get_rect(bottomright=(screen.get_width() - 10, screen.get_height() - 10))
    screen.blit(fps_text, rect)

def randomdeathmsg():
    rdm = random.randint(1,11)
    if rdm == 1:
        return "Ssssssssssskill\nisssssssssssssue"
    elif rdm == 2:
        return "That better not have\nbeen a wall you went into"
    elif rdm == 3:
        return "Walls arent fruit\ndont forget"
    elif rdm == 4:
        return "The fruit is sentient btw"
    elif rdm == 5:
        return "Cant go phasing through\nwalls here"
    elif rdm == 6:
        return "You are now hissstory"
    elif rdm == 7:
        return "Noodles, no noodles, fruit\nno fruit"
    elif rdm == 8:
        return "The walls have feelings too"
    elif rdm == 9:
        return "You were meant to go the other\nway btw"
    elif rdm == 10:
        return "Slithered right past the fruit salad"
    elif rdm == 11:
        return "PUMPKIN"
    else:
        return "How?????????"
    
def playbutton(death):
    w,h = screen.get_size()
    track = pygame.Rect(0, 0, 300, 8)
    track.center = (w//2,h//2+160)
    slowfps, fastfps = 300, 60
    t = (slowfps - 150) / (slowfps - fastfps)
    dragging = False
    button = pygame.Rect(0,0,200,70)
    button.center = (w//2,h//2+40)
    rdm = randomdeathmsg()
    pygame.mixer.music.play(loops=-1, fade_ms=3000)
    while True:
        mouse = pygame.mouse.get_pos()
        hovered = button.collidepoint(mouse)
        handle_x = track.left + int(t*track.width)
        handle = pygame.Rect(0, 0, 22, 30)
        handle.center = (handle_x, track.centery)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hovered:
                    return int(slowfps - t * (slowfps - fastfps))
                if handle.collidepoint(mouse) or track.inflate(0, 30).collidepoint(mouse):
                    dragging = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return int(slowfps - t * (slowfps - fastfps))
        if dragging:
                t = max(0, min(1, (mouse[0] - track.left) / track.width))
        screen.fill((30,30,30))
        if death == True:
            deathmessage = mid_font.render(rdm, True, (206, 255,145))
            youdied = small_font.render("You Died!", True, (255,67,54))
            screen.blit(deathmessage, deathmessage.get_rect(center=(w//2,100)))
            screen.blit(youdied, youdied.get_rect(center = (w//2,190)))
        title = title_font.render("Snake", True, (206, 255, 145))
        screen.blit(title, title.get_rect(center=(w//2,h//2-70)))
        color = (170,230,90)if hovered else (139,197,68)
        pygame.draw.rect(screen, color, button, border_radius=14)
        label = small_font.render("Play", True, (30, 30, 30))
        screen.blit(label, label.get_rect(center=button.center))
        pygame.draw.rect(screen, (70,70,70), track, border_radius=4)
        filled = pygame.Rect(track.left, track.top, int(t*track.width), track.height)
        pygame.draw.rect(screen, (139,197,68), filled, border_radius=4)
        pygame.draw.rect(screen, (206,255,145), handle, border_radius=8)
        speed_label = small_font.render(f"Speed: {int(t*9) + 1}", True, (200,200,200))
        screen.blit(speed_label, speed_label.get_rect(center=(w//2, track.centery - 35)))
        pygame.display.update()
        clock.tick(60)

def loadingstep(label="Loading..."):
    global loadedassets
    loadedassets += 1
    draw_loading(label)

def scoreprint(Types):
    global score, length
    if Types == "Score":
        score += 1
        length = score + 3

def draw_loading(label="Loading..."):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((30,30,30))
    w, h = screen.get_size()

    title = title_font.render("SNAKE", True, (206, 255, 145))
    screen.blit(title, title.get_rect(center=(w//2, h//2-70)))

    bar_w, bar_h = 400, 24
    bar_x, bar_y = w//2-bar_w//2, h//2
    pygame.draw.rect(screen, (70, 70, 70), (bar_x, bar_y, bar_w, bar_h), border_radius=12)
    fill = int(bar_w * min(loadedassets / totalassets, 1))
    if fill > 0:
        pygame.draw.rect(screen, (139,197,68), (bar_x, bar_y, fill, bar_h), border_radius=12)

    text = small_font.render(label, True, (200,200,200))
    screen.blit(text, text.get_rect(center=(w//2, bar_y+55)))

    pygame.display.update()

def load_scaled(path):
    image = pygame.image.load(path).convert_alpha()
    image = pygame.transform.scale(image, (cell_size, cell_size))
    body_color = (139, 197, 68)
    for x in range(cell_size):
        for y in range(cell_size):
            pixel = image.get_at((x, y))
            if pixel.a < 255:
                image.set_at((x, y), (*body_color, pixel.a))
    loadingstep("Loading snake...")
    return image

def load_scaled_gif(path):
    gif = gif_pygame.load(path)
    gif_pygame.transform.scale(gif, (cell_size, cell_size))
    loadingstep("Loading snake...")
    return gif

class TEXT:
    def __init__(self):
        global score
        

    def textadd(self):
        self.scoretext = mid_font.render(f"Score: {score}", True, (0,176,135))
        screen.blit(self.scoretext, self.scoretext.get_rect(midleft=(50,850)))

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.fruit.randomise(self.snake.body)
        self.text = TEXT()

        pygame.mixer.music.load("Assets/audio/music.mp3")
        pygame.mixer.music.set_volume(0.4)

        self.chomp = pygame.mixer.Sound("Assets/audio/chomp.mp3")
        self.chomp.set_volume(0.4)

        self.ping = pygame.mixer.Sound("Assets/audio/ping.mp3")
        self.ping.set_volume(0.4)

        self.hiss = pygame.mixer.Sound("Assets/audio/hiss.mp3")
        self.hiss.set_volume(0.2)

        self.slchannel = pygame.mixer.Channel(1)

    def update(self):
        self.snake.move_snake()
        if random.random() < 0.08 and not self.slchannel.get_busy():
            self.slchannel.play(self.hiss)
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.fruit.drawfruit()
        self.snake.drawsnake()
        self.text.textadd()

    def check_collision(self):
        global score
        if self.fruit.pos == self.snake.body[0]:
            if (score+1) % 10 == 0 and score > 0:
                self.ping.play()
            else:
                self.chomp.play()
            self.fruit.randomise(self.snake.body)
            scoreprint("Score")
            self.snake.addblock()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.mixer.music.fadeout(1000)
        global score, length
        pygame.time.set_timer(SCREEN_UPDATE, 0)
        score = 0
        length = 3
        self.snake.reset()
        self.fruit.randomise(self.snake.body)
        ms = playbutton(True)
        pygame.event.clear()
        pygame.time.set_timer(SCREEN_UPDATE, ms)

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
                behind = self.body[index + 1] - block
                ahead = self.body[index - 1] - block

                if behind.x == ahead.x:
                    screen.blit(self.body_vertical, block_rect)
                elif behind.y == ahead.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    corner = behind + ahead
                    if corner == Vector2(-1, -1):
                        screen.blit(self.body_tl, block_rect)
                    elif corner == Vector2(1, -1):
                        screen.blit(self.body_tr, block_rect)
                    elif corner == Vector2(-1, 1):
                        screen.blit(self.body_bl, block_rect)
                    else:
                        screen.blit(self.body_br, block_rect)

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

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.next_direction = Vector2(1,0)
        self.new_block = False

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

    def randomise(self, snake_body=()):
        while True:
            self.x = random.randint(0,cell_number - 1)
            self.y = random.randint(0,cell_number - 1)
            self.pos = Vector2(self.x,self.y)
            if self.pos not in snake_body:
                break
        self.image = random.choice(fruit_images)

pygame.mixer.pre_init(44100, -16, 2 ,512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size+100))
pygame.display.set_caption("Snake")

title_font = pygame.font.Font("Assets/Audex-Regular.ttf", 90)
mid_font = pygame.font.Font("Assets/Audex-Regular.ttf", 40)
small_font = pygame.font.Font("Assets/Audex-Regular.ttf", 30)
draw_loading("Starting up...")

background = pygame.image.load("Assets/checkerboard.png").convert_alpha()
background = pygame.transform.smoothscale(background, (cell_number * cell_size, cell_number * cell_size))
loadingstep("Loading background...")

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
    loadingstep("Loading fruit...")

main_game = MAIN()

tick_ms = playbutton(False)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, tick_ms)

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
    screen.fill((194, 100, 0))
    screen.blit(background, (0,0))
    main_game.draw_elements()
    fpsmonitor()
    pygame.display.update()
    clock.tick(60)
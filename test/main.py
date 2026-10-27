import pygame


pygame.init()

sound = pygame.mixer.Sound("Assets/Sounds/yoshi's-island---athletic-theme-made-with-Voicemod.mp3")

sfx = pygame.mixer.Sound("Assets/Sounds/master_of_dreams_wooshes_sub_7_994.mp3")

sound.play(-1)

screen = pygame.display.set_mode((640, 640))

potato_img = pygame.image.load("Assets/Images/Potato_JE3_BE2.png").convert()

potato_img = pygame.transform.scale(potato_img,
                                    (potato_img.get_width() / 2,
                                     potato_img.get_height() / 2))

potato_img.set_colorkey((0,0,0))

font = pygame.font.Font(None,size=30)

running = True

x = 0
clock = pygame.time.Clock()

delta_time = 0.1

right = False
left = False

while running:
    screen.fill((255, 255, 255))

    screen.blit(potato_img, (x, 30))

    hitbox = pygame.Rect(x, 30, potato_img.get_width(), potato_img.get_height())

    mpos = pygame.mouse.get_pos()

    target = pygame.Rect(300, 0, 160, 280)
    collision = hitbox.colliderect(target)
    m_collision = target.collidepoint(mpos)
    pygame.draw.rect(screen, (255 * collision,255 * m_collision,0), target)
    
    if right:
        x += 50 * delta_time
    if left:
        x -= 50 * delta_time

    text = font.render("Hello World!", True, (0,0,0))
    screen.blit(text, (x, 30))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_f:
                sfx.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                right = False
            if event.key == pygame.K_a:
                left = False

    pygame.display.flip()

    delta_time = clock.tick(60) / 1000
    delta_time = max(0.001, min(0.1, delta_time))

pygame.quit()
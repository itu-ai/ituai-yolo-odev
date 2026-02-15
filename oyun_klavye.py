import pygame
import random

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
PLAYER_SPEED = 5
ENEMY_SPEED = 3
SPAWN_INTERVAL = 45

DARK_BG = (30, 30, 40)
BLUE    = (52, 152, 219)
RED     = (231, 76, 60)
WHITE   = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge the Blocks!")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

player = pygame.Rect(275, 360, 50, 30)
enemies = []
score = 0
spawn_timer = 0
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #klavye kontrolü
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player.x += PLAYER_SPEED

    if player.x < 0:
        player.x = 0
    if player.x > SCREEN_WIDTH - player.width:
        player.x = SCREEN_WIDTH - player.width

    spawn_timer += 1
    if spawn_timer > SPAWN_INTERVAL:
        spawn_timer = 0
        enemies.append(pygame.Rect(random.randint(0, SCREEN_WIDTH - 40), -40, 40, 40))

    for enemy in enemies:
        enemy.y += ENEMY_SPEED
    enemies = [e for e in enemies if e.y < SCREEN_HEIGHT]

    for enemy in enemies:
        if player.colliderect(enemy):
            print(f"Game Over! Score: {score}")
            running = False

    score += 1

    screen.fill(DARK_BG)
    pygame.draw.rect(screen, BLUE, player)
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

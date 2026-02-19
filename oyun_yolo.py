import pygame
import random

import cv2
from ultralytics import YOLO

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
PLAYER_SPEED = 5
ENEMY_SPEED = 3
SPAWN_INTERVAL = 45

DARK_BG = (30, 30, 40)
BLUE = (52, 152, 219)
RED = (231, 76, 60)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge the Blocks!")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

model = YOLO("yolov8n-pose.pt")
camera = cv2.VideoCapture(0)

player = pygame.Rect(275, 360, 50, 30)
enemies = []
score = 0
spawn_timer = 0
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # kafa kontrolü
    ok, frame = camera.read()
    frame = cv2.flip(frame, 1)
    results = model(frame, verbose=False)

    if results and results[0].keypoints is not None:
        keypoints = results[0].keypoints.data[0]
        left_eye = keypoints[1]
        right_eye = keypoints[2]
        y_difference = left_eye[1] - right_eye[1]

        if y_difference > 0:
            player.x += PLAYER_SPEED
        else:
            player.x -= PLAYER_SPEED

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

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    preview = cv2.resize(frame_rgb, (160, 120))
    cam_surface = pygame.surfarray.make_surface(preview.swapaxes(0, 1))
    screen.blit(cam_surface, (430, 10))

    pygame.display.flip()
    clock.tick(30)


pygame.quit()

import pygame
import math
import pickle
from network import client

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Game")

# Constants
BLUE = (0, 0, 255)
BULLET_COLOR = (255, 255, 0)
FPS = 60
SPEED = 3
ROT_SPEED = 3
BULLET_SPEED = 8
BLUE_X = 400
BLUE_Y = 300
ANGLE = 0

# Fonts
font = pygame.font.SysFont("Arial", 36)
clock = pygame.time.Clock()

bullets = []

# Server check (optional, unchanged)
SERVER_MESSAGE = {"message": "server-check"}
try:
    client.send(pickle.dumps(SERVER_MESSAGE))
    client.settimeout(1)
    response_bytes = client.recv(1024)
    response = response_bytes.decode("utf-8")
    print(response)
except (BlockingIOError):
    response = "No response from server"
finally:
    client.setblocking(False)

# ------------------------
# MAIN GAME LOOP
# ------------------------
running = True
while running:
    # --- HANDLE EVENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle single-shot left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Spawn bullet slightly in front of circle
            rad = math.radians(ANGLE)
            offset = 50  # how far from center bullet spawns
            bullet_x = BLUE_X + math.cos(rad) * offset
            bullet_y = BLUE_Y - math.sin(rad) * offset
            bullets.append({"x": bullet_x, "y": bullet_y, "angle": ANGLE})

    # --- HANDLE KEYBOARD INPUT (separate from events) ---
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        ANGLE += ROT_SPEED
    if keys[pygame.K_d]:
        ANGLE -= ROT_SPEED

    rad = math.radians(ANGLE)
    if keys[pygame.K_w]:
        BLUE_X += math.cos(rad) * SPEED
        BLUE_Y -= math.sin(rad) * SPEED
    if keys[pygame.K_s]:
        BLUE_X -= math.cos(rad) * SPEED
        BLUE_Y += math.sin(rad) * SPEED

    # --- UPDATE BULLETS ---
    for bullet in bullets:
        b_rad = math.radians(bullet["angle"])
        bullet["x"] += math.cos(b_rad) * BULLET_SPEED
        bullet["y"] -= math.sin(b_rad) * BULLET_SPEED

    bullets = [
        b for b in bullets
        if 0 <= b["x"] <= 800 and 0 <= b["y"] <= 600
    ]

    # --- DRAW EVERYTHING ---
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, BLUE, (int(BLUE_X), int(BLUE_Y)), 50)

    # Facing line
    line_length = 70
    end_x = BLUE_X + math.cos(rad) * line_length
    end_y = BLUE_Y - math.sin(rad) * line_length
    pygame.draw.line(screen, (255, 255, 255), (BLUE_X, BLUE_Y), (end_x, end_y), 3)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.circle(screen, BULLET_COLOR, (int(bullet["x"]), int(bullet["y"])), 8)

    text_surface2 = font.render("WASD to move, Left Click to shoot", True, (255, 0, 0))
    screen.blit(text_surface2, (80, 50))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

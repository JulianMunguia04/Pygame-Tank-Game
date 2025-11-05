import pygame
import math
import pickle
from network import client

WIDTH = 800
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Controller")

# Constants
FPS = 60
SPEED = 3
ROT_SPEED = 3
BULLET_SPEED = 8
BULLET_COLOR = (255, 255, 0)

# --- NEW: Target setup ---
TARGET_X = 100
TARGET_Y = 100
TARGET_RADIUS = 40
TARGET_COLOR = (255, 0, 0)

# Tank
TANK_X = 400
TANK_Y = 300
TANK_ANGLE = 0  # rotation of body
TURRET_ANGLE = 0  # rotation of head (follows mouse)

# Load images
TANK_BODY = pygame.image.load("assets/images/tank-body.png").convert_alpha()
TANK_HEAD = pygame.image.load("assets/images/tank-head.png").convert_alpha()
TANK_HEAD = pygame.transform.flip(TANK_HEAD, True, False)

# Fonts and clock
font = pygame.font.SysFont("Arial", 24)
clock = pygame.time.Clock()

bullets = []

# Optional server check
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Shoot bullet
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            rad = math.radians(TURRET_ANGLE)
            offset = 225
            bullet_x = TANK_X + math.cos(rad) * offset
            bullet_y = TANK_Y - math.sin(rad) * offset
            bullets.append({"x": bullet_x, "y": bullet_y, "angle": TURRET_ANGLE})

    # --- HANDLE INPUT ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        TANK_ANGLE += ROT_SPEED
    if keys[pygame.K_d]:
        TANK_ANGLE -= ROT_SPEED

    rad = math.radians(TANK_ANGLE)
    if keys[pygame.K_w]:
        new_x = TANK_X + math.cos(rad) * SPEED
        new_y = TANK_Y - math.sin(rad) * SPEED
        if 0 < new_x < WIDTH and 0 < new_y < HEIGHT:
            TANK_X, TANK_Y = new_x, new_y

    if keys[pygame.K_s]:
        new_x = TANK_X - math.cos(rad) * SPEED
        new_y = TANK_Y + math.sin(rad) * SPEED
        if 0 < new_x < WIDTH and 0 < new_y < HEIGHT:
            TANK_X, TANK_Y = new_x, new_y

    # --- UPDATE TURRET ANGLE (toward mouse) ---
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - TANK_X
    dy = TANK_Y - mouse_y  # y inverted because screen y increases downward
    TURRET_ANGLE = math.degrees(math.atan2(dy, dx))

    # --- UPDATE BULLETS ---
    for bullet in bullets:
        b_rad = math.radians(bullet["angle"])
        bullet["x"] += math.cos(b_rad) * BULLET_SPEED
        bullet["y"] -= math.sin(b_rad) * BULLET_SPEED

    bullets = [
        b for b in bullets
        if 0 <= b["x"] <= 800 and 0 <= b["y"] <= 600
    ]

     #Check bullet collisions with target
    for bullet in bullets:
        dx = bullet["x"] - TARGET_X
        dy = bullet["y"] - TARGET_Y
        distance = math.hypot(dx, dy)
        if distance < TARGET_RADIUS + 6:
            print("💥 Target hit!")
            bullets.remove(bullet)
            break

    # --- DRAW EVERYTHING ---
    screen.fill((255, 255, 255))

    #Draw Target
    pygame.draw.circle(screen, TARGET_COLOR, (TARGET_X, TARGET_Y), TARGET_RADIUS)

    # Draw tank body
    body_rot = pygame.transform.rotate(TANK_BODY, TANK_ANGLE)
    body_rect = body_rot.get_rect(center=(TANK_X, TANK_Y))
    screen.blit(body_rot, body_rect)

    # Draw turret
    turret_rot = pygame.transform.rotate(TANK_HEAD, TURRET_ANGLE)
    turret_rect = turret_rot.get_rect(center=(TANK_X, TANK_Y))
    screen.blit(turret_rot, turret_rect)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.circle(screen, BULLET_COLOR, (int(bullet["x"]), int(bullet["y"])), 6)

    # Instruction text
    text_surface = font.render("W/S move, A/D rotate body, Mouse aims, LMB fires", True, (255, 0, 0))
    screen.blit(text_surface, (50, 50))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

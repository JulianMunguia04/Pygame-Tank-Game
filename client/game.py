import pygame
import pickle
import math
from network import client

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Game")

# Constants
BLUE = (0, 0, 255)
FPS = 60
BLUE_X = 0
BLUE_Y = 0

# Fonts
font = pygame.font.SysFont("Arial", 36)
clock = pygame.time.Clock()

# ------------------------
# ONE-TIME SERVER CHECK
# ------------------------
SERVER_MESSAGE = {"message": "server-check"}
try:
    client.send(pickle.dumps(SERVER_MESSAGE))  # send once

    # Try to receive server response (blocking briefly)
    client.settimeout(1)  # wait up to 1 second
    response_bytes = client.recv(1024)
    response = response_bytes.decode("utf-8")
    print(response)
except (BlockingIOError):
    response = "No response from server"
finally:
    client.setblocking(False)  # back to non-blocking for game loop

# ------------------------
# MAIN GAME LOOP
# ------------------------
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Move circle
    # Compute direction vector
    dx = mouse_x - BLUE_X
    dy = mouse_y - BLUE_Y

    # Compute distance (so we can normalize)
    distance = math.hypot(dx, dy)

    # Only move if we're not already exactly on the mouse
    if distance > 1:
        # Normalize (make vector length = 1)
        dx /= distance
        dy /= distance

        # Move toward mouse
        BLUE_X += dx * 3
        BLUE_Y += dy * 3

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        print("Holding A")

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, BLUE, (BLUE_X, BLUE_Y), 50)

    # Static text
    text_surface2 = font.render("Hello, Pygame!", True, (255, 0, 0))
    screen.blit(text_surface2, (100, 50))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

import pygame
import pickle
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

    # Move circle
    BLUE_X += 1
    BLUE_Y += 1

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, BLUE, (BLUE_X, BLUE_Y), 50)

    # Static text
    text_surface2 = font.render("Hello, Pygame!", True, (255, 0, 0))
    screen.blit(text_surface2, (100, 50))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

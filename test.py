
import pygame, sys

pygame.init()
# Create the window, saving it to a variable.
surface = pygame.display.set_mode((800, 450), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Example resizable window")

while True:
    surface.fill((255,255,255))

    # Draw a red rectangle that resizes with the window.
    pygame.draw.rect(surface, (255, 150, 150), (1, 1, 5, 5))
    
    surface.blit(pygame.image.load("player.png"), (4,4))

    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


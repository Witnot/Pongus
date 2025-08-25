import pygame

BRICK_WIDTH = 20
BRICK_HEIGHT = 40
BRICK_COLOR = (200, 50, 50)

class Brick:
    def __init__(self, x, y, hits=1, indestructible=False):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.hits = hits
        self.indestructible = indestructible
        self.alive = True

    def hit(self):
        if self.indestructible:
            return
        self.hits -= 1
        if self.hits <= 0:
            self.alive = False

    def draw(self, screen):
        if not self.alive:
            return
        if self.indestructible:
            color = (50, 50, 50)  # wall
        elif self.hits == 2:
            color = (200, 100, 100)  # strong brick
        else:
            color = (200, 200, 200)  # normal
        pygame.draw.rect(screen, color, self.rect)





import random



# Progressive levels
LEVELS = []
for level in range(1, 11):  # Levels 1-10
    bricks = []
    cols = min(level, 5)  # max 5 columns
    rows = 10 + level      # rows grow with level

    for c in range(cols):
        x = 700 - (c * (BRICK_WIDTH + 5))  # push left each column
        for r in range(rows):
            y = r * BRICK_HEIGHT
            if y + BRICK_HEIGHT < 600:  # stay inside screen height
                bricks.append((x, y))

    LEVELS.append(bricks)


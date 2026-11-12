
import pygame
import random
import math

WIDTH = 800
HEIGHT = 600
pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virus Simulation")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (50, 130, 255)
RED = (255, 50, 50)


class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def move(self, vector):
        self.x += vector.h
        self.y += vector.v


class Vector:
    def __init__(self, h, v):
        self.h = float(h)
        self.v = float(v)

    def add(self, otherVector):
        return Vector(self.h + otherVector.h,
                      self.v + otherVector.v)

    def divide(self, scalar):
        if scalar != 0:
            self.h /= scalar
            self.v /= scalar


class Cell:
    def __init__(self, x, y, infected=False):
        self.position = Point(x, y)
        self.velocity = Vector(
            random.uniform(-2, 2),
            random.uniform(-2, 2)
        )
        self.radius = 8
        self.infected = infected

    def move(self):
        self.position.move(self.velocity)

        if self.position.x <= self.radius or self.position.x >= WIDTH - self.radius:
            self.velocity.h *= -1

        if self.position.y <= self.radius or self.position.y >= HEIGHT - self.radius:
            self.velocity.v *= -1

    def draw(self):
        color = RED if self.infected else BLUE
        pygame.draw.circle(
            screen,
            color,
            (int(self.position.x), int(self.position.y)),
            self.radius
        )


cells = []

for i in range(50):
    x = random.randint(20, WIDTH - 20)
    y = random.randint(20, HEIGHT - 20)
    cells.append(Cell(x, y, i == 0))


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    for cell in cells:
        cell.move()

    for i in range(len(cells)):
        for j in range(i + 1, len(cells)):
            cell1 = cells[i]
            cell2 = cells[j]

            dx = cell1.position.x - cell2.position.x
            dy = cell1.position.y - cell2.position.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance <= cell1.radius + cell2.radius:
                if cell1.infected:
                    cell2.infected = True

                if cell2.infected:
                    cell1.infected = True

    for cell in cells:
        cell.draw()

    infected_count = sum(cell.infected for cell in cells)

    font = pygame.font.SysFont(None, 28)
    text = font.render(
        f"Infected: {infected_count}/50",
        True,
        (0, 0, 0)
    )
    screen.blit(text, (15, 15))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

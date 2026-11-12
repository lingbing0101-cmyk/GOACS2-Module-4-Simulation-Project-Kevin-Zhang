import random
import math

WIDTH = 800
HEIGHT = 600
TITLE = "Simulation 3"
RADIUS = 7
CELL_COUNT = 50


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, vector):
        self.x += vector.dx
        self.y += vector.dy


class Vector:
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy


class Cell:
    def __init__(self, x, y, infected=False):
        self.position = Point(x, y)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1.5, 3)

        self.velocity = Vector(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        )

        self.infected = infected

    def move(self):
        speed_multiplier = 1.8 if self.infected else 1

        self.position.move(
            Vector(
                self.velocity.dx * speed_multiplier,
                self.velocity.dy * speed_multiplier
            )
        )

        if self.position.x <= RADIUS or self.position.x >= WIDTH - RADIUS:
            self.velocity.dx *= -1

        if self.position.y <= RADIUS or self.position.y >= HEIGHT - RADIUS:
            self.velocity.dy *= -1


def create_cells():
    return [
        Cell(
            random.randint(20, WIDTH - 20),
            random.randint(20, HEIGHT - 20),
            i == 0
        )
        for i in range(CELL_COUNT)
    ]


cells = create_cells()
frame_count = 0
trial_count = 0

open("sim3_data.txt", "w").close()


def update():
    global cells, frame_count, trial_count

    if trial_count >= 100:
        return

    for _ in range(4):
        for cell in cells:
            cell.move()

        for i in range(len(cells)):
            for j in range(i + 1, len(cells)):
                a = cells[i]
                b = cells[j]

                dx = a.position.x - b.position.x
                dy = a.position.y - b.position.y

                if dx ** 2 + dy ** 2 <= (RADIUS * 2) ** 2:
                    if a.infected:
                        b.infected = True
                    if b.infected:
                        a.infected = True

        frame_count += 1

        if all(cell.infected for cell in cells):
            with open("sim3_data.txt", "a") as f:
                f.write(str(round(frame_count / 60, 4)) + "\n")

            trial_count += 1
            cells = create_cells()
            frame_count = 0
            break


def draw():
    screen.fill("white")

    for cell in cells:
        color = "red" if cell.infected else "blue"
        screen.draw.filled_circle(
            (cell.position.x, cell.position.y),
            RADIUS,
            color
        )

    infected = sum(cell.infected for cell in cells)

    screen.draw.text(
        f"Infected: {infected}/50",
        (15, 15),
        color="black",
        fontsize=25
    )

    screen.draw.text(
        f"Trials: {trial_count}/100",
        (15, 45),
        color="black",
        fontsize=25
    )

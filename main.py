
import os
import pygame as pg
from random import randint, uniform
from math import sqrt

os.environ['SDL_VIDEO_CENTERED'] = '1'
RES = WIDTH, HEIGHT = 1920, 1080

FPS = 60
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
velocity = 0.8
max_distance = 200

pg.init()
screen = pg.display.set_mode(RES)
clock = pg.time.Clock()


class Circle:
    def __init__(self, quantity):
        self.quantity = quantity
        self.circles = []
        self.velocity = [velocity, velocity]
        self.create_circles()

    def create_circles(self):
        for _ in range(self.quantity):
            self.x = randint(0, WIDTH)
            self.y = randint(0, HEIGHT)
            self.velocity_x = uniform(-self.velocity[0], self.velocity[0])
            self.velocity_y = uniform(-self.velocity[1], self.velocity[1])
            self.position = (self.x, self.y, self.velocity_x, self.velocity_y)
            self.circles.append(self.position)

    def update(self):
        self.circles_moved = []

        for i in self.circles:
            self.x = i[0]
            self.y = i[1]

            self.velocity_x = i[2]
            self.velocity_y = i[3]

            self.x += self.velocity_x
            self.y += self.velocity_y

            if self.x >= WIDTH or self.x <= 0:
                self.velocity_x *= -1

            if self.y >= HEIGHT or self.y <= 0:
                self.velocity_y *= -1

            self.position = (self.x, self.y, self.velocity_x, self.velocity_y)
            self.circles_moved.append(self.position)
            self.circles = self.circles_moved

    def connect_circles(self):
        self.lines = []
        for p0 in range(self.quantity - 1):
            for p1 in range(p0 + 1, self.quantity):
                self.lines.append([self.circles[p0][:2], self.circles[p1][:2]])

        return self.lines


def color(distance, max_distance):
    x = int((max_distance - distance) * 255 / max_distance)
    return x, 0, 0


circles = Circle(100)


def main():
    running = True
    while running:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False

        screen.fill(BLACK)

        # Draw lines
        for i in circles.connect_circles():
            start_position = i[0]
            end_position = i[1]
            distance = sqrt((start_position[0] - end_position[0]) ** 2 + (start_position[1] - end_position[1]) ** 2)

            if distance < max_distance:
                pg.draw.line(screen, color(distance, max_distance), start_pos=i[0], end_pos=i[1], width=2)

        # Draw circles
        for i in circles.circles:
           pg.draw.circle(screen, RED, center=i[:2], radius=2)
          #pg.draw.circle(screen, BLUE, center=i[:2], radius=2)


        circles.update()

        pg.display.update()


if __name__ == "__main__":
    main()
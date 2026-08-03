import cv2
import random


class Particle:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)

        self.size = 2

        self.max_size = random.randint(8, 16)

        self.life = 40

        self.color = (
            random.randint(180,255),
            random.randint(180,255),
            random.randint(180,255)
        )


    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.size += 0.3

        self.life -= 1


    def draw(self, frame):

        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            int(self.size),
            self.color,
            -1
        )


    @property
    def finished(self):

        return self.life <= 0
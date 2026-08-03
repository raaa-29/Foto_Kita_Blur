import cv2

class EnergyRing:

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.radius = 10
        self.max_radius = 180

        self.thickness = 4

        self.finished = False

    def update(self):

        self.radius += 8

        if self.radius >= self.max_radius:
            self.finished = True

    def draw(self, frame):

        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            int(self.radius),
            (255, 255, 255),
            self.thickness
        )
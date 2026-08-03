import cv2
from particles import Particle


# ======================================
# Base Animation
# ======================================

class Animation:

    def update(self):
        pass

    def draw(self, frame):
        pass

    @property
    def finished(self):
        return False


# ======================================
# Energy Ring
# ======================================

class EnergyRing(Animation):

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.radius = 10
        self.max_radius = 180

        self.thickness = 4

        self._finished = False

    def update(self):

        self.radius += 8

        if self.radius >= self.max_radius:
            self._finished = True

    def draw(self, frame):

        cv2.circle(
            frame,
            (int(self.x), int(self.y)),
            int(self.radius),
            (255, 255, 255),
            self.thickness
        )

    @property
    def finished(self):
        return self._finished


# ======================================
# Particle Explosion
# ======================================

class ParticleExplosion(Animation):

    def __init__(self, x, y):

        self.particles = []

        for _ in range(30):
            self.particles.append(
                Particle(x, y)
            )

    def update(self):

        for particle in self.particles:
            particle.update()

        self.particles = [
            p for p in self.particles
            if not p.finished
        ]

    def draw(self, frame):

        for particle in self.particles:
            particle.draw(frame)

    @property
    def finished(self):
        return len(self.particles) == 0


# ======================================
# Animation Manager
# ======================================

class AnimationManager:

    def __init__(self):

        self.animations = []

    def add(self, animation):

        self.animations.append(animation)

    def update(self):

        for animation in self.animations:
            animation.update()

        self.animations = [
            a for a in self.animations
            if not a.finished
        ]

    def draw(self, frame):

        for animation in self.animations:
            animation.draw(frame)
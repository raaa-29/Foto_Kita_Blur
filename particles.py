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
            random.randint(180, 255),
            random.randint(180, 255),
            random.randint(180, 255)
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


class SakuraParticle:
    def __init__(self, x, y):
        # Offset acak kecil agar bunga tidak keluar persis di 1 titik
        self.x = x + random.uniform(-10, 10)
        self.y = y + random.uniform(-10, 10)

        # Kecepatan melayang halus
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)

        # Animasi Ukuran (Mekar: Kecil -> Besar)
        self.size = 2.0
        self.max_size = random.uniform(12, 22)
        self.grow_rate = 0.8

        # Fade Out / Life
        self.life = 1.0        # Opacity 100%
        self.fade_rate = 0.02  # Kecepatan memudar

        # Warna Sakura (BGR di OpenCV: Pink Khas)
        self.color = (
            random.randint(180, 210),  # B
            random.randint(180, 200),  # G
            random.randint(230, 255)   # R
        )

    def update(self):
        # Gerakan melayang
        self.x += self.vx
        self.y += self.vy

        # Efek Mekar (Kecil -> Besar)
        if self.size < self.max_size:
            self.size += self.grow_rate

        # Memudar
        self.life -= self.fade_rate

    def draw(self, frame):
        if self.life <= 0:
            return

        # Render Bunga Sederhana menggunakan Overlay (Transparan)
        overlay = frame.copy()

        cv2.circle(
            overlay,
            (int(self.x), int(self.y)),
            int(self.size),
            self.color,
            -1
        )

        alpha = max(0, self.life)
        cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    @property
    def finished(self):
        return self.life <= 0
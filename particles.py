import cv2
import random
import os

# ======================================
# Safe Image Loading for sakura.png
# ======================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(BASE_DIR, "sakura.png")

# Load gambar PNG lengkap dengan Alpha Channel (-1 / IMREAD_UNCHANGED)
SAKURA_IMG = cv2.imread(IMG_PATH, cv2.IMREAD_UNCHANGED)

if SAKURA_IMG is not None:
    print("✅ Berhasil memuat gambar sakura.png!")
else:
    print("⚠️ File sakura.png tidak ditemukan! Pastikan nama & lokasinya benar.")


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
        self.x = x + random.uniform(-4, 4)
        self.y = y + random.uniform(-4, 4)

        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, 0.5)

        self.size = 6.0
        self.max_size = random.uniform(24, 38)
        self.grow_rate = 1.6

        self.angle = random.uniform(0, 360)
        self.rot_speed = random.uniform(-2.0, 2.0)

        self.life = 1.0
        self.fade_rate = 0.025

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.angle += self.rot_speed

        if self.size < self.max_size:
            self.size += self.grow_rate

        self.life -= self.fade_rate

    def draw(self, frame):
        if self.life <= 0 or SAKURA_IMG is None:
            return

        size = int(self.size)
        if size < 4:
            return

        # Resize & Rotasi
        resized = cv2.resize(SAKURA_IMG, (size, size), interpolation=cv2.INTER_AREA)
        M = cv2.getRotationMatrix2D((size // 2, size // 2), self.angle, 1.0)
        rotated = cv2.warpAffine(
            resized, M, (size, size), 
            flags=cv2.INTER_LINEAR, 
            borderMode=cv2.BORDER_CONSTANT, 
            borderValue=(0, 0, 0, 0)
        )

        # Hitung Bounding Box
        x1 = int(self.x - size // 2)
        y1 = int(self.y - size // 2)
        x2 = x1 + size
        y2 = y1 + size

        h, w, _ = frame.shape

        # SAFE CROPPING (Agar bunga di pinggir layar tidak hilang secara tiba-tiba)
        x1_clamped = max(0, x1)
        y1_clamped = max(0, y1)
        x2_clamped = min(w, x2)
        y2_clamped = min(h, y2)

        if x1_clamped >= x2_clamped or y1_clamped >= y2_clamped:
            return

        # Potong area gambar yang masuk dalam frame saja
        sprite_crop = rotated[
            (y1_clamped - y1):(y2_clamped - y1),
            (x1_clamped - x1):(x2_clamped - x1)
        ]

        if sprite_crop.shape[2] == 4:
            sprite_bgr = sprite_crop[:, :, :3]
            sprite_alpha = (sprite_crop[:, :, 3] / 255.0) * max(0.0, self.life)

            roi = frame[y1_clamped:y2_clamped, x1_clamped:x2_clamped]

            for c in range(3):
                roi[:, :, c] = (sprite_alpha * sprite_bgr[:, :, c] + (1.0 - sprite_alpha) * roi[:, :, c])

    @property
    def finished(self):
        return self.life <= 0
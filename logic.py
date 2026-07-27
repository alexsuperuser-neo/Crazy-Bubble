import math
import random

# Яркие цвета для "crazy" эффекта при касании правой стенки
BRIGHT_COLORS = [
    (255, 0, 0),       # Красный
    (0, 255, 0),       # Зелёный
    (0, 0, 255),       # Синий
    (255, 255, 0),     # Жёлтый
    (255, 0, 255),     # Пурпурный
    (0, 255, 255),     # Голубой
    (255, 165, 0),     # Оранжевый
    (128, 0, 128),     # Фиолетовый
    (255, 69, 0),      # Красно-оранжевый
    (0, 255, 127),     # Весенне-зелёный
    (75, 0, 130),      # Индиго
    (255, 20, 147),    # Розовый
]


class BallLogic:
    """Модель шарика: позиция, скорость, цвет, радиус."""

    def __init__(self, x, y, radius, color, vx=None, vy=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color  # RGB кортеж, например (255, 0, 0)
        self.vx = vx if vx is not None else random.uniform(-2, 2)
        self.vy = vy if vy is not None else random.uniform(-2, 2)

    def _invert_color(self):
        """Инвертирует цвет шарика (255 - R, 255 - G, 255 - B)."""
        r, g, b = self.color
        self.color = (255 - r, 255 - g, 255 - b)

    def _random_bright_color(self):
        """Устанавливает случайный яркий цвет."""
        self.color = random.choice(BRIGHT_COLORS)

    def update(self, screen_width, screen_height):
        """Движение шарика с отскоком от стенок и crazy-эффектами."""
        self.x += self.vx
        self.y += self.vy

        # Отскок от левой стенки → инвертировать цвет
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = abs(self.vx)
            self._invert_color()
        # Отскок от правой стенки → случайный яркий цвет
        elif self.x + self.radius > screen_width:
            self.x = screen_width - self.radius
            self.vx = -abs(self.vx)
            self._random_bright_color()

        # Отскок от верхней и нижней стенок (без эффектов)
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = abs(self.vy)
        elif self.y + self.radius > screen_height:
            self.y = screen_height - self.radius
            self.vy = -abs(self.vy)

    def check_collision(self, other):
        """Проверка столкновения двух шариков (по расстоянию между центрами)."""
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.hypot(dx, dy)
        return distance < self.radius + other.radius

    def mix_colors(self, other):
        """
        Математическое смешивание цветов по RGB:
        оба шарика получают усреднённое значение своих цветов.
        """
        r = (self.color[0] + other.color[0]) // 2
        g = (self.color[1] + other.color[1]) // 2
        b = (self.color[2] + other.color[2]) // 2
        new_color = (r, g, b)
        self.color = new_color
        other.color = new_color

    def contains_point(self, px, py):
        """Проверяет, находится ли точка (px, py) внутри шарика."""
        dx = self.x - px
        dy = self.y - py
        return math.hypot(dx, dy) <= self.radius

    def distance_to(self, other):
        """Расстояние между центрами двух шариков."""
        return math.hypot(self.x - other.x, self.y - other.y)

    def move_towards(self, target_x, target_y, speed=5):
        """Движение шарика к целевой точке (для выплёвывания)."""
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed
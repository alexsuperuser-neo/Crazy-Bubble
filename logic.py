import math

class BallLogic:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color  # RGB кортеж, например (255, 0, 0)

    def move(self):
        self.x += 1  # Простое движение для теста

    def mix_colors(self, other_ball):
        # Математическое смешивание цветов по RGB из методички
        r = (self.color[0] + other_ball.color[0]) // 2
        g = (self.color[1] + other_ball.color[1]) // 2
        b = (self.color[2] + other_ball.color[2]) // 2
        self.color = (r, g, b)

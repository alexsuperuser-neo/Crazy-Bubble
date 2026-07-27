import pygame
import random
import sys
from logic import BallLogic, BRIGHT_COLORS

# ============================================================
# НАСТРОЙКИ (можно менять)
# ============================================================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 20
NUM_BALLS = 15          # Стартовое количество шариков
FPS = 60
MOVE_SPEED = 7          # Скорость выплёвывания шарика

# Зона удаления (правый нижний угол)
DELETE_ZONE = pygame.Rect(
    SCREEN_WIDTH - 130, SCREEN_HEIGHT - 80, 120, 70
)

# Палитра начальных цветов (из logic.py, 12 ярких цветов)
COLORS = BRIGHT_COLORS[:]

# ============================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================================
def random_color():
    """Случайный цвет из палитры."""
    return random.choice(COLORS)


def create_balls(n, radius, width, height):
    """Создаёт n шариков со случайными позициями и цветами."""
    balls = []
    for _ in range(n):
        x = random.randint(radius, width - radius)
        y = random.randint(radius, height - radius)
        color = random_color()
        ball = BallLogic(x, y, radius, color)
        balls.append(ball)
    return balls


def handle_collisions(balls):
    """Проверяет все пары шариков на столкновение и смешивает цвета."""
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            if balls[i].check_collision(balls[j]):
                balls[i].mix_colors(balls[j])


# ============================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Crazy Bubble")
    clock = pygame.time.Clock()

    # Создаём шарики
    balls = create_balls(NUM_BALLS, BALL_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT)
    inventory_ball = None  # Шарик, который «всосан» мышкой
    inventory_ball_index = -1  # Индекс шарика в списке (чтобы потом вернуть)

    running = True
    while running:
        # ---- Обработка событий ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                # Если есть шарик в инвентаре
                if inventory_ball is not None:
                    # Проверка: клик по зоне удаления?
                    if DELETE_ZONE.collidepoint(mx, my):
                        # Удаляем шарик — просто выбрасываем из инвентаря
                        inventory_ball = None
                        inventory_ball_index = -1
                    else:
                        # Выплёвываем шарик: задаём ему направление к курсору
                        inventory_ball.move_towards(mx, my, MOVE_SPEED)
                        # Возвращаем шарик в общий список
                        if inventory_ball_index >= 0:
                            # Восстанавливаем на место, если индекс валидный
                            # (но он мог сдвинуться — ищем по позиции)
                            pass
                        balls.append(inventory_ball)
                        inventory_ball = None
                        inventory_ball_index = -1
                else:
                    # Инвентарь пуст — пытаемся всосать шарик
                    for idx, ball in enumerate(balls):
                        if ball.contains_point(mx, my):
                            inventory_ball = ball
                            inventory_ball_index = idx
                            balls.pop(idx)
                            # Перемещаем шарик за курсором
                            inventory_ball.x = mx
                            inventory_ball.y = my
                            inventory_ball.vx = 0
                            inventory_ball.vy = 0
                            break

        # ---- Обновление логики ----
        for ball in balls:
            ball.update(SCREEN_WIDTH, SCREEN_HEIGHT)

        handle_collisions(balls)

        # Если есть шарик в инвентаре — он следует за мышкой
        if inventory_ball is not None:
            mx, my = pygame.mouse.get_pos()
            inventory_ball.x = mx
            inventory_ball.y = my

        # ---- Отрисовка ----
        screen.fill((255, 255, 255))  # Белый фон

        # Рисуем все шарики
        for ball in balls:
            pygame.draw.circle(
                screen, ball.color,
                (int(ball.x), int(ball.y)), ball.radius
            )

        # Рисуем зону удаления
        pygame.draw.rect(screen, (180, 180, 180), DELETE_ZONE)
        font = pygame.font.SysFont("Arial", 20)
        delete_text = font.render("DELETE", True, (0, 0, 0))
        text_rect = delete_text.get_rect(center=DELETE_ZONE.center)
        screen.blit(delete_text, text_rect)

        # Рисуем шарик в инвентаре (если есть)
        if inventory_ball is not None:
            pygame.draw.circle(
                screen, inventory_ball.color,
                (int(inventory_ball.x), int(inventory_ball.y)),
                inventory_ball.radius
            )

        # Счётчик шариков
        count_text = font.render(f"Balls: {len(balls)}", True, (50, 50, 50))
        screen.blit(count_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
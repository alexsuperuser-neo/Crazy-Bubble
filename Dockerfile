FROM python:3.11-slim

# Устанавливаем системные библиотеки для Pygame/SDL2 и X11
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    x11-xserver-utils \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Pygame
RUN pip install --no-cache-dir pygame

# Рабочая директория
WORKDIR /app

# Копируем все файлы проекта
COPY . .

# Запускаем игру
CMD ["python", "gui.py"]
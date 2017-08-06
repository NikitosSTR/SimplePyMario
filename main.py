#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
from pygame import *

from blocks import *
from player import *
from camera import *

# Ширина создаваемого окна
WIN_WIDTH = 800
# Высота
WIN_HEIGHT = 506
# Группируем ширину и высоту в одну переменную
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
# Задаем цвет фона
BACKGROUND_COLOR = "#004400"


def main():
    # создаем героя по (x,y) координатам
    hero = Player(55, 55)
    # по умолчанию стоим и не прыгаем
    up = left = right = False

    # Все объекты
    entities = pygame.sprite.Group()
    # то, во что мы будем врезаться или опираться
    platforms = []
    # Добавляем героя
    entities.add(hero)

    # Инициализвция уровня
    level = [
       "--------------------------------------",
       "-                                    -",
       "-                                    -",
       "-                       --      ---  -",
       "-                                    -",
       "-                  --                -",
       "-            --                 - -  -",
       "-                                    -",
       "-                                    -",
       "--                                   -",
       "-                                    -",
       "-                  ----     ---      -",
       "-                                    -",
       "--                                   -",
       "-        -------                 --  -",
       "-                                    -",
       "-                           ---      -",
       "-                                    -",
       "-      ---    --        -            -",
       "-                                    -",
       "-                                    -",
       "-   ------         ----              -",
       "-                                    -",
       "-                        -           -",
       "-                                    -",
       "-                           --       -",
       "-                                    -",
       "-                                    -",
       "-                                    -",
       "-                                    -",
       "-                       --      ---  -",
       "-                                    -",
       "-                  --                -",
       "--------------------------------------"]

    # Timer
    timer = pygame.time.Clock()

    # Инициация PyGame, обязательная строчка
    pygame.init()

    # Создаем оконо
    screen = pygame.display.set_mode(DISPLAY)
    # Пишем в название окна
    pygame.display.set_caption("PyMario")
    # Создание видимой поверхности
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    # Заливаем поверхность сплошным цветом
    bg.fill(Color(BACKGROUND_COLOR))

    # Высчитываем фактическую ширину уровня
    total_level_width = len(level[0])*PLATFORM_WIDTH
    # высоту
    total_level_height = len(level)*PLATFORM_HEIGHT

    camera = Camera(camera_configure, total_level_width, total_level_height)

    # координаты
    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                # инициализируем новую платформу с нужными координатами
                pf = Platform(x, y)
                # добавление платформы в массив всех спрайтов
                entities.add(pf)
                # добавление в массив со спрайтами препятствий/платформ
                platforms.append(pf)

            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0

    # Основной цикл программы
    while True:

        timer.tick(40)

        # Обрабатываем события
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit("QUIT")

            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True

            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYDOWN and e.key == K_UP:
                up = True

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False

            if e.type == KEYUP and e.key == K_LEFT:
                left = False

            if e.type == KEYUP and e.key == K_UP:
                up = False

        # Отрисовка фона
        screen.blit(bg, (0, 0))
        # Отрисовка нового положения персонажа
        hero.update(left, right, up, platforms)

        # Обновляем камеру относительно персонажа
        camera.update(hero)

        # Отрисовка всего остальнного
        for e in entities:
            screen.blit(e.image, camera.apply(e))

        # Обновление и вывод всех изменений на экран
        pygame.display.update()


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    # Фикчация камеры внутри уровня
    l = min(0.0, l)
    l = max(float(-(camera.width - WIN_WIDTH)), l)
    t = max(float(-(camera.height-WIN_HEIGHT)), t)
    t = min(0.0, t)

    return Rect(l, t, w, h)

if __name__ == "__main__":
    main()

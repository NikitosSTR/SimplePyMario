#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *

MOVE_SPEED = 10
WIDTH = 22
HEIGHT = 32
JUMP_POWER = 20
GRAVITY = 1.35
COLOR = "#888888"


class Player(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        # Скорость вертикального перемещения
        self.yvel = 0
        # На земле ли персоонаж
        self.onGround = False
        # Скорость перемещения. 0 - стоять на месте
        self.xvel = 0
        # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startX = x
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        # прямоугольный объект
        self.rect = Rect(x, y, WIDTH, HEIGHT)

    def update(self,  left, right, up, platforms):

        if left:
            self.xvel = -MOVE_SPEED

        if right:
            self.xvel = MOVE_SPEED

        if up:
            if self.onGround:
                self.yvel = -JUMP_POWER

        if not(left or right):
            self.xvel = 0

        if not self.onGround:
                self.yvel += GRAVITY

        self.onGround = False

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            # если есть пересечение платформы с игроком
            if sprite.collide_rect(self, p):

                # если движется вправо
                if xvel > 0:
                    # то не движется вправо
                    self.rect.right = p.rect.left

                # если движется влево
                if xvel < 0:
                    # то не движется влево
                    self.rect.left = p.rect.right

                # если падает вниз
                if yvel > 0:
                    # то не падает вниз
                    self.rect.bottom = p.rect.top
                    # и становится на что-то твердое
                    self.onGround = True
                    # и энергия падения пропадает
                    self.yvel = 0

                # если движется вверх
                if yvel < 0:
                    # то не движется вверх
                    self.rect.top = p.rect.bottom
                    # и энергия прыжка пропадает
                    self.yvel = 0

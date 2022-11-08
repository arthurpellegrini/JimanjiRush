#!/usr/bin/python
# -*- coding: utf-8 -*-s
import random

import pygame

from .constants import Constants


class Sprite(pygame.sprite.Sprite):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.current_image = 0
        self.images = [f.convert_alpha() for f in Constants.ASSETS[name]]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rate = 10  # vitesse du changement d'image dans l'animation

    def animate(self, reverse=False):
        index = self.current_image // self.rate % len(self.images)
        if reverse:
            index *= -1
        self.image = self.images[index]
        self.current_image += 1

    def update(self):
        self.animate()


class Skull(Sprite):
    def __init__(self, pos: tuple):
        super().__init__("SKULL")
        self.rect.center = pos


class Collectable(Sprite):
    def __init__(self, name: str):
        super().__init__(name)
        self.margin = 20
        self.velocity = Constants.VELOCITY
        self.ground_height = 100
        self.rect.x = Constants.DISPLAY_W // 10 * random.randint(1, 10) - self.margin - self.rect.width
        self.rect.y = - random.randint(0, Constants.DISPLAY_H // 10)

    def fall(self):
        self.animate()
        self.rect.y += self.velocity

    def check_if_visible(self) -> bool:
        if self.rect.y >= Constants.DISPLAY_H - self.margin - self.ground_height:
            return False
        return True


class Bonus(Sprite):
    def __init__(self, name: str):
        super().__init__(name)


#!/usr/bin/python
# -*- coding: utf-8 -*-s
import random

from .constants import Constants
from .sprite import Sprite


class Entity(Sprite):
    def __init__(self, name: str, velocity: int):
        """

        :param name:
        """
        super().__init__(name=name)
        self.name = name
        self.velocity = velocity
        self.rect = self.image.get_rect()
        self.margin = 20
        self.ground_heigth = 100

        self.rect.x = Constants.DISPLAY_W // 10 * random.randint(1, 10) - self.margin - self.rect.width
        self.rect.y = - random.randint(0, Constants.DISPLAY_H // 10)

    def fall(self):
        self.animate()
        self.rect.y += self.velocity

    def check_if_visible(self) -> bool:
        if self.rect.y >= Constants.DISPLAY_H - self.margin - self.ground_heigth:
            return False
        return True

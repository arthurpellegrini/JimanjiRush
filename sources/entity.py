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
        self.margin = 10
        self.rect.center = (Constants.DISPLAY_W / 10 * random.randint(1, 9) - self.margin, self.margin)

    def fall(self):
        self.animate()
        self.rect.y += self.velocity

    def check_if_visible(self) -> bool:
        if self.rect.y >= Constants.DISPLAY_H - self.margin:
            return False
        return True

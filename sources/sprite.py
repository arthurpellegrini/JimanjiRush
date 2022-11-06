#!/usr/bin/python
# -*- coding: utf-8 -*-s
import pygame

from .constants import Constants


class Sprite(pygame.sprite.Sprite):
    def __init__(self, name: str):
        super().__init__()
        self.current_image = 0
        self.images = Constants.ASSETS[name]
        self.image = self.images[0]
        self.rate = 10  # vitesse du changement d'image dans l'animation

    def animate(self, reverse=False):
        index = self.current_image // self.rate % len(self.images)
        if reverse:
            index *= -1
        self.image = self.images[index]
        self.current_image += 1

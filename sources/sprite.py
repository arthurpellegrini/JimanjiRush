#!/usr/bin/python
# -*- coding: utf-8 -*-s
import random
import threading
import time

import pygame

from .constants import Constants


class Sprite(pygame.sprite.Sprite):
    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.current_image = 0
        self.images = [f.convert_alpha() for f in Constants.ASSETS[name]]
        self.image = self.images[0]
        self.margin = 25
        self.ground_height = 100 + self.margin
        self.rect = self.image.get_rect()
        self.velocity = Constants.VELOCITY
        self.rate = 8  # vitesse du changement d'image dans l'animation

    def animate(self, reverse=False):
        self.image = self.images[self.current_image // self.rate % len(self.images)]
        if reverse:
            self.image = pygame.transform.flip(self.image, True, False)
        self.current_image += 1

    def check_if_visible(self) -> bool:
        if self.rect.y >= Constants.DISPLAY_H - self.ground_height:
            return False
        return True

    def collide(self, sprite: pygame.sprite.Sprite):
        pass


class Player(Sprite):
    def __init__(self):
        super().__init__("PLAYER")
        self.rate //= 2
        self.reset_position()
        self.left, self.right = False, False
        self.egg, self.star = False, False
        self.last_velocity = 0

    def reset_position(self):
        self.rect.center = (Constants.DISPLAY_W / 9, Constants.DISPLAY_H - self.ground_height)

    def move(self, key_pressed: dict):
        self.velocity = Constants.VELOCITY
        if key_pressed.get(pygame.K_LEFT):
            self.left, self.right = True, False
            self.move_left()

        elif key_pressed.get(pygame.K_RIGHT):
            self.left, self.right = False, True
            self.move_right()
        else:
            self.image = Constants.ASSETS["IDDLE"][0]
            if self.left and not self.right:
                self.image = pygame.transform.flip(self.image, True, False)

    def move_left(self):
        self.animate(reverse=True)
        if self.rect.x - self.velocity > self.margin:
            self.rect.x -= self.velocity
        else:
            self.rect.x = self.margin

    def move_right(self):
        self.animate()
        if self.rect.x + self.velocity < Constants.DISPLAY_W - self.margin - self.rect.width:
            self.rect.x += self.velocity
        else:
            self.rect.x = Constants.DISPLAY_W - self.margin - self.rect.width

    def increase_velocity(self):
        self.star = True
        self.last_velocity = Constants.VELOCITY * 0.5
        self.velocity += self.last_velocity

        def wait_and_restore():
            time.sleep(1)
            self.velocity -= self.last_velocity
            self.star = False

        threading.Thread(target=wait_and_restore, daemon=True).start()

    def decrease_velocity(self):
        self.egg = True
        self.last_velocity = Constants.VELOCITY * 0.5
        self.velocity -= self.last_velocity

        def wait_and_restore():
            time.sleep(1)
            self.velocity += self.last_velocity
            self.egg = False

        threading.Thread(target=wait_and_restore, daemon=True).start()


class User(Player):
    def __init__(self):
        super().__init__()
        self.name = ""
        self.score = 0
        self.start_time = 0
        self.time = 0
        self.hearts = 3

    def update_time(self):
        self.time = (abs(self.start_time - pygame.time.get_ticks())) // 1000

    def reset_name(self):
        self.name = ""

    def reset_score(self):
        self.score = 0

    def reset_time(self):
        self.time = 0

    def reset_hearts(self):
        self.hearts = 3

    def reset_all(self):
        self.reset_score()
        self.reset_time()
        self.reset_hearts()


class Collectable(Sprite):
    def __init__(self, name: str):
        super().__init__(name)
        self.rect.x = Constants.DISPLAY_W // 9 * random.randint(1, 9) - self.margin - self.rect.width
        self.rect.y = - random.randint(0, Constants.DISPLAY_H // 9)

    def fall(self):
        self.velocity = Constants.VELOCITY // 2
        self.rect.y += self.velocity

    def collide(self, user: User):
        if self.rect.colliderect(user.rect):
            Constants.SPRITES.remove(self)
            if self.name == "COIN":
                user.score += Constants.SCORE_VALUE * 5

            elif self.name == "BLUE_GEM":
                user.score += Constants.SCORE_VALUE * 10

            elif self.name == "GREEN_GEM":
                user.score += Constants.SCORE_VALUE * 40

            elif self.name == "RUBY":
                user.score += Constants.SCORE_VALUE * 80


class CannonBall(Sprite):
    def __init__(self):
        super().__init__("CANNONBALL")
        self.rect.x = Constants.DISPLAY_W // 9 * random.randint(1, 9) - self.margin - self.rect.width
        self.rect.y = - random.randint(0, Constants.DISPLAY_H // 9)

    def fall(self):
        self.velocity = Constants.VELOCITY // 2
        self.rect.y += self.velocity

    def collide(self, user: User):
        if self.rect.colliderect(user.rect):
            Constants.SPRITES.remove(self)
            if user.hearts > 0:
                user.hearts -= 1


class Heart(Sprite):
    def __init__(self):
        super().__init__("HEART")
        self.rect.x = Constants.DISPLAY_W // 9 * random.randint(1, 9) - self.margin - self.rect.width
        self.rect.y = - random.randint(0, Constants.DISPLAY_H // 9)

    def fall(self):
        self.velocity = Constants.VELOCITY // 2
        self.rect.y += self.velocity

    def collide(self, user: User):
        if self.rect.colliderect(user.rect):
            Constants.SPRITES.remove(self)
            if user.hearts < 3:
                user.hearts += 1


class Egg(Sprite):
    def __init__(self):
        super().__init__("EGG")
        self.rect.x = Constants.DISPLAY_W // 9 * random.randint(1, 9) - self.margin - self.rect.width
        self.rect.y = - random.randint(0, Constants.DISPLAY_H // 9)

    def fall(self):
        self.velocity = Constants.VELOCITY // 2
        self.rect.y += self.velocity

    def collide(self, user: User):
        if self.rect.colliderect(user.rect):
            Constants.SPRITES.remove(self)
            if not user.egg and not user.star:
                user.decrease_velocity()
            else:
                if user.score >= Constants.SCORE_VALUE:
                    user.score -= Constants.SCORE_VALUE


class Star(Sprite):
    def __init__(self):
        super().__init__("STAR")
        self.rect.x = Constants.DISPLAY_W // 9 * random.randint(1, 9) - self.margin - self.rect.width
        self.rect.y = - random.randint(0, Constants.DISPLAY_H // 9)

    def fall(self):
        self.velocity = Constants.VELOCITY // 2
        self.rect.y += self.velocity

    def collide(self, user: User):
        if self.rect.colliderect(user.rect):
            Constants.SPRITES.remove(self)
            if not user.star and not user.egg:
                user.increase_velocity()
            else:
                user.score += Constants.SCORE_VALUE


class Skull(Sprite):
    def __init__(self, pos: tuple):
        super().__init__("SKULL")
        self.rect.center = pos

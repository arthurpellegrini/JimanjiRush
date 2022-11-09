#!/usr/bin/python
# -*- coding: utf-8 -*-s
import random
import re

import pygame

from .constants import Constants
from .menu import MainMenu, InputMenu, GameOverMenu, ScoreMenu, CreditsMenu
from .score import Score
from .sprite import User, Collectable, CannonBall, Heart, Egg, Star


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_icon(Constants.ASSETS["ICON"])
        pygame.display.set_caption("Jimanji Rush")

        self.display = pygame.Surface((Constants.DISPLAY_W, Constants.DISPLAY_H))
        self.window = pygame.display.set_mode((Constants.DISPLAY_W, Constants.DISPLAY_H))

        self.clock = pygame.time.Clock()
        self.running, self.playing = True, False

        self.key_pressed = {}
        self.unicode = ""

        self.iterations = 0

        self.user = User()
        self.scores = Score()

        self.main_menu = MainMenu(self)
        self.input_menu = InputMenu(self)
        self.game_over_menu = GameOverMenu(self)
        self.score_menu = ScoreMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.current_menu = self.main_menu

    def check_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.current_menu.run_display = False

            if event.type == pygame.KEYDOWN:
                self.key_pressed[event.key] = True

                if type(self.current_menu) == InputMenu and re.match(Constants.USERNAME_REGEX, event.unicode):
                    self.unicode = event.unicode

            elif event.type == pygame.KEYUP:
                self.key_pressed[event.key] = False

    def reset_keys(self, key=None):
        if key is None:
            for key_code in list(self.key_pressed.keys()):
                self.key_pressed[key_code] = False
            self.unicode = ""
        else:
            self.key_pressed[key] = False

    def display_text(self, text, size, pos: tuple, color=Constants.WHITE):
        font = pygame.font.Font(Constants.ASSETS["FONT"], size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = pos
        self.display.blit(text_surface, text_rect)

    def game_loop(self):
        while self.playing:
            self.check_events()
            self.gameplay()
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.clock.tick(60)
            self.iterations += 1

    def gameplay(self):
        if self.key_pressed.get(pygame.K_ESCAPE) or self.user.hearts == 0:
            self.current_menu = self.main_menu
            if self.user.hearts == 0:
                self.scores.add_user((self.user.name, self.user.score, self.user.time))
                self.current_menu = self.game_over_menu
            self.user.reset_all()
            self.user.reset_position()
            Constants.SPRITES.clear()
            self.playing = False

        self.display.blit(Constants.ASSETS["BACKGROUND"][0], (0, 0))
        self.generate_object()

        self.display_sprites()

        self.display_monitor()
        self.reset_keys(key=pygame.K_ESCAPE)

    def display_sprites(self):
        for entity in Constants.SPRITES:
            if not entity.check_if_visible():
                Constants.SPRITES.remove(entity)
            else:
                entity.collide(self.user)
                entity.fall()
                entity.update()
            self.display.blit(entity.image, entity.rect)
        self.user.move(self.key_pressed)
        self.display.blit(self.user.image, self.user.rect)

    def display_monitor(self):
        self.user.update_time()
        self.display_text("Score: " + str(self.user.score), 30, (Constants.DISPLAY_W / 6, Constants.DISPLAY_H / 15))
        self.display_text("Time: " + str(self.user.time), 30, (Constants.DISPLAY_W / 6 * 3, Constants.DISPLAY_H / 15))
        self.display_text("Heart: " + str(self.user.hearts), 30,
                          (Constants.DISPLAY_W / 6 * 5, Constants.DISPLAY_H / 15))

    def generate_object(self):
        if len(Constants.SPRITES) < Constants.NB_SPRITES:
            luck = random.randint(0, 100)
            if luck in range(0, 35):  # CannonBall
                Constants.SPRITES.append(CannonBall())
            elif luck in range(35, 40):  # Heart
                Constants.SPRITES.append(Heart())
            elif luck in range(40, 45):  # Egg
                Constants.SPRITES.append(Egg())
            elif luck in range(45, 50):  # Star
                Constants.SPRITES.append(Star())
            elif luck in range(50, 80):  # Coin
                Constants.SPRITES.append(Collectable("COIN"))
            elif luck in range(80, 89):  # Blue Gem
                Constants.SPRITES.append(Collectable("BLUE_GEM"))
            elif luck in range(89, 95):  # Green Gem
                Constants.SPRITES.append(Collectable("GREEN_GEM"))
            elif luck in range(95, 100):  # Ruby
                Constants.SPRITES.append(Collectable("RUBY"))

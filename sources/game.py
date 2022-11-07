#!/usr/bin/python
# -*- coding: utf-8 -*-s
import random
import re

import pygame

from .constants import Constants
from .entity import Entity
from .menu import MainMenu, CreditsMenu, ScoreMenu
from .player import Player
from .score import Score, UserScore


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
        self.entity_velocity = 5

        # TODO: REMETTRE QUAND FIN TEST
        self.STATE = "INPUT"
        # self.STATE = "GAMEPLAY"
        self.username = ""
        self.username_is_empty, self.username_overflow = False, False
        self.first_frame_game_over = True

        self.player = Player()
        self.hearts = 3
        self.entities = []

        self.user_score = 0
        self.user_time = 0
        self.scores = Score()

        self.main_menu = MainMenu(self)
        self.score_menu = ScoreMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.current_menu = self.main_menu

    def check_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.current_menu.run_display = False
                self.scores.write_score_file()

            if event.type == pygame.KEYDOWN:
                self.key_pressed[event.key] = True

                if re.match(Constants.USERNAME_REGEX, event.unicode):
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

    def draw_text(self, text, size, x, y, color=Constants.WHITE):
        font = pygame.font.Font(Constants.ASSETS["FONT"], size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def game_loop(self):
        while self.playing:
            self.check_events()
            self.input_name()
            self.gameplay()
            self.game_over()
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.clock.tick(60)
            self.iterations += 1

    def input_name(self):
        if self.STATE == "INPUT":
            self.display.fill(Constants.BACKGROUND)

            if self.key_pressed.get(pygame.K_ESCAPE):
                self.username = ""
                self.playing = False

            if self.key_pressed.get(pygame.K_RETURN):
                if self.username == "":
                    self.username_is_empty = True
                else:
                    self.STATE = "GAMEPLAY"

            if self.key_pressed.get(pygame.K_BACKSPACE):
                self.username_overflow = False
                self.username = self.username[:-1]

            if self.unicode != "":
                if len(self.username) < 15:
                    self.username_is_empty = False
                    self.username += self.unicode
                else:
                    self.username_overflow = True

            # Cursor Flashing
            if self.iterations % 60 in range(30):
                cursor = "_"
            else:
                cursor = " "

            self.draw_text("Your name: " + self.username + cursor, 40, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 3)

            if self.username_is_empty:
                self.draw_text("Username field can't be empty", 20, Constants.DISPLAY_W / 2,
                               Constants.DISPLAY_H / 3 * 2,
                               Constants.RED)
            if self.username_overflow:
                self.draw_text("/!\ Username can't exceed 15 characters", 20, Constants.DISPLAY_W / 2,
                               Constants.DISPLAY_H / 3 * 2, Constants.RED)

            self.draw_text("Press RETURN to play", 20, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 15 * 13)
            self.draw_text('Press ESC to return to Main Menu', 20, Constants.DISPLAY_W / 2,
                           Constants.DISPLAY_H / 15 * 14)
            self.reset_keys()

    def gameplay(self):
        if self.STATE == "GAMEPLAY":
            self.first_frame_game_over = True
            if self.key_pressed.get(pygame.K_ESCAPE):
                self.playing = False
                self.STATE = "INPUT"

            if self.hearts == 0:
                self.STATE = "GAME_OVER"

            self.display.blit(pygame.transform.scale(Constants.ASSETS["BACKGROUND"][0],
                                                     (Constants.DISPLAY_W, Constants.DISPLAY_H)), (0, 0))
            self.generate_object()
            for entity in self.entities:
                if entity.check_if_visible():
                    if entity.rect.colliderect(self.player.rect):
                        self.entities.remove(entity)
                        if entity.name == "CANNONBALL":
                            if self.hearts > 0:
                                self.hearts -= 1
                        elif entity.name == "HEART":
                            if self.hearts < 3:
                                self.hearts += 1
                        elif entity.name == "EGG":
                            if not self.player.egg and not self.player.star:
                                self.player.decrease_velocity()
                            else:
                                self.user_score -= 100
                        elif entity.name == "STAR":
                            if not self.player.star and not self.player.egg:
                                self.player.increase_velocity()
                            else:
                                self.user_score += 100
                        elif entity.name == "COIN":
                            self.user_score += 500
                        elif entity.name == "BLUE_GEM":
                            self.user_score += 1000
                        elif entity.name == "GREEN_GEM":
                            self.user_score += 4000
                        elif entity.name == "RUBY":
                            self.user_score += 8000
                    entity.fall()
                else:
                    self.entities.remove(entity)
                self.display.blit(entity.image, entity.rect)
            self.player.move(self.key_pressed)

            self.display.blit(self.player.image, self.player.rect)
            self.draw_text("Score: " + str(self.user_score), 30, Constants.DISPLAY_W / 4, Constants.DISPLAY_H / 15)
            self.draw_text("Time: " + str(pygame.time.get_ticks() // 1000), 30, Constants.DISPLAY_W / 4 * 3,
                           Constants.DISPLAY_H / 15)
            self.reset_keys(key=pygame.K_ESCAPE)

    def generate_object(self):
        if len(self.entities) < 10:
            nb = random.randint(0, 100)
            if nb in range(0, 35):  # CannonBall
                self.entities.append(Entity("CANNONBALL", self.entity_velocity))
            elif nb in range(35, 40):  # Heart
                self.entities.append(Entity("HEART", self.entity_velocity))
            elif nb in range(40, 45):  # Egg
                self.entities.append(Entity("EGG", self.entity_velocity))
            elif nb in range(45, 50):  # Star
                self.entities.append(Entity("STAR", self.entity_velocity))
            elif nb in range(50, 80):  # Coin
                self.entities.append(Entity("COIN", self.entity_velocity))
            elif nb in range(80, 89):  # Blue Gem
                self.entities.append(Entity("BLUE_GEM", self.entity_velocity))
            elif nb in range(89, 95):  # Green Gem
                self.entities.append(Entity("GREEN_GEM", self.entity_velocity))
            elif nb in range(95, 100):  # Ruby
                self.entities.append(Entity("RUBY", self.entity_velocity))

    def game_over(self):
        if self.STATE == "GAME_OVER":
            if self.first_frame_game_over:
                self.player.reset_position()
                self.user_time = random.randint(150, 9999)
                self.user_score = random.randint(600, 99999999)

                self.scores.add_user(UserScore(self.username, self.user_score, self.user_time))
                self.first_frame_game_over = False

            if self.key_pressed.get(pygame.K_ESCAPE):
                self.playing = False
                self.STATE = "INPUT"

            if self.key_pressed.get(pygame.K_RETURN):
                self.user_score = 0
                self.user_time = 0
                self.hearts = 3
                self.entities.clear()
                self.STATE = "GAMEPLAY"

            skull = pygame.transform.scale(
                Constants.ASSETS["SKULL"][self.iterations // 10 % len(Constants.ASSETS["SKULL"])], (186, 225))
            skull_rect = skull.get_rect()
            skull_rect.center = (Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 5 * 2)
            self.display.fill(Constants.BLACK)
            self.display.blit(skull, skull_rect)

            self.draw_text('Game Over', 40, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 5 * 3)
            self.draw_text('Press RETURN to Replay', 20, Constants.DISPLAY_W / 2,
                           Constants.DISPLAY_H / 15 * 13)
            self.draw_text('Press ESC to return to Main Menu', 20, Constants.DISPLAY_W / 2,
                           Constants.DISPLAY_H / 15 * 14)
            self.reset_keys()

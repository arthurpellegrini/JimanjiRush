#!/usr/bin/python
# -*- coding: utf-8 -*-s
import random
import re

import pygame

from .constants import Constants
from .menu import MainMenu, CreditsMenu, ScoreMenu
from .score import Score, UserScore
from .constants import Constants


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_icon(Constants.ASSETS["ICON"])
        pygame.display.set_caption("Jimanji Rush")

        self.clock = pygame.time.Clock()
        self.running, self.playing = True, False

        self.LEFT_KEY, self.RIGHT_KEY, self.DOWN_KEY, self.UP_KEY = False, False, False, False
        self.ENTER_KEY, self.ESC_KEY, self.BACKSPACE, self.SPACE_KEY = False, False, False, False
        self.unicode = ""

        self.iterations = 0

        self.STATE = "INPUT"
        self.username = ""
        self.username_is_empty, self.username_overflow = False, False
        self.first_frame_game_over = True

        self.user_score = 0
        self.user_time = 0
        self.scores = Score()

        self.display = pygame.Surface((Constants.DISPLAY_W, Constants.DISPLAY_H))
        self.window = pygame.display.set_mode((Constants.DISPLAY_W, Constants.DISPLAY_H))

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
                if event.key == pygame.K_RETURN:
                    self.ENTER_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.ESC_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACKSPACE = True
                if event.key == pygame.K_SPACE:
                    self.SPACE_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.DOWN_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.UP_KEY = True
                if re.match(Constants.USERNAME_REGEX, event.unicode):
                    self.unicode = event.unicode

    def reset_keys(self):
        self.LEFT_KEY, self.RIGHT_KEY, self.DOWN_KEY, self.UP_KEY = False, False, False, False
        self.ENTER_KEY, self.ESC_KEY, self.BACKSPACE, self.SPACE_KEY = False, False, False, False
        self.unicode = ""

    def draw_text(self, text, size, x, y, color=Constants.WHITE):
        font = pygame.font.Font(Constants.ASSETS["FONT"], size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def game_loop(self):
        while self.playing:
            self.input_name()
            self.gameplay()
            self.game_over()
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.clock.tick(60)
            self.iterations += 1

    def input_name(self):
        if self.STATE == "INPUT":
            self.check_events()
            self.display.fill(Constants.BACKGROUND)

            if self.ESC_KEY:
                self.username = ""
                self.playing = False

            if self.SPACE_KEY:
                if self.username == "":
                    self.username_is_empty = True
                else:
                    self.STATE = "GAMEPLAY"

            if self.BACKSPACE:
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

            self.draw_text("Press SPACE to play", 20, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 15 * 13)
            self.draw_text('Press ESC to return to Main Menu', 20, Constants.DISPLAY_W / 2,
                           Constants.DISPLAY_H / 15 * 14)
            self.reset_keys()

    def gameplay(self):
        if self.STATE == "GAMEPLAY":
            self.check_events()
            self.first_frame_game_over = True
            if self.ESC_KEY:
                self.playing = False
                self.STATE = "INPUT"

            if self.SPACE_KEY:
                self.STATE = "GAME_OVER"

            self.display.blit(pygame.transform.scale(Constants.ASSETS["BACKGROUND"][0],
                                                     (Constants.DISPLAY_W, Constants.DISPLAY_H)), (0, 0))

            self.draw_text('Thanks for Playing', 20, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 2)
            self.draw_text('Press ESC to return to Main Menu', 20, Constants.DISPLAY_W / 2,
                           Constants.DISPLAY_H / 15 * 14)
            self.reset_keys()

    def game_over(self):
        if self.STATE == "GAME_OVER":
            self.check_events()

            if self.first_frame_game_over:
                self.user_time = random.randint(150, 9999)
                self.user_score = random.randint(600, 99999999)

                self.scores.add_user(UserScore(self.username, self.user_score, self.user_time))
                self.first_frame_game_over = False

            if self.ESC_KEY:
                self.playing = False
                self.STATE = "INPUT"

            if self.SPACE_KEY:
                self.STATE = "GAMEPLAY"

            skull = pygame.transform.scale(
                Constants.ASSETS["SKULL"][self.iterations // 8 % len(Constants.ASSETS["SKULL"])], (186, 225))
            skull_rect = skull.get_rect()
            skull_rect.center = (Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 3)
            self.display.fill(Constants.BLACK)
            self.display.blit(skull, skull_rect)
            self.draw_text('Press SPACE to Replay', 20, Constants.DISPLAY_W / 2,
                           Constants.DISPLAY_H / 15 * 13)
            self.draw_text('Press ESC to return to Main Menu', 20, Constants.DISPLAY_W / 2,
                           Constants.DISPLAY_H / 15 * 14)
            self.reset_keys()

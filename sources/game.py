#!/usr/bin/python
# -*- coding: utf-8 -*-s
import pygame
import re
from .menu import MainMenu, CreditsMenu, ScoreMenu
from .score import Score, UserScore


class Game:
    def __init__(self, assets: dict):
        pygame.init()
        self.running, self.playing = True, False
        self.first_time = True

        self.event_unicode = ""
        self.LEFT_KEY, self.RIGHT_KEY, self.DOWN_KEY, self.UP_KEY = False, False, False, False
        self.ENTER_KEY, self.ESC_KEY, self.BACKSPACE, self.SPACE = False, False, False, False

        self.DISPLAY_W, self.DISPLAY_H = 1280, 720
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))

        # TODO: Modifier l'icône et le nom de la fenêtre principale
        self.assets = assets
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.BACKGROUND_COLOR = (78, 150, 142)
        self.main_menu = MainMenu(self)
        self.score_menu = ScoreMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

        self.score = Score()

    def game_loop(self):
        while self.playing:
            self.check_events()  # vérifie les entrées
            if self.ESC_KEY:  # Le joueur veut-il quitter la partie
                self.playing = False
                self.first_time = True

            self.display.blit(pygame.transform.scale(self.assets["BACKGROUND"][0],
                                                     (self.DISPLAY_W, self.DISPLAY_H)), (0, 0))

            self.draw_text('Thanks for Playing', 20, self.DISPLAY_W / 2, self.DISPLAY_H / 2)

            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()  # on nettoie les entrées

    def check_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
                self.score.write_score_file()

            if event.type == pygame.KEYDOWN:
                self.event_unicode = event.unicode
                if event.key == pygame.K_RETURN:
                    self.ENTER_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.ESC_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACKSPACE = True
                if event.key == pygame.K_SPACE:
                    self.SPACE = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.DOWN_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.UP_KEY = True

    def reset_keys(self):
        self.LEFT_KEY, self.RIGHT_KEY, self.DOWN_KEY, self.UP_KEY = False, False, False, False
        self.ENTER_KEY, self.ESC_KEY, self.BACKSPACE, self.SPACE = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.assets["FONT"], size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def display_time(self):
        pass

    # def input_name(self) -> str:
    #     finish = False
    #     pattern = re.compile(r"([0-9A-Za-z]){1,10}", re.IGNORECASE)
    #
    #     self.display.fill(self.BACKGROUND_COLOR)
    #     self.draw_text("Your name: ", 40, self.DISPLAY_W / 3, self.DISPLAY_H / 2)
    #
    #     pygame.display.update()
    #     user_input_value = ""
    #
    #     while not finish:
    #         self.check_events()
    #         if self.SPACE:
    #             finish = True
    #         elif self.BACKSPACE:
    #             user_input_value = user_input_value[:-1]
    #         if pattern.match(self.event_unicode) is not None:
    #             user_input_value += self.event_unicode
    #         print(user_input_value)
    #         self.draw_text(user_input_value, 40, self.DISPLAY_W * 2, self.DISPLAY_H / 2)
    #
    #         self.reset_keys()
    #
    #     return user_input_value

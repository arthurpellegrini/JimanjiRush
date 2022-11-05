#!/usr/bin/python
# -*- coding: utf-8 -*-s
import pygame
import re
from .menu import MainMenu, CreditsMenu, ScoreMenu
from .score import Score, UserScore
from .constants import Constants


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running, self.playing = True, False

        self.username = ""
        self.user_score = 0
        self.user_time = 0
        self.scores = Score()

        self.unicode = ""

        self.LEFT_KEY, self.RIGHT_KEY, self.DOWN_KEY, self.UP_KEY = False, False, False, False
        self.ENTER_KEY, self.ESC_KEY, self.BACKSPACE, self.SPACE_KEY = False, False, False, False

        self.display = pygame.Surface((Constants.DISPLAY_W, Constants.DISPLAY_H))
        self.window = pygame.display.set_mode((Constants.DISPLAY_W, Constants.DISPLAY_H))

        # TODO: Modifier l'icône et le nom de la fenêtre principale
        self.main_menu = MainMenu(self)
        self.score_menu = ScoreMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def game_loop(self):
        while self.playing:
            if self.username == "":
                self.input_name()
            else:
                self.check_events()  # vérifie les entrées
                if self.ESC_KEY:  # Le joueur veut-il quitter la partie
                    self.playing = False

                self.display.blit(pygame.transform.scale(Constants.ASSETS["BACKGROUND"][0],
                                                         (Constants.DISPLAY_W, Constants.DISPLAY_H)), (0, 0))

                self.draw_text('Thanks for Playing', 20, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 2)

                self.window.blit(self.display, (0, 0))
                pygame.display.update()
                self.reset_keys()  # on nettoie les entrées

    def check_events(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
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

    def display_time(self):
        pass

    # TODO: fonction game_over qui sauvegarde le score du joueur en cours
    # def game_over(self):
    # afficher une page de game over et cliquer sur espace pour revenir au menu (OPTIONNEL: ou cliquer pour relancer)
    # self.scores.add_user(UserScore(self.username, self.user_score, self.user_time)

    def input_name(self):
        finish = False
        is_empty, is_full = False, False

        while not finish:
            self.display.fill(Constants.BACKGROUND)
            self.check_events()

            if self.ESC_KEY:
                self.username = ""
                finish = True
                self.playing = False
                continue

            if self.SPACE_KEY:
                if self.username == "":
                    is_empty = True
                else:
                    finish = True
                    continue

            if self.BACKSPACE:
                is_full = False
                self.username = self.username[:-1]

            if self.unicode != "":
                if len(self.username) < 15:
                    is_empty = False
                    self.username += self.unicode
                else:
                    is_full = True

            self.draw_text("Your name: " + self.username, 40, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 4)

            if is_empty:
                self.draw_text("Field cannot be empty", 30, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 4 * 2,
                               Constants.RED)
            if is_full:
                self.draw_text("Cannot exceed (15) characters", 30, Constants.DISPLAY_W / 2,
                               Constants.DISPLAY_H / 4 * 2, Constants.RED)

            self.draw_text("Press space to play", 30, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 4 * 3)
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()
            self.clock.tick(60)

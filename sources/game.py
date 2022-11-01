#!/usr/bin/python
# -*- coding: utf-8 -*-s
import sys
import pygame
from .menu import MainMenu, CreditsMenu, ScoreMenu


class Game:
    def __init__(self, assets: dict):
        pygame.init()
        self.running, self.playing = True, False

        self.LEFT_KEY, self.RIGHT_KEY, self.DOWN_KEY, self.UP_KEY = False, False, False, False
        self.ENTER_KEY, self.ESC_KEY = False, False

        self.DISPLAY_W, self.DISPLAY_H = 1280, 720
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.assets = assets
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = ScoreMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def game_loop(self):
        while self.playing:
            self.check_events()  # vérifie les entrées
            if self.ESC_KEY:    # Le joueur veut-il quitter la partie
                self.playing = False

            # self.display.fill(self.BLACK)
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.ENTER_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.ESC_KEY = True
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
        self.ENTER_KEY, self.ESC_KEY = False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.assets["FONT"], size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def display_time(self):
        print("")
        #scoredisplay = myFont.render("DISTANCE {0}".format(int(new_score.get_distance())), True, (255, 255, 255))
        #new_score.update_distance()
        #return self.display.blit(scoredisplay, (5, 10))
#!/usr/bin/python
# -*- coding: utf-8 -*-s
import pygame
from .constants import Constants


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 4
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 150

    def draw_cursor(self):
        self.game.draw_text('>', 40, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'GAME'
        self.startx, self.starty = self.mid_w, self.mid_h + 200
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 250
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 300
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(Constants.BACKGROUND)
            self.game.draw_text("Jimanji Rush", 80, self.mid_w, self.mid_h)
            self.game.draw_text("GAME", 40, self.startx, self.starty)
            self.game.draw_text("SCORES", 40, self.optionsx, self.optionsy)
            self.game.draw_text("CREDITS", 40, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'GAME':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'SCORES'
            elif self.state == 'SCORES':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'CREDITS'
            elif self.state == 'CREDITS':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'GAME'
        elif self.game.UP_KEY:
            if self.state == 'GAME':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'CREDITS'
            elif self.state == 'SCORES':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'GAME'
            elif self.state == 'CREDITS':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'SCORES'

    def check_input(self):
        self.move_cursor()
        if self.game.ENTER_KEY:
            if self.state == 'GAME':
                self.game.playing = True
            elif self.state == 'SCORES':
                self.game.curr_menu = self.game.score_menu
            elif self.state == 'CREDITS':
                self.game.curr_menu = self.game.credits
            self.run_display = False


class ScoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_input()
            self.game.display.fill(Constants.BACKGROUND)
            self.game.draw_text('SCORES', 80, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 4)
            self.display_scores()
            self.blit_screen()

    def check_input(self):
        self.game.check_events()
        if self.game.ENTER_KEY or self.game.ESC_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

    def display_scores(self):
        height = Constants.DISPLAY_H / 4 + 150
        width = Constants.DISPLAY_W / 4

        self.game.draw_text("NAME", 40, width, height)
        self.game.draw_text("SCORE", 40, width * 2, height)
        self.game.draw_text("TIME(sec)", 40, width * 3, height)

        # TODO: changer la couleur des lignes pour les 3 premiers joueurs (OR, ARGENT, BRONZE)
        for score in self.game.scores.get_best_users():
            height += 50
            self.game.draw_text(str(score.name), 40, width, height)
            self.game.draw_text(str(score.score), 40, width * 2, height)
            self.game.draw_text(str(score.time), 40, width * 3, height)


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_input()
            self.game.display.fill(Constants.BACKGROUND)
            self.game.draw_text('CREDITS', 80, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 4)
            self.game.draw_text('Arthur PELLEGRINI', 40, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 4 + 150)
            self.game.draw_text('Clement BRISSARD', 40, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 4 + 200)
            self.game.draw_text('Osama RAHIM', 40, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 4 + 250)
            self.blit_screen()

    def check_input(self):
        self.game.check_events()
        if self.game.ENTER_KEY or self.game.ESC_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False

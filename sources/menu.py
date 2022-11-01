#!/usr/bin/python
# -*- coding: utf-8 -*-s
import pygame


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 4
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 90

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'GAME'
        self.startx, self.starty = self.mid_w, self.mid_h + 100
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 160
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 220
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Jimanji Rush', 50, self.mid_w, self.mid_h)
            self.game.draw_text("GAME", 25, self.startx, self.starty)
            self.game.draw_text("SCORES", 25, self.optionsx, self.optionsy)
            self.game.draw_text("CREDITS", 25, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'GAME':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'SCORES'
            elif self.state == 'SCORES':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'GAME'
        elif self.game.UP_KEY:
            if self.state == 'GAME':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'SCORES':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'GAME'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'SCORES'

    def check_input(self):
        self.move_cursor()
        if self.game.ENTER_KEY:
            if self.state == 'GAME':
                self.game.playing = True
            elif self.state == 'SCORES':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False


class ScoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text('SCORES', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 30)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.ESC_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            pass
        elif self.game.ENTER_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            pass


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.ENTER_KEY or self.game.ESC_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('CREDITS', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 4)
            self.game.draw_text('Arthur PELLEGRINI', 25, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 4 + 100)
            self.game.draw_text('Clement BRISSARD', 25, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 4 + 160)
            self.game.draw_text('Osama RAHIM', 25, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 4 + 220)
            self.blit_screen()

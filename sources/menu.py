#!/usr/bin/python
# -*- coding: utf-8 -*-s
import pygame

from .constants import Constants


class Menu:
    def __init__(self, game):
        self.game = game
        self.width_center, self.heigth_center = Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 4
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
        self.state = 'PLAY'
        self.pox_x_play, self.pos_y_play = self.width_center, self.heigth_center + 200
        self.pos_x_scores, self.pos_y_scores = self.width_center, self.heigth_center + 250
        self.pos_x_credits, self.pos_y_credits = self.width_center, self.heigth_center + 300
        self.cursor_rect.midtop = (self.pox_x_play + self.offset, self.pos_y_play)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(Constants.BACKGROUND)
            self.game.draw_text("Jimanji Rush", 80, self.width_center, self.heigth_center)
            self.game.draw_text("PLAY", 40, self.pox_x_play, self.pos_y_play)
            self.game.draw_text("SCORES", 40, self.pos_x_scores, self.pos_y_scores)
            self.game.draw_text("CREDITS", 40, self.pos_x_credits, self.pos_y_credits)

            self.game.draw_text("Use ARROWS to select a section and press RETURN to valid", 20, Constants.DISPLAY_W / 2,
                                Constants.DISPLAY_H / 15 * 13)
            self.game.draw_text('Press ESC to quit the game', 20, Constants.DISPLAY_W / 2,
                                Constants.DISPLAY_H / 15 * 14)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.key_pressed.get(pygame.K_DOWN):
            if self.state == 'PLAY':
                self.cursor_rect.midtop = (self.pos_x_scores + self.offset, self.pos_y_scores)
                self.state = 'SCORES'
            elif self.state == 'SCORES':
                self.cursor_rect.midtop = (self.pos_x_credits + self.offset, self.pos_y_credits)
                self.state = 'CREDITS'
            elif self.state == 'CREDITS':
                self.cursor_rect.midtop = (self.pox_x_play + self.offset, self.pos_y_play)
                self.state = 'PLAY'
        elif self.game.key_pressed.get(pygame.K_UP):
            if self.state == 'PLAY':
                self.cursor_rect.midtop = (self.pos_x_credits + self.offset, self.pos_y_credits)
                self.state = 'CREDITS'
            elif self.state == 'SCORES':
                self.cursor_rect.midtop = (self.pox_x_play + self.offset, self.pos_y_play)
                self.state = 'PLAY'
            elif self.state == 'CREDITS':
                self.cursor_rect.midtop = (self.pos_x_scores + self.offset, self.pos_y_scores)
                self.state = 'SCORES'

    def check_input(self):
        self.move_cursor()
        if self.game.key_pressed.get(pygame.K_ESCAPE):
            self.game.running = False
            self.game.current_menu.run_display = False
        if self.game.key_pressed.get(pygame.K_RETURN):
            if self.state == 'PLAY':
                self.game.playing = True
            elif self.state == 'SCORES':
                self.game.current_menu = self.game.score_menu
            elif self.state == 'CREDITS':
                self.game.current_menu = self.game.credits_menu
            self.run_display = False


class ScoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_input()
            self.game.display.fill(Constants.BACKGROUND)
            self.game.draw_text('SCORES', 80, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 12 * 2)
            self.game.draw_text('Press ESC or RETURN to return to Main Menu', 20, Constants.DISPLAY_W / 2,
                                Constants.DISPLAY_H / 15 * 14)

            self.display_scores()
            self.blit_screen()

    def check_input(self):
        self.game.check_events()
        if self.game.key_pressed.get(pygame.K_RETURN) or self.game.key_pressed.get(pygame.K_ESCAPE):
            self.game.current_menu = self.game.main_menu
            self.run_display = False

    def display_scores(self):
        height = Constants.DISPLAY_H / 12 * 5
        width = Constants.DISPLAY_W / 4

        self.game.draw_text("NAME", 40, width, height)
        self.game.draw_text("SCORE", 40, width * 2, height)
        self.game.draw_text("TIME(sec)", 40, width * 3, height)

        for i, score in enumerate(self.game.scores.get_best_users()):
            height += Constants.DISPLAY_H / 12
            color = Constants.WHITE
            if i in range(3):
                if i == 0:
                    color = Constants.GOLD
                if i == 1:
                    color = Constants.SILVER
                if i == 2:
                    color = Constants.BRONZE
                self.game.display.blit(pygame.transform.scale(Constants.ASSETS["MEDAL"][i], (20, 30)),
                                       (width - 150, height - 20))
            self.game.draw_text(str(score.name), 25, width, height, color)
            self.game.draw_text(str(score.score), 25, width * 2, height, color)
            self.game.draw_text(str(score.time), 25, width * 3, height, color)


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.check_input()
            self.game.display.fill(Constants.BACKGROUND)
            self.game.draw_text('CREDITS', 80, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 12 * 3)
            self.game.draw_text('Arthur PELLEGRINI', 30, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 12 * 6)
            self.game.draw_text('Clement BRISSARD', 30, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 12 * 7)
            self.game.draw_text('Osama RAHIM', 30, Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 12 * 8)
            self.game.draw_text('Press ESC or RETURN to return to Main Menu', 20, Constants.DISPLAY_W / 2,
                                Constants.DISPLAY_H / 15 * 14)
            self.blit_screen()

    def check_input(self):
        self.game.check_events()
        if self.game.key_pressed.get(pygame.K_RETURN) or self.game.key_pressed.get(pygame.K_ESCAPE):
            self.game.current_menu = self.game.main_menu
            self.run_display = False

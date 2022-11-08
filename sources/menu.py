#!/usr/bin/python
# -*- coding: utf-8 -*-s
import pygame

from .constants import Constants
from .sprite import Skull


class Menu:
    def __init__(self, game):
        self.game = game
        self.width_center, self.heigth_center = Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 4
        self.background = Constants.ASSETS["BACKGROUND"][2]
        self.run_display = True

    def check_input(self):
        if self.game.key_pressed.get(pygame.K_RETURN) or self.game.key_pressed.get(pygame.K_ESCAPE):
            self.game.current_menu = self.game.main_menu
            self.run_display = False

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def display_content(self):
        pass

    def display(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            if type(self.background) == pygame.Surface:
                self.game.display.fill(Constants.BACKGROUND)
                self.game.display.blit(self.background, (0, 0))
            if type(self.background) == tuple:
                self.game.display.fill(self.background)
            self.display_content()
            self.blit_screen()
            self.game.clock.tick(60)


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'PLAY'
        self.pox_x_play, self.pos_y_play = self.width_center, self.heigth_center + 200
        self.pos_x_scores, self.pos_y_scores = self.width_center, self.heigth_center + 250
        self.pos_x_credits, self.pos_y_credits = self.width_center, self.heigth_center + 300

        self.offset = - 150
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.cursor_rect.midtop = (self.pox_x_play + self.offset, self.pos_y_play)

    def check_input(self):
        self.move_cursor()
        if self.game.key_pressed.get(pygame.K_ESCAPE):
            self.game.running = False
            self.game.current_menu.run_display = False
        if self.game.key_pressed.get(pygame.K_RETURN):
            if self.state == 'PLAY':
                self.game.current_menu = self.game.input_menu
            elif self.state == 'SCORES':
                self.game.current_menu = self.game.score_menu
            elif self.state == 'CREDITS':
                self.game.current_menu = self.game.credits_menu
            self.run_display = False

    def display_content(self):
        self.game.draw_text("Jimanji Rush", 80, (self.width_center, self.heigth_center))
        self.game.display.blit(pygame.transform.scale(Constants.ASSETS["ICON"], (90, 90)),
                               (self.width_center - 55, self.heigth_center - 110))
        self.draw_cursor()
        self.game.draw_text("PLAY", 40, (self.pox_x_play, self.pos_y_play))
        self.game.draw_text("SCORES", 40, (self.pos_x_scores, self.pos_y_scores))
        self.game.draw_text("CREDITS", 40, (self.pos_x_credits, self.pos_y_credits))
        self.game.draw_text("Use ARROWS to select a section and press RETURN to valid", 20,
                            (Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 15 * 13))
        self.game.draw_text('Press ESC to quit the game', 20, (Constants.DISPLAY_W / 2,
                                                               Constants.DISPLAY_H / 15 * 14))

    def draw_cursor(self):
        self.game.draw_text('>', 40, (self.cursor_rect.x, self.cursor_rect.y))

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


class InputMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.input = ""
        self.empty, self.overflow = False, False
        self.iterations = 0

    def check_input(self):
        if self.game.key_pressed.get(pygame.K_ESCAPE):
            self.input = ""
            self.game.current_menu = self.game.main_menu
            self.run_display = False

        if self.game.key_pressed.get(pygame.K_RETURN):

            if self.input == "":
                self.empty = True
            else:
                self.game.playing = True
                self.run_display = False

        if self.game.key_pressed.get(pygame.K_BACKSPACE):
            self.overflow = False
            self.input = self.input[:-1]

        if self.game.unicode != "":
            if len(self.input) < 15:
                self.empty = False
                self.input += self.game.unicode
            else:
                self.overflow = True

    def display_content(self):
        if self.iterations % 60 in range(30):
            cursor = "_"
        else:
            cursor = " "
        self.iterations += 1

        self.game.draw_text("Your name: " + self.input + cursor, 40, (Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 3))

        if self.empty:
            error_text = "Username field can't be empty"
        elif self.overflow:
            error_text = "/!\ Username can't exceed 15 characters"
        else:
            error_text = ""

        self.game.draw_text(error_text, 20, (Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 3 * 2), Constants.RED)
        self.game.draw_text("Press RETURN to play", 20, (Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 15 * 13))
        self.game.draw_text('Press ESC to return to Main Menu', 20, (Constants.DISPLAY_W / 2,
                                                                     Constants.DISPLAY_H / 15 * 14))


class GameOverMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.background = Constants.BLACK
        self.skull = Skull((Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 5 * 2))

    def check_input(self):
        if self.game.key_pressed.get(pygame.K_ESCAPE):
            self.game.current_menu = self.game.main_menu
            self.run_display = False

        if self.game.key_pressed.get(pygame.K_RETURN):
            self.game.current_menu = self.game.main_menu
            self.game.playing = True
            self.run_display = False

    def display_content(self):
        self.skull.animate()
        self.game.display.blit(self.skull.image, self.skull.rect)

        self.game.draw_text('Game Over', 40, (Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 5 * 3))
        self.game.draw_text('Press RETURN to Replay', 20, (Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 15 * 13))
        self.game.draw_text('Press ESC to return to Main Menu', 20,
                            (Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 15 * 14))


class ScoreMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.medals = [pygame.transform.scale(medal, (20, 30)) for medal in Constants.ASSETS["MEDAL"]]
        self.font_color = Constants.WHITE

    def display_content(self):
        self.game.draw_text('SCORES', 80, (Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 12 * 2))
        self.display_scores()
        self.game.draw_text('Press ESC or RETURN to return to Main Menu', 20,
                            (Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 15 * 14))

    def display_scores(self):
        width = Constants.DISPLAY_W / 4
        height = Constants.DISPLAY_H / 12 * 5

        self.game.draw_text("NAME", 40, (width, height))
        self.game.draw_text("SCORE", 40, (width * 2, height))
        self.game.draw_text("TIME(sec)", 40, (width * 3, height))

        for i, score in enumerate(self.game.scores.get_best_users()):
            height += Constants.DISPLAY_H / 12
            if i in range(3):
                self.game.display.blit(self.medals[i], (width - 150, height - 20))
                if i == 0:
                    self.font_color = Constants.GOLD
                elif i == 1:
                    self.font_color = Constants.SILVER
                elif i == 2:
                    self.font_color = Constants.BRONZE
            else:
                self.font_color = Constants.WHITE
            self.game.draw_text(str(score.name), 25, (width, height), self.font_color)
            self.game.draw_text(str(score.score), 25, (width * 2, height), self.font_color)
            self.game.draw_text(str(score.time), 25, (width * 3, height), self.font_color)


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_content(self):
        self.game.draw_text('CREDITS', 80, (Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 12 * 3))
        self.game.draw_text('Arthur PELLEGRINI', 30, (Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 12 * 6))
        self.game.draw_text('Clement BRISSARD', 30, (Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 12 * 7))
        self.game.draw_text('Osama RAHIM', 30, (Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 12 * 8))
        self.game.draw_text('Press ESC or RETURN to return to Main Menu', 20, (
            Constants.DISPLAY_W / 2, Constants.DISPLAY_H / 15 * 14))

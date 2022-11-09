#!/usr/bin/python
# -*- coding: utf-8 -*-s
import random
import re
import threading
import time

import pygame

from .constants import Constants
from .menu import MainMenu, InputMenu, GameOverMenu, ScoreMenu, CreditsMenu
from .score import Score
from .sprite import User, Collectable, CannonBall, Heart, Egg, Star


def wait(sprite_name: str, delta: float) -> None:
    """
    Cette fonction permet de mettre en non disponible un sprite pendant un certain temps afin de limiter son apparition.
    :param sprite_name: le nom du sprite en question.
    :param delta: le temps d'indisponibilité.
    """
    Constants.SPRITE_AVAILABLE[sprite_name] = False

    def wait_and_restore() -> None:
        """
        Cette fonction permet d'attendre le temps spécifié puis de remettre le sprite comme disponible.
        """
        time.sleep(delta)
        Constants.SPRITE_AVAILABLE[sprite_name] = True

    threading.Thread(target=wait_and_restore, daemon=True).start()


def generate_falling_sprites() -> None:
    """
    Cette fonction permet de générer de manière aléatoire le sprite qui va être généré et de l'ajouter à une liste qui
    les contient tous.
    """
    if len(Constants.SPRITES) < Constants.NB_SPRITES:
        luck = random.randint(0, 100)
        if luck in range(0, 35) and Constants.SPRITE_AVAILABLE["CANNONBALL"]:
            Constants.SPRITES.append(CannonBall())
            wait("CANNONBALL", 0.1)
        elif luck in range(35, 40) and Constants.SPRITE_AVAILABLE["HEART"]:
            Constants.SPRITES.append(Heart())
            wait("HEART", 10)
        elif luck in range(40, 45) and Constants.SPRITE_AVAILABLE["EGG"]:
            Constants.SPRITES.append(Egg())
            wait("EGG", 5)
        elif luck in range(45, 50) and Constants.SPRITE_AVAILABLE["STAR"]:
            Constants.SPRITES.append(Star())
            wait("STAR", 5)
        elif luck in range(50, 80) and Constants.SPRITE_AVAILABLE["COIN"]:
            Constants.SPRITES.append(Collectable("COIN"))
            wait("COIN", 0.5)
        elif luck in range(80, 89) and Constants.SPRITE_AVAILABLE["BLUE_GEM"]:
            Constants.SPRITES.append(Collectable("BLUE_GEM"))
            wait("BLUE_GEM", 1)
        elif luck in range(89, 95) and Constants.SPRITE_AVAILABLE["GREEN_GEM"]:
            Constants.SPRITES.append(Collectable("GREEN_GEM"))
            wait("GREEN_GEM", 3)
        elif luck in range(95, 100) and Constants.SPRITE_AVAILABLE["RUBY"]:
            Constants.SPRITES.append(Collectable("RUBY"))
            wait("RUBY", 6)


class Game:
    """
    La classe Game permet la création d'objets qui permettent le bon fonctionnement du jeu.
    """

    def __init__(self):
        """
        Le constructeur de la classe Game.
        """
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

        self.initial_velocity = Constants.VELOCITY
        self.initial_time_increase_difficulty = Constants.TIME_INCREASE_DIFFICULTY
        self.initial_nb_sprites = Constants.NB_SPRITES
        self.cannonball_available, self.heart_available = True, True
        self.egg_available, self.star_available = True, True

        self.main_menu = MainMenu(self)
        self.input_menu = InputMenu(self)
        self.game_over_menu = GameOverMenu(self)
        self.score_menu = ScoreMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.current_menu = self.main_menu

    def check_events(self) -> None:
        """
        Cette méthode permet remplir les variables contenant les touches appuyées par l'utilisateur.
        """
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

    def reset_keys(self, key=None) -> None:
        """
        Cette méthode permet de réinitialiser les variables contenant les touches appuyées par l'utilisateur.
        :param key: la valeur d'une touche qui veut être réinitialisé sans réinitialiser les autres.
        """
        if key is None:
            for key_code in list(self.key_pressed.keys()):
                self.key_pressed[key_code] = False
            self.unicode = ""
        else:
            self.key_pressed[key] = False

    def display_text(self, text: str, size: int, pos: tuple, color: tuple = Constants.WHITE) -> None:
        """
        Cette méthode permet d'afficher du texte sur l'écran.
        :param text: La chaine de caractère correspondante au message qui veut être affiché.
        :param size: La taille du texte sur l'écran.
        :param pos: Un tuple contenant la position en largeur et en hauteur du texte.
        :param color: Un tuple contenant la couleur sous le format RGB.
        """
        font = pygame.font.Font(Constants.ASSETS["FONT"], size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.center = pos
        self.display.blit(text_surface, text_rect)

    def game_loop(self) -> None:
        """
        Cette méthode permet l'exécution en boucle du jeu.
        """
        while self.playing:
            self.check_events()
            self.gameplay()
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
            self.clock.tick(60)
            self.iterations += 1

    def gameplay(self) -> None:
        """
        Cette méthode permet l'exécution d'une image pour le jeu.
        """
        if self.key_pressed.get(pygame.K_ESCAPE) or self.user.hearts == 0:
            self.current_menu = self.main_menu
            if self.user.hearts == 0:
                self.scores.add_user((self.user.username, self.user.score, self.user.time))
                self.current_menu = self.game_over_menu
            self.playing = False

        self.display.blit(Constants.ASSETS["BACKGROUND"][0], (0, 0))
        self.increase_difficulty()
        self.user.update_time()
        generate_falling_sprites()
        self.display_sprites()
        self.display_monitor()
        self.reset_keys(key=pygame.K_ESCAPE)

    def reset_gameplay(self) -> None:
        """
        Cette méthode permet de réinitialiser les variables de position, ou encore de score propre à chaque partie.
        """
        self.user.reset_all()
        self.user.reset_position()
        self.user.start_time = pygame.time.get_ticks()
        Constants.SPRITES.clear()
        Constants.VELOCITY = self.initial_velocity
        Constants.TIME_INCREASE_DIFFICULTY = self.initial_time_increase_difficulty
        Constants.NB_SPRITES = self.initial_nb_sprites

    def increase_difficulty(self) -> None:
        """
        Cette méthode permet d'augmenter la vitesse de déplacements des sprites mais aussi le nombre de sprites présents
        sur l'écran afin d'augmenter la difficulté.
        """
        if self.user.time >= Constants.TIME_INCREASE_DIFFICULTY:
            if Constants.NB_SPRITES < 10:
                Constants.NB_SPRITES += 1
            Constants.VELOCITY += 2
            Constants.TIME_INCREASE_DIFFICULTY += 50

    def display_sprites(self) -> None:
        """
        Cette méthode permet l'affichage des instances de sprites qui sont impliquées dans le jeu (Player, Pièces,
        Boulets de canon, ...).
        """
        for sprite in Constants.SPRITES:
            if not sprite.check_if_visible():
                Constants.SPRITES.remove(sprite)
            else:
                sprite.collide(self.user)
                sprite.fall()
                sprite.animate()
            self.display.blit(sprite.image, sprite.rect)
        self.user.move(self.key_pressed)
        self.display.blit(self.user.image, self.user.rect)

    def display_monitor(self) -> None:
        """
        Cette méthode permet d'afficher des informations sur la partie en cours (Score, Temps, Nombre de vies).
        """
        self.display_text("Score: " + str(self.user.score), 30, (Constants.DISPLAY_W / 6, Constants.DISPLAY_H / 15))
        self.display_text("Time: " + str(self.user.time), 30, (Constants.DISPLAY_W / 6 * 3, Constants.DISPLAY_H / 15))
        self.display_text("Heart: " + str(self.user.hearts), 30,
                          (Constants.DISPLAY_W / 6 * 5, Constants.DISPLAY_H / 15))

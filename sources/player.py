#!/usr/bin/python
# -*- coding: utf-8 -*-s
import pygame
import threading
import time

from .constants import Constants
from .sprite import Sprite


class Player(Sprite):
    """
    Définie toutes les actions que peut effectuer le joueur (courir de droite à gauche).
    """

    def __init__(self):
        """
        Le constructeur de la classe Player.
        """
        super().__init__("PLAYER")
        self.rate = 4
        self.velocity = 10  # vitesse de l'utilisateur
        self.rect = self.image.get_rect()
        self.reset_position()
        self.margin = 10
        self.egg, self.star = False, False

    def reset_position(self):
        """
        Permet d'initialiser à partir des coordonnées la position de départ du joueur.
        :return: None.
        """
        self.rect.center = (Constants.DISPLAY_W / 9, Constants.DISPLAY_H / 10 * 8)

    def move(self, key_pressed: dict):
        """
        Fonction utilisée dans la classe Game qui permet d'appeler nos fonctions move_left & right si les touches
        flèche gauche ou flèche droite sont pressées. Sinon le personnage ne bouge pas et obtient l'animation statique.
        :param key_pressed: Contient les touches pressées par l'utilisateur.
        :return: None.
        """
        if key_pressed.get(pygame.K_LEFT):
            self.move_left()

        elif key_pressed.get(pygame.K_RIGHT):
            self.move_right()
        else:
            self.image = Constants.ASSETS["IDDLE"][0]

    def move_left(self):
        """
        Permet au joueur de se déplacer vers la gauche quand la flèche gauche du clavier est pressée.
        :return: None.
        """
        self.animate(reverse=True)
        if self.rect.x - self.velocity > self.margin:
            self.rect.x -= self.velocity
        else:
            self.rect.x = self.margin

    def move_right(self):
        """
        Permet au joueur de se déplacer vers la droite quand la flèche droite du clavier est pressée.
        :return: None.
        """
        self.animate()
        if self.rect.x + self.velocity < Constants.DISPLAY_W - self.margin:
            self.rect.x += self.velocity
        else:
            self.rect.x = Constants.DISPLAY_W - self.margin

    def increase_velocity(self):
        """
        Ajoute 5 à la variable velocity quand le joueur récolte une étoile.
        :return: None.
        """
        self.star = True
        self.velocity += 5

        def wait_and_restore():
            time.sleep(5)
            self.velocity -= 5
            self.star = False

        threading.Thread(target=wait_and_restore).start()

    def decrease_velocity(self):
        """
        Baisse de 5 la variable quand le joueur se prend un œuf sur la tête.
        :return:
        """
        self.egg = True
        self.velocity -= 5

        def wait_and_restore():
            time.sleep(5)
            self.velocity += 5
            self.egg = False

        threading.Thread(target=wait_and_restore).start()

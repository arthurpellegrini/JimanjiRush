#!/usr/bin/python
# -*- coding: utf-8 -*-s
import random
import threading
import time

import pygame

from .constants import Constants


class Sprite(pygame.sprite.Sprite):
    """
    Cette classe permet de définir le fonctionnement d'un sprite dans le jeu.
    """
    def __init__(self, name: str):
        """
        Le constructeur de la classe Sprite.
        :param name: la clef correspond au sprite dans le dictionnaire des assets.
        """
        super().__init__()
        self.name = name
        self.current_image = 0
        self.images = [f.convert_alpha() for f in Constants.ASSETS[name]]
        self.image = self.images[0]
        self.margin = 25
        self.ground_height = 100 + self.margin
        self.rect = self.image.get_rect()
        self.velocity = Constants.VELOCITY
        self.rate = 8  # vitesse du changement d'image dans l'animation

    def animate(self, reverse=False) -> None:
        """
        Cette méthode permet de changer l'image afin de donner l'impression que le sprite est animé.
        :param reverse: si la valeur est à True, elle permet de mettre en place l'animation inverse.
        """
        self.image = self.images[self.current_image // self.rate % len(self.images)]
        if reverse:
            self.image = pygame.transform.flip(self.image, True, False)
        self.current_image += 1

    def fall(self) -> None:
        """
        Cette méthode permet de modifier la position du sprite afin de donner l'impression que celui-ci tombe.
        """
        self.velocity = Constants.VELOCITY // 2
        self.rect.y += self.velocity

    def check_if_visible(self) -> bool:
        """
        Cette méthode permet de savoir si le sprite est présent sur l'écran.
        :return: un booléen correspondant au fait que le sprite soit présent ou non sur l'écran de jeu.
        """
        if self.rect.y >= Constants.DISPLAY_H - self.ground_height:
            return False
        return True

    def collide(self, sprite: pygame.sprite.Sprite) -> None:
        """
        Cette méthode permet de détecter la collision du sprite avec un autre sprite
        :param sprite: un objet correspondant à l'autre sprite.
        """
        pass


class Player(Sprite):
    """
    Cette classe permet de définir les spécificités du sprite d'un joueur.
    """
    def __init__(self):
        """
        Le constructeur de la classe Player.
        """
        super().__init__("PLAYER")
        self.rate //= 2
        self.reset_position()
        self.left, self.right = False, False
        self.egg, self.star = False, False
        self.last_velocity = 0

    def reset_position(self) -> None:
        """
        Cette méthode permet de réinitialiser la position du joueur sur l'écran.
        """
        self.rect.center = (Constants.DISPLAY_W / 9, Constants.DISPLAY_H - self.ground_height)

    def move(self, key_pressed: dict) -> None:
        """
        Cette méthode permet de modifier la position du joueur en fonction des touches pressées par l'utilisateur.
        :param key_pressed: un dictionnaire contenant les touches appuyées par l'utilisateur.
        """
        if key_pressed.get(pygame.K_LEFT):
            self.left, self.right = True, False
            self.move_left()

        elif key_pressed.get(pygame.K_RIGHT):
            self.left, self.right = False, True
            self.move_right()
        else:
            self.image = Constants.ASSETS["IDDLE"][0]
            if self.left and not self.right:
                self.image = pygame.transform.flip(self.image, True, False)

    def move_left(self) -> None:
        """
        Cette méthode permet de mettre à jour la position et l'image du joueur si le déplacement est vers la gauche.
        """
        self.animate(reverse=True)
        if self.rect.x - self.velocity > self.margin:
            self.rect.x -= self.velocity
        else:
            self.rect.x = self.margin

    def move_right(self) -> None:
        """
        Cette méthode permet de mettre à jour la position et l'image du joueur si le déplacement est vers la droite.
        """
        self.animate()
        if self.rect.x + self.velocity < Constants.DISPLAY_W - self.margin - self.rect.width:
            self.rect.x += self.velocity
        else:
            self.rect.x = Constants.DISPLAY_W - self.margin - self.rect.width

    def increase_velocity(self) -> None:
        """
        Cette méthode permet d'augmenter la vitesse du joueur lorsqu'une étoile a été touchée.
        """
        self.star = True
        self.last_velocity = self.velocity
        self.velocity *= 1.5

        def wait_and_restore() -> None:
            """
            Cette fonction permet d'attendre 2s puis de rendre à nouveau disponible l'utilisation d'une étoile.
            """
            time.sleep(2)
            self.velocity = self.last_velocity
            self.star = False

        threading.Thread(target=wait_and_restore, daemon=True).start()

    def decrease_velocity(self) -> None:
        """
        Cette méthode permet de diminuer la vitesse du joueur lorsqu'un œuf a été touché.
        """
        self.egg = True
        self.last_velocity = self.velocity
        self.velocity *= 0.5

        def wait_and_restore() -> None:
            """
            Cette fonction permet d'attendre 2s puis de rendre à nouveau disponible l'utilisation d'un œuf.
            """
            time.sleep(2)
            self.velocity = self.last_velocity
            self.egg = False

        threading.Thread(target=wait_and_restore, daemon=True).start()


class User(Player):
    """
    Cette classe permet de créer un utilisateur.
    """
    def __init__(self):
        """
        Le constructeur de la classe User.
        """
        super().__init__()
        self.available = True
        self.username = ""
        self.score = 0
        self.start_time = 0
        self.time = 0
        self.hearts = 3

    def update_time(self) -> None:
        """
        Cette méthode permet de mettre à jour le temps du joueur pour une partie.
        """
        self.time = (abs(self.start_time - pygame.time.get_ticks())) // 1000

    def reset_name(self) -> None:
        """
        Cette méthode permet de réinitialiser le nom du joueur.
        """
        self.username = ""

    def reset_all(self) -> None:
        """
        Cette méthode permet de réinitialiser les attributs du joueur spécifique à une partie en particulier.
        """
        self.score = 0
        self.time = 0
        self.hearts = 3


class Collectable(Sprite):
    """
    Cette classe permet de définir les objets collectibles par l'utilisateur(Pièce, Gemme Bleue, Gemme Verte et Ruby).
    """

    def __init__(self, name: str):
        """
        Le constructeur de la classe Collectable.
        :param name: le nom correspondant au collectible.
        """
        super().__init__(name)
        self.rect.x = Constants.DISPLAY_W // 9 * random.randint(1, 9) - self.margin - self.rect.width
        self.rect.y = - random.randint(0, Constants.DISPLAY_H // 9)

    def collide(self, user: User) -> None:
        """
        Cette méthode permet de détecter la collision du sprite avec le joueur et d'effectuer les actions
        correspondantes si tel est le cas.
        :param user: un objet user correspondant au sprite du joueur.
        """
        if self.rect.colliderect(user.rect):
            Constants.SPRITES.remove(self)
            if self.name == "COIN":
                user.score += Constants.SCORE_VALUE * 5

            elif self.name == "BLUE_GEM":
                user.score += Constants.SCORE_VALUE * 10

            elif self.name == "GREEN_GEM":
                user.score += Constants.SCORE_VALUE * 40

            elif self.name == "RUBY":
                user.score += Constants.SCORE_VALUE * 80


class CannonBall(Sprite):
    """
    Cette classe permet de définir des objets correspondants aux boulets de canon.
    """

    def __init__(self):
        """
        Le constructeur de la classe CannonBall.
        """
        super().__init__("CANNONBALL")
        self.rect.x = Constants.DISPLAY_W // 9 * random.randint(1, 9) - self.margin - self.rect.width
        self.rect.y = - random.randint(0, Constants.DISPLAY_H // 9)

    def collide(self, user: User) -> None:
        """
        Cette méthode permet de détecter la collision du sprite avec le joueur et d'effectuer les actions
        correspondantes si tel est le cas.
        :param user: un objet user correspondant au sprite du joueur.
        """
        if self.rect.colliderect(user.rect):
            Constants.SPRITES.remove(self)
            if user.hearts > 0 and user.available:
                user.available = False

                def wait_and_restore():
                    """
                    Cette fonction permet d'attendre 1s puis de remettre la variable heart du joueur disponible à la
                    modification.
                    """
                    time.sleep(1)
                    user.available = True

                user.hearts -= 1
                threading.Thread(target=wait_and_restore, daemon=True).start()


class Heart(Sprite):
    """
    Cette classe permet de définir des sprites correspondants aux cœurs.
    """

    def __init__(self):
        """
        Le constructeur de la classe Heart.
        """
        super().__init__("HEART")
        self.rect.x = Constants.DISPLAY_W // 9 * random.randint(1, 9) - self.margin - self.rect.width
        self.rect.y = - random.randint(0, Constants.DISPLAY_H // 9)

    def collide(self, user: User) -> None:
        """
        Cette méthode permet de détecter la collision du sprite avec le joueur et d'effectuer les actions
        correspondantes si tel est le cas.
        :param user: un objet user correspondant au sprite du joueur.
        """
        if self.rect.colliderect(user.rect):
            Constants.SPRITES.remove(self)
            if user.hearts < 3:
                user.hearts += 1


class Egg(Sprite):
    """
    Cette classe permet de définir des sprites correspondant aux œufs.
    """

    def __init__(self):
        """
        Le constructeur de la classe Egg.
        """
        super().__init__("EGG")
        self.rect.x = Constants.DISPLAY_W // 9 * random.randint(1, 9) - self.margin - self.rect.width
        self.rect.y = - random.randint(0, Constants.DISPLAY_H // 9)

    def collide(self, user: User) -> None:
        """
        Cette méthode permet de détecter la collision du sprite avec le joueur et d'effectuer les actions
        correspondantes si tel est le cas.
        :param user: un objet user correspondant au sprite du joueur.
        """

        if self.rect.colliderect(user.rect):
            Constants.SPRITES.remove(self)
            if not user.egg and not user.star:
                user.decrease_velocity()
            else:
                if user.score >= Constants.SCORE_VALUE:
                    user.score -= Constants.SCORE_VALUE


class Star(Sprite):
    """
    Cette classe permet de définir le sprite correspondant à une étoile.
    """

    def __init__(self):
        """
        Le constructeur de la classe Star.
        """
        super().__init__("STAR")
        self.rect.x = Constants.DISPLAY_W // 9 * random.randint(1, 9) - self.margin - self.rect.width
        self.rect.y = - random.randint(0, Constants.DISPLAY_H // 9)

    def collide(self, user: User) -> None:
        """
        Cette méthode permet de détecter la collision du sprite avec le joueur et d'effectuer les actions
        correspondantes si tel est le cas.
        :param user: un objet user correspondant au sprite du joueur.
        """
        if self.rect.colliderect(user.rect):
            Constants.SPRITES.remove(self)
            if not user.star and not user.egg:
                user.increase_velocity()
            else:
                user.score += Constants.SCORE_VALUE


class Skull(Sprite):
    """
    Cette classe permet de créer un sprite correspondant à une tête de mort.
    """

    def __init__(self, pos: tuple):
        """
        Le constructeur de la classe Skull.
        :param pos: un tuple contenant la position du sprite sur l'écran.
        """
        super().__init__("SKULL")
        self.rect.center = pos

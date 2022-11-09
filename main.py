#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

import pygame

from sources import Game, Constants


def get_assets() -> dict:
    """
    Cette fonction permet la récupération des éléments graphiques du jeu.
    :return: un dictionnaire contenant ces éléments sous forme d'objets pygame.
    """
    root = os.path.abspath("assets/")
    assets = {}

    for elem in os.listdir(root):  # Boucle dans les éléments contenus dans le dossier /assets
        # On récupère le chemin du dossier parent (background, player, ...)
        parent_elem_path = os.path.join(root, elem)

        if os.path.isdir(parent_elem_path):  # Si l'élément est un dossier
            # On récupère le nom du dossier en majuscule pour l'index du dictionnaire
            parent_elem_dir_name = os.path.basename(parent_elem_path).upper()
            # On instancie le tableau qui va contenir les images
            assets[parent_elem_dir_name] = []

            # On boucle sur les éléments d'un sous dossier de /assets (éléments de /assets/player)
            for sub_elem in os.listdir(parent_elem_path):
                # On récupère le chemin du fichier
                sub_parent_elem_path = os.path.join(parent_elem_path, sub_elem)
                # On ajoute l'élément au tableau sous la forme d'une image Pygame
                image = pygame.image.load(sub_parent_elem_path)
                if parent_elem_dir_name == "PLAYER":
                    image = pygame.transform.scale(image, (21 * 6, 33 * 6))
                elif parent_elem_dir_name == "IDDLE":
                    image = pygame.transform.scale(image, (17 * 6, 31 * 6))
                elif parent_elem_dir_name == "SKULL":
                    image = pygame.transform.scale(image, (62 * 3, 75 * 3))
                elif parent_elem_dir_name == "BACKGROUND":
                    image = pygame.transform.scale(image, (Constants.DISPLAY_W, Constants.DISPLAY_H))
                elif parent_elem_dir_name != "MEDAL":
                    image = pygame.transform.scale(image, (36 * 1.5, 45 * 1.5))
                assets[parent_elem_dir_name].append(image)

        else:  # Sinon on sait que c'est la police
            if parent_elem_path.split(".")[-1] == "ttf":
                assets["FONT"] = parent_elem_path
            if parent_elem_path.split(".")[-1] == "png":
                assets["ICON"] = pygame.image.load(parent_elem_path)
    return assets


if __name__ == "__main__":
    Constants.ASSETS = get_assets()
    game = Game()

    while game.running:
        game.current_menu.display()
        game.game_loop()

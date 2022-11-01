#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pygame

from sources import Game, Score, UserScore


def get_assets() -> dict:
    """
    Cette fonction permet la récupération des éléments graphiques du jeu.
    :return: un dictionnaire contenant toutes les images et la police du dossier assets.
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
                assets[parent_elem_dir_name].append(pygame.image.load(sub_parent_elem_path))

        else:  # Sinon on sait que c'est la police
            if parent_elem_path.split(".")[-1] == "TTF":  # Si c'est un fichier TTF
                assets["FONT"] = parent_elem_path
    return assets


if __name__ == "__main__":
    game = Game(get_assets())

    while game.running:
        game.curr_menu.display_menu()
        game.game_loop()

    # MODIFY SCORE
    # score = Score()
    # score.add_user(UserScore("XXXXXXXXXXXXXXXXXXXX", 9828, 1000.0))
    # score.write_score_file()



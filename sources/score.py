#!/usr/bin/python
# -*- coding: utf-8 -*-s
class UserScore:
    """
    La classe UserScore permet de créer un objet qui contient un nom, un score et une durée de jeu qui lui est associé.
    """
    def __init__(self, name: str, score: int, time: int):
        """
        Le constructeur de la classe UserScore.
        :param name: Le nom du joueur.
        :param score: Le nombre de points qu'il a obtenu durant sa partie.
        :param time: Son temps de survie lors de sa partie.
        """
        self.name = name
        self.score = score
        self.time = time

    def __str__(self) -> str:
        """
        Permet l'affichage d'un objet UserScore sous la forme d'une chaine de caractères.
        :return: la chaine de caractère correspondante.
        """
        return f"{self.name},{self.score},{self.time}\n"


class Score:
    """
    La classe Score permet de créer un objet qui contient les différents scores réalisés sur le jeu.
    """
    def __init__(self):
        """
        Le constructeur de la classe Score.
        """
        self.users = []
        self.score_file_path = "data/scores.csv"
        self.get_score_file()

    def add_user(self, user: UserScore) -> None:
        """
        Cette fonction permet d'ajouter des données sur un utilisateur qui a réalisé un score lors d'une partie.
        :param user: Un objet UserScore qui contient le nom, le score et le temps de jeu du joueur.
        :return: None.
        """
        self.users.append(user)
        self.sort_users()

    def sort_users(self) -> None:
        """
        Cette fonction permet de trier la liste qui contient les données sur les parties des joueurs.
        :return: None.
        """
        self.users.sort(key=lambda user: user.score, reverse=True)

    def get_best_users(self):
        """
        Permet d'obtenir les 5 meilleurs joueurs.
        :return: Une liste contenant les 5 joueurs qui ont enregistré les meilleurs scores.
        """
        return self.users[0:5]

    def get_score_file(self) -> None:
        """
        Permet de récupérer les informations des utilisateurs stockées dans un fichier CSV.
        Ces informations seront stockées dans un attribut de l'objet score.
        :return: None.
        """
        with open(self.score_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for raw_line in lines:
            line = raw_line.split(",")
            user = UserScore(line[0], int(line[1]), int(line[2]))
            self.add_user(user)

    def write_score_file(self) -> None:
        """
        Permet de d'écrire les scores enregistrés dans le fichier CSV.
        :return: None.
        """
        with open(self.score_file_path, 'w', encoding='utf-8') as file:
            file.write(self.__str__())

    def __str__(self) -> str:
        """
        Permet l'affichage d'un objet Score sous la forme d'une chaine de caractères.
        :return: la chaine de caractère correspondante.
        """
        output = ""
        for user in self.users:
            output += user.__str__()
        return output

#!/usr/bin/python
# -*- coding: utf-8 -*-s
class UserScore:
    def __init__(self, name: str, score: int, time: int):
        self.name = name
        self.score = score
        self.time = time

    def __str__(self):
        return f"{self.name},{self.score},{self.time}\n"


class Score:
    def __init__(self):
        self.users = []
        self.score_file_path = "data/scores.csv"
        self.get_score_file()

    def add_user(self, user: UserScore):
        self.users.append(user)
        self.sort_users()

    def sort_users(self):
        self.users.sort(key=lambda user: user.score, reverse=True)

    def get_best_users(self):
        """
        Permet d'obtenir les 5 meilleurs joueurs
        :return: Une liste des meilleurs joueurs
        """
        return self.users[0:5]

    def get_score_file(self):
        """
        Permet de récupérer les informations des utilisateurs stockées dans un fichier CSV
        La fonction reader renvoie les données de l'utilisateur sous forme d'une liste de Str
        : return: une liste de liste contenant les informations des utilisateurs
        """
        with open(self.score_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        for raw_line in lines:
            line = raw_line.split(",")
            user = UserScore(line[0], int(line[1]), int(line[2]))
            self.add_user(user)

    def write_score_file(self):
        with open(self.score_file_path, 'w', encoding='utf-8') as file:
            file.write(self.__str__())

    def __str__(self):
        output = ""
        for user in self.users:
            output += user.__str__()
        return output

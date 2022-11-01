import csv

valueItem = {
    "piece": 10,
    "emeraude": 500,
    "rubis": 1000,
    "bombe": 550,  # perte de 550 sur le score et 1 vie
}


def download_users_from_csv():
    """
    Permet de récupérer les informations des utilisateurs stockées dans un fichier CSV
    La fonction reader renvoie les données de l'utilisateur sous forme d'une liste de Str
    : return: une liste de liste contenant les informations des utilisateurs
    """
    with open("../data/scores.csv", 'r', encoding='utf-8') as f:
        # Créer un objet csv à partir du fichier
        obj = csv.reader(f)
        list_score = []
        for ligne in obj:
            list_score.append(ligne)
        f.close()
        return list_score


def create_user_in_csv(name: str, score: int, distance: int):
    """
    Ouvrir le fichier en mode écriture avec "a" qui permet de ne pas effacer le contenu comme avec "w"
    mais écrit sur une nouvelle ligne en partant de la fin du fichier
    :param name: nom de l'utilisateur
    :param score: score de l'utilisateur dans une partie
    :param distance: distance parcourue par le joueur dans une partie
    :return: /
    """
    fichier = open('../data/scores.csv', 'a')
    obj = csv.writer(fichier, dialect='excel')
    obj.writerow([name, str(score), str(distance)])
    fichier.close()


def update_users_in_csv(new_list_of_users: list):
    """
    TODO
    pas de méthode CSV permettant une suppression de ligne ou une update de ligne dans le fichier csv du moins à
    partir de la biblio CSV donc obligé de réécrire le fichier à partir de la liste utilisateur contenant
    les nouvelles valeurs
    L'élément newline permet de ne pas écrire une ligne vide après l'ajout d'une valeur par writerow
    :param new_list_of_users: contient l'ensemble des informations des joueurs, comme un fichier CSV
    :return: /
    """
    with open('../data/scores.csv', 'w', newline='') as fichier:
        fichier = csv.writer(fichier)  # this is the writer object
        for ligne in new_list_of_users:
            fichier.writerow(ligne)  # this is the data


class ScoreUser:

    def __init__(self, name):
        self.name = name  # non implémenté dans les fonctions
        self.fichier_score = download_users_from_csv()
        self.score_joueur_actuel = 0
        self.distance_joueur_actuel = 0
        self.time = 0  # non implémenté dans les fonctions

    def sort_users_by_stronger(self):
        """
        Fonction qui trie les utilisateurs en fonction du score de manière décroissant
        :return: Une liste triée du meilleur joueur au moins bon
        """
        sort_list = self.fichier_score
        for i in range(len(sort_list) - 1):
            for j in range(i + 1, len(sort_list)):
                if int(sort_list[i][1]) < int(sort_list[j][1]):
                    temp = sort_list[i]
                    sort_list[i] = sort_list[j]
                    sort_list[j] = temp
        return sort_list

    def get_users_all(self):
        """
        Permet d'obtenir les scores de tous les joueurs de manière triée
        :return: La liste de tous les joueurs ayant rentré leur score
        """
        return self.sort_users_by_stronger()

    def get_users_top(self):
        """
        Permet d'obtenir les 5 meilleurs joueurs
        :return: Une liste des meilleurs joueurs
        """
        return self.sort_users_by_stronger()[0:5]

    def get_user(self, name):
        """
        Permet d'avoir les performances d'un joueur en particulier
        :param name: pseudo de l'utilisateur
        :return: une liste contenant les informations du joueur ["name", "score", "durée"]
        """
        for user in self.fichier_score:
            if user[0] == name:
                return user

    def create_user(self, name, score, distance):
        """
        Fonction permettant la création d'un utilisateur si ce dernier n'existe pas.
        Si l'utilisateur existe, on appelle la fonction update_user
        :param name: nom de l'utilisateur
        :param score: score de l'utilisateur
        :param distance: distance parcourue par le joueur dans une partie
        :return: /
        """
        if self.get_user(name) is None:
            self.fichier_score.append([name, str(score), str(distance)])  # ajoute à la liste fichier_score
            create_user_in_csv(name, score, distance)  # ajoute au fichier csv
        else:
            self.update_user(name, score, distance)

    def update_user(self, name, score, distance):
        """
        Fonction permettant la modification du score d'un utilisateur.
        Cette modification se fait si l'utilisateur a amélioré son score par rapport à celui stocké dans le CSV
        :param name: nom de l'utilisateur
        :param score: score de l'utilisateur
        :param distance: distance parcourue par le joueur dans une partie
        :return: /
        """
        # Vérifie si le score est plus élevé ou non, sinon ne pas modifier
        if int(self.get_user(name)[1]) < score:
            self.delete_user(name)
            self.create_user(name, score, distance)
            update_users_in_csv(self.fichier_score)  # permet de réécrire le csv avec les modifications appliquées

    def delete_user(self, name):
        """
        Permet de supprimer les données d'un joueur dans le CSV
        :param name: nom de l'utilisateur
        :return: /
        """
        self.fichier_score.remove(self.get_user(name))
        update_users_in_csv(self.fichier_score)  # permet de réécrire le csv avec les modifications appliquées
        # appeler la fonction update_users_in_csv pour appliquer une supression


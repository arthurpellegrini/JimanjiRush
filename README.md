Jimanji Rush
==============================================================

[![Version Python][python]](https://www.python.org/downloads/release/python-3100/)

[![Pycharm][pycharm]](https://www.jetbrains.com/fr-fr/pycharm/download/#section=windows)

Description
--------------------------------------------------------------
Ce projet a été réalisé dans le cadre du module Python de notre formation d'ingénieur en Informatique et Application à 
l'ESIEE-IT. Jimanji Rush est un jeu 2D dans lequel le joueur doit éviter des boulets de canons qui tombent.

Voici les outils utilisés pour le développement de cette application : 
* Python (en sa version 3.10) ainsi que la librairie Pygame
* PyCharm
* Github

Commandes
--------------------------------------------------------------
Lancer le projet
````shell
python main.py
````

Pour créer un exécutable dans le dossier 'build' :
```shell
python setup.py build
```
L'exécutable sera créé dans un des sous-dossiers de "build" suivant la version de l'application (Windows, Linux, MacOS).

<u>Attention</u> : le script setup.py a été conçu pour un système Windows, par conséquent, il faudra modifier ce script
afin de le faire fonctionner pour un autre système, tel que Linux/MacOS.

Pour générer la documentation html : 
```shell
cd docs
sphinx-apidoc -o .\source\ ..\
sphinx-build -b html .\source\  html
```

Ensuite rendez-vous dans "docs\html" et lancez le fichier "index.html", afin de pouvoir visualiser la documentation.




Fonctionnalités
--------------------------------------------------------------
L'utilisateur incarne un joueur qui peut se déplacer sur un axe horizontal et suivant la situation esquiver ou prendre
des items qui tomberont du ciel.

Voici la liste des items:

* Boulet de Canon : - 1 ❤
* Coeur           : + 1 ❤

* Étoile          : ↗️Vitesse pendant 2 secondes ️
* Oeuf            : ↙️Vitesse pendant 2 secondes
 /!\️Si un œuf ou une étoile est récupérée durant la période de l'effet celui-ci pourra respectivement faire perdre 
ou gagner des points au score.

* Pièces          : valeur standard
* Gemme Bleue     : 2 fois plus qu'une pièce
* Gemme Verte     : 8 fois plus qu'une pièce
* Gemme Rouge     : 16 fois plus qu'une pièce

Au fur à mesure de la partie, la quantité ainsi que la vitesse des objets pourra être amenée à augmenter. De plus, un 
système de chance a été mis en place afin de limiter l'apparition de certains items.

[//]: # (BADGES)
[python]: https://img.shields.io/badge/Python-3.10-FFC300?style=for-the-badge&logo=python
[pycharm]: https://img.shields.io/badge/PyCharm-2022.2.3-7ce473?style=for-the-badge&logo=pycharm

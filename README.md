# Projet Q-Learning

Ce projet utilise que des bibliothèques standards de python, il n'y aucun package supplémentaire à installer.

## Lancement du programme

### Exécution

Pour exécuter le programme, il faut lancer la commande :

```bash
python3 GUI.py
```

### Fichier labyrinthe.csv

Le programme se lance sur le labyrinthe labyrinthe.csv présent avec les sources du projet. Il n'est pas encore possible d'ourvir un fichier depuis l'interface graphique mais il est possible de modifier le fichier directement, sachant que le fichier est codé de la manière suivante :

* 0 = mur
* 1 = départ
* 2 = arrivée
* -1 = chemin
* -n = poids du piège avec n>1

### Rafraichissement interface graphique

Pour ralentir la vitesse du robot qui défile dans le labyrinthe, il faut modifier le code à la main en remplacant la valeur :

```python
sleep(0.0001)
```

Présent dans le fichier QLearning.py à la ligne 49 par une autre valeur en seconde.

## Stratégie utilisée

La stratégie utilisée dans notre algorithme du Q-Learning peut être directement tuné via l'interface graphique.

Par défaut, on favorise l'exploration au départ puis converge vers de l'exploitation. Le changement est régie par une loi exponentielle en fonction du nombre d'itération en cours afin de favoriser l'eploration au départ puis on fait tendre l'exponentielle vers zéro pour laisser la place à l'exploitation.

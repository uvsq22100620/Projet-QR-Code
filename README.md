# Projet-QR-Code- IN202

# LE CORRE Camille
# LEFEVRE Laura
# COUSTILLAS Laurédane
# LDDBI


### Présentation du projet:

Ce projet a pour objectif de créer un programme qui permette la lecture d'un QR Code. Ce programme est écrit en python et utilise l'interface Tkinter pour charger un QR Code et le lire. Le programme est constitué de nombreuses fonctions qui permettent de charger un QR Code, de le vérifier puis de lire son contenu.


### Qu'est-ce qu'un QR Code :

Un QR Code est une sorte de code-barres avec des informations stockées à l'intérieur sous formes binaires, afin qu'elles puissent être lues par un ordinateur. Il est constitué de pixels noirs et blancs dans une matrice et possèdent 3 carrés noirs entourés d'une bande blanche dans chaque coin, sauf celui en bas à droite, ce qui permet à l'ordinateur de détecter son sens de lecture. Il y a également un ligne de pointillés qui relient les 2 carrés à gauches et les 2 carrés en haut.


### La lecture du QR Code:

La lecture d'un QR Code s'effectue par bloc de 14 bits. Le premier bloc qui doit être lu se trouve en bas à droite du QR Code, puis on lit le bloc se trouvant à sa gauche, puis celui au dessus de ce dernier, celui à droite, et ainsi de suite.
Le QR Code contient au maximum 16 blocs (le nombre de blocs à décoder est codé en binaire sur 5 bits se trouvant entre les carrés de gauche).

Chaque bloc est constitué de 14 bits (2 fois 7 bits) auxquels on applique un code de correction d'erreur de Hamming(7,4). Chaque bloc est donc composé de 2 fois 4 bits codants (car il y a 2 fois 3 bits de parité pour chaque bloc).

Le pixel à la position (24, 8) code le type de données. S’il est à 0 il s’agit de données numériques : 8 bits codent deux symboles hexadécimaux. S’il est à 1, il s’agit de données brutes, 8 bits seront interprétés comme un code ASCII.

Enfin, on peut appliquer un filtre à notre QR Code, qui modifie certains bits du QR Code. Celui-ci est stocké sur deux bits de contrôle dans les pixels (22, 8) et (23, 8). Quatre filtres différents peuvent être appliqué : un tout noir (qui ne change), un damier, des lignes horizontales ou bien des lignes verticales.


### Interface graphique:

La fenêtre Tkinter est constituée des boutons charger (qui permet d'importer un QR Code dans l'interface), scanner (qui permet de lire le QR Code) et quitter.
Quand un QR Code est lu, des informations sont renvoyées comme le message décodé, le filtre appliqué, le nombre de blocs lus et le type de données.
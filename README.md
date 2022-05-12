# Projet-QR-Code
Projet IN 202 QR Code
# LE CORRE Camille
# LEFEVRE Laura
# COUSTILLAS Laurédane
# LDDBI

Lecture d'un QR Code:

Ce projet a pour objectif de créer un programme qui permette la lecture d'un QR Code. Ce programme est écrit en python et utilise l'interface Tkinter pour charger un QR Code et le lire. Le programme est constitué de nombreuses fonctions qui permettent de charger un QR Code, de le vérifier puis de lire son contenu en le scannant.

Qu'est-ce qu'un QR Code :

Un QR Code est une sorte de code-barres avec des informations stockées à l'intérieur sous formes binaires, afin qu'elles puissent être lues par un ordinateur. Il est constitué de pixels noirs et blancs dans une matrice et possèdent 3 carrés noirs entourés d'une bande blanche dans chaque coin, sauf celui en bas à droite, ce qui permet à l'ordinateur de détecter son sens de lecture. Il y a également un ligne de pointillés qui relient les 2 carrés à gauches et les 2 carrés en haut.

La lecture d'un QR Code s'effectue par bloc de 14 bits (2 fois 7 bits, codés avec le code de Hamming). Un bloc se lit en diagonale (de la droite vers la gauche). On commence la lecture en bas à droite du QR Code, puis on lit 2 blocs(de droite à gauche), on remonte, on lit 2 bloc(de gauche à droite) et ainsi de suite.
Chaque bloc contient 8 bits d'informations. Le pixel à la position (24, 8) code le type de données. S’il est à 0 il s’agit de données numériques : 8 bits codent deux symboles hexadécimaux. S’il est à 1, il s’agit de données brutes, 8 bits seront interprétés comme un code ASCII.


Les fonctions du programme :

La fonction charger permet d'accéder à des QR Code enregistrés dans notre ordinateur via l'interface Tkinter.

Les fonctions de vérification permettent de déterminer si le QR Code est dans le bon sens de lecture et dans le cas contraire lui faire faire des rotations de 90° vers la droite jusqu'à ce qu'il soit dans la bonne position, ainsi que de vérifier s'il y a bien les pointillés entre les carrés de gauche et les carrés du haut.

Les fonctions bits de correction et correction d'erreurs sont utiliées pour le code de Hamming. Elles vérifient qu'il n'y ait pas d'erreurs grâce aux bits de cotrôle (7 bits par bloc : 4 bits de message et 3 bits de parité). 

La fonction filtre lit les pixels en position (22,8) et (23,8) puis applique le filtre correspondant, c'est-à-dire :
- rien si les pixels sont 00
- un damier (avec une case noire en haut à gauche), si les pixels sont 01
- des lignes horizontales alternées noires et blanches, la plus haute étant noire, si les pixels sont 10
- des lignes verticales alternées noires et blanches, la plus à gauche étant noire, si les pixels sont 11

Nous avons donc créer une fonction pour chaque filtre afin de générer le filtre correspondant, à la lecture des pixels (22,8) et (23,8).

La fonction scanner permet la lecture du QR Code. En effet,  elle vérifie qu'un QR Code est chargé dans l'interface et qu'il est dans le bon sens, puis elle récupère les informations contenues dans les blocs et les affiche.
 
Interface graphique:

La fenêtre Tkinter est constituée des boutons charger (qui permet d'importer un QR Code dans l'interface), scanner (qui permet de lire le QR Code) et sauvegarder ( qui sauvegarde une image en noir et blanc).



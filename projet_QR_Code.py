######################################### 
# LDDBI
# LE CORRE Camille
# COUSTILLAS Laurédane
# LEFEVRE Laura
# https://github.com/uvsq22100620/Projet-QR-Code.git
##########################################


##########################################
##### Import des librairies
##########################################


import PIL as pil
from PIL import Image
from PIL import ImageTk 

import tkinter as tk


##########################################
##### Variables globales et constantes
##########################################


global mat_QRC

filename = "qr_code_ssfiltre_num.png"

TAILLE_CARRE = 8


##########################################
##### Fonctions
##########################################


def nbrCol(matrice):
    """ Fonction qui retourne le nombre de colonnes d'une matrice"""

    return len(matrice[0])



def nbrLig(matrice):
    """ Fonction qui retourne le nombre de lignes d'une matrice"""

    return len(matrice)



def saving(matPix, filename):#sauvegarde l'image contenue dans matpix dans le fichier filename
							 #utiliser une extension png pour que la fonction fonctionne sans perte d'information
    toSave=pil.Image.new(mode = "1", size = (nbrCol(matPix),nbrLig(matPix)))
    for i in range(nbrLig(matPix)):
        for j in range(nbrCol(matPix)):
            toSave.putpixel((j,i),matPix[i][j])
    toSave.save(filename)



def loading(filename):#charge le fichier image filename et renvoie une matrice de 0 et de 1 qui représente 
					  #l'image en noir et blanc
    toLoad=pil.Image.open(filename)
    mat=[[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            mat[i][j]= 0 if toLoad.getpixel((j,i)) == 0 else 1
    return mat



def sousListe(matrice, i1, j1, i2, j2):
    """ Créer une sous-liste correspondant à un endroit particulier de la matrice prise en 
    entrée (récupère les informations de cette matrice);
    (i1, j1) sont les coordonnées du coin supérieur gauche de la sous-matrice (coordonnées 
    du 1er élément) et (i2, j2) sont celles du coin inférieur droit (dernier élément)"""

    nbr_lignes = i2 - i1 + 1
    nbr_colonnes = j2 - j1 + 1

    ss_liste = [[0]* nbr_colonnes for b in range(nbr_lignes)]

    for x in range(nbr_lignes):
        for y in range(nbr_colonnes):
            ss_liste[x][y] = matrice[i1+x][j1+y]


    return ss_liste



def creationMotif(n):
    """ Créer le motif du carré présent en haut à gauche, en haut à droite et
    en bas à gauche du QR Code ; c'est un carré dont le côté est de taille n"""
    # il faut que n >= 4

    l0 = []
    for k in range(n):
        l0.append(0)

    l1 = [0]
    for k in range(n-1):
        l1.append(1)

    l2 = [0,1]
    for k in range(n-3):
        l2.append(0)
    l2.append(1)

    l3 = [0,1,0]
    for k in range(n-5):
        l3.append(1)
    l3.append(0)
    l3.append(1)


    mat = [l0]
    mat.append(l1)
    mat.append(l2)
    for k in range(n-5):
        mat.append(l3)
    mat.append(l2)
    mat.append(l1)

    return mat
    


def rotation(matrice):
    """ Tourne la matrice de 90° vers la droite """  # droite peu importe
    
    mat_res = [[0]*nbrLig(matrice) for i in range(nbrCol(matrice))]

    for i in range(nbrLig(matrice)):
        for j in range(nbrCol(matrice)):
            mat_res[i][j] = matrice[nbrLig(matrice)-1-j][i]

    return mat_res
       


def verifCarre(matrice, n):
    """ Vérifie si le QR Code est dans le bon sens. Si ce n'est pas le cas, on effectue une rotation,
    jusqu'à ce qu'il soit positionné dans le bon sens. Les symboles carrés sont de taille n"""

    sous_liste = sousListe(matrice, 17, 17, 24, 24)
    carre = creationMotif(n)

    while sous_liste == carre:
        rotation(matrice)
        sous_liste = sousListe(matrice, 17, 17, 24, 24)

    return matrice



def verifPointillesHaut(m):
    """ Vérifie s'il y a bien des pointillés entre les carrés en haut (sur la 7ème ligne)"""

    for j in range(8, 17):      
        if j % 2 == 0:                  # les pixels dans une colonne paire doivent être noirs
            if m[6, j] == 0:
                return False
        elif j % 2 == 1:
            if m[6,j] == 1:
                return False
    return True



def verifPointillesGauche(m):
    """ Vérifie s'il y a bien des pointillés entre les carrés à gauche (sur la 7ème colonne)"""

    for i in range(8, 17):
        if i % 2 == 0:              # les pixels dans une ligne paire doivent être noirs
            if m[i,6] == 0:
                return False
        elif i % 2 == 1:
            if m[i,6] == 1:
                return False
    return True



def bits_de_correction(liste):
    """ Fonction qui renvoie les 3 bits de contrôle d'une liste de 4 bits"""

    m1 = liste[0]
    m2 = liste[1]
    m3 = liste[2]
    m4 = liste[3]

    c1 = m1 ^ m2 ^ m4
    c2 = m1 ^ m3 ^ m4
    c3 = m2 ^ m3 ^ m4 

    return [m1, m2, m3, m4, c1, c2, c3]



def correction_erreurs(liste):
    """ Prend une liste de 7 bits et la corrige s'il y a une erreur"""

    m1 = liste[0]
    m2 = liste[1]
    m3 = liste[2]
    m4 = liste[3]

    c1 = liste[4]
    c2 = liste[5]
    c3 = liste[6]

    erreurs = [0, 0, 0]           # liste qui contient les erreurs des bits de contrôle (1 => erreur)

    controle = bits_de_correction([m1, m2, m3, m4])

    if controle[4] != c1:
        erreurs[0] = 1
    if controle[5] != c2:
        erreurs[1] = 1
    if controle[6] != c3:
        erreurs[2] = 1

    if (erreurs[0] == 1) and (erreurs[1] == 1) and (erreurs[2] == 1):
        if m4 == 0:
            m4 = 1
        else:
            m4 = 0
    elif (erreurs[0] == 1) and (erreurs[1] == 1):
        if m1 == 0:
            m1 = 1
        else:
            m1 = 0
    elif (erreurs[0] == 1) and (erreurs[2] == 1):
        if m2 == 0:
            m2 = 1
        else:
            m2 = 0
    elif (erreurs[1] == 1) and (erreurs[2] == 1):
        if m3 == 0:
            m3 = 1
        else:
            m3 = 0



def messageErreur():
    """ Affiche dans un label un message d'erreur lorsque le QR Code n'est pas conforme"""
    pass



def scanner(matrice):
    """Fonction qui permet la lecture du QR Code"""        # docstring à compléter
    pass                                                   # fonction utilisée par le bouton 'scanner'
    ## verifCarre(matrice)
    ## if (verifPointillesHaut(matrice) == True) and (verifPointillesGauche(matrice) == True):
    ##    utilisation des fonctions pour la lecture du QR Code
    ## else:
    ##    messageErreur()



##########################################
##### Boucle principale
##########################################


mat_QRC = loading(filename)

racine = tk.Tk()
racine.title("Lecture de QR Code")

racine.mainloop()
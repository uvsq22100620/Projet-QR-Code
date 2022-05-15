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
from tkinter import filedialog
from tkinter import simpledialog


##########################################
##### Variables globales et constantes
##########################################


type_donnees = 0


TAILLE_CARRE = 8

create = True
NomImgCourante=""
nomImgDebut=""

mat_QRC = []

##########################################
##### Fonctions
##########################################


def nbrCol(matrice):
    """ Fonction qui retourne le nombre de colonnes d'une matrice"""

    return len(matrice[0])


def nbrLig(matrice):
    """ Fonction qui retourne le nombre de lignes d'une matrice"""

    return len(matrice)


def saving(matPix, filename):
    '''Sauvegarde l'image contenue dans matpix dans le fichier filename utiliser une extension png pour que la fonction fonctionne sans perte d'information'''
    toSave=pil.Image.new(mode = "1", size = (nbrCol(matPix),nbrLig(matPix)))
    for i in range(nbrLig(matPix)):
        for j in range(nbrCol(matPix)):
            toSave.putpixel((j,i),matPix[i][j])
    toSave.save(filename)


def loading(filename):
    ''' Charge le fichier image filename et renvoie une matrice de 0 et de 1 qui représente l'image en noir et blanc'''
    toLoad=pil.Image.open(filename)
    mat=[[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            mat[i][j]= 0 if toLoad.getpixel((j,i)) == 0 else 1
    return mat


def charger(widget, filename):
    '''Fonction permettant de charger un QR Code et qui l'affiche'''

    global create, nomImgDebut, NomImgCourante, canvas, dessin, photo

    img = pil.Image.open(filename)
    NomImgCourante = filename.name
    nomImgDebut = filename.name
    photo = ImageTk.PhotoImage(img)
    if create:
        canvas = tk.Canvas(widget, width=img.size[0], height=img.size[1])
        dessin = canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.grid(row=0, column=2)
        create=False

    else:
        canvas.grid_forget()
        canvas=tk.Canvas(widget, width=img.size[0], height=img.size[1])
        dessin=canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.grid(row=0, column=2)


def init_matQRC():
    '''Fonction permettant d'initialiser la matrice du QR Code chargé'''
    global mat_QRC

    filename = filedialog.askopenfile(mode='rb', title='Choose a file')
    mat_QRC = loading(filename)
    charger(racine, filename)
    print(mat_QRC)


def fermer_fenetre():
    racine.destroy()


def creationMotif(n=8):
    '''Fonction permettant la création du motif avec pour modèle le carré en bas à droite'''
    
    #Creation de 4 listes différentes représentant les différentes lignes du motif
    l0 = [1]*n
    l1 = [1] + [0]*(n-1)
    l2 = [1,0] + [1]*(n-4) + [1,0]
    l3 = [1,0,1] + [0]*(n-5) + [1,0]

    #concatenation des listes pour representer le motif avec une liste imbriquee
    mat = [l0]+[l1]+[l2]+[l3]*(n-5)+[l2]+[l1]
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


def rotation(matrice):
    """ Tourne la matrice de 90° vers la droite """
    
    mat_res = [[0]*nbrLig(matrice) for i in range(nbrCol(matrice))]

    for i in range(nbrLig(matrice)):
        for j in range(nbrCol(matrice)):
            mat_res[i][j] = matrice[nbrLig(matrice)-1-j][i]

    return mat_res


def verifCarre(matrice, n):
    """ Vérifie si le QR Code est dans le bon sens. Si ce n'est pas le cas, on effectue une rotation,
    jusqu'à ce qu'il soit positionné dans le bon sens. Les symboles carrés sont de taille n"""

    c1 = len(matrice)-n
    c2 = len(matrice)-1
    
    sous_liste = sousListe(matrice, c1, c1, c2, c2)
    carre = creationMotif(n)

    while sous_liste == carre:
        matrice = rotation(matrice)
        sous_liste = sousListe(matrice, c1, c1, c2, c2)

    affichage_texte.config(text="Le QR Code a été tourné dans le bon sens")
    return matrice


def verifPointillesHaut(m):
    """ Vérifie s'il y a bien des pointillés entre les carrés en haut (sur la 8ème ligne)"""

    for j in range(8, 17):      
        if j % 2 == 0:                  # les pixels dans une colonne paire doivent être noirs
            if m[6][j] == 1:
                return False
        elif j % 2 == 1:
            if m[6][j] == 0:
                return False
    return True


def verifPointillesGauche(m):
    """ Vérifie s'il y a bien des pointillés entre les carrés à gauche (sur la 8ème colonne)"""

    for i in range(8, 17):
        if i % 2 == 0:              # les pixels dans une ligne paire doivent être noirs
            if m[i][6] == 1:
                return False
        elif i % 2 == 1:
            if m[i][6] == 0:
                return False
    return True


def divisionBlocs(matrice):
    """ Divise la partie du QR Code contenant les informations
    à récupérer en 16 blocs de 14 bits chacun"""

    nb_blocs = nombreBlocs(matrice)
    blocs = [0 for b in range(16)]

    ind_blocs_droite = [0,3,4,7,8,11,12,15]
    ind_blocs_gauche = [1,2,5,6,9,10,13,14]

    for k in range(8):      # pour les blocs de droite
        blocs[ind_blocs_droite[k]] = sousListe(matrice, (23-(k*2)), 18, (24-(k*2)), 24)

    for k in range(8):      # pour les blocs de gauche
        blocs[ind_blocs_gauche[k]] = sousListe(matrice, (23-(k*2)), 11, (24-(k*2)), 17)

    #for k in range(16-nb_blocs):
    #    del(blocs[-(k+1)])

    #affichage_blocs.config(text='Le QR_Code contient ' + str(nb_blocs) + ' bloc(s)')

    return blocs



def lectureBloc(liste_de_blocs):
    """ Transforme une matrice contenant les blocs du QR Code en des listes de 7 bits,
    les 4 premiers sont les bits de message et les 3 derniers sont les bits de correction"""


    res = []

    for b in liste_de_blocs:
        l1 = [b[1][6], b[0][6], b[1][5], b[0][5], b[1][4], b[0][4], b[1][3]]
        res.append(l1)
        l2 = [b[0][3], b[1][2], b[0][2], b[1][1], b[1][0], b[1][0], b[0][0]]
        res.append(l2)

    return res


def bits_de_correction(liste):
    """ Fonction qui renvoie les 3 bits de contrôle d'une liste de 4 bits"""

    m1 = liste[0]
    m2 = liste[1]
    m3 = liste[2]
    m4 = liste[3]

    c1 = m1 ^ m2 ^ m4
    c2 = m1 ^ m3 ^ m4
    c3 = m2 ^ m3 ^ m4 

    return [c1, c2, c3]


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

    if controle[0] != c1:
        erreurs[0] = 1
    if controle[1] != c2:
        erreurs[1] = 1
    if controle[2] != c3:
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

    return [m1, m2, m3, m4]


def messageErreur(txt:str):
    """ Affiche dans un label un message d'erreur lorsque le QR Code n'est pas conforme"""
    
    affichage_texte.config(text=txt)


def creationFiltre00(matrice):
    """ Génère le filtre 00 (entièrement noir)"""
    
    return [[0]*nbrCol(matrice) for b in range(nbrLig(matrice))]


def creationFiltre01(matrice):
    """ Génère le filtre 01 (damier avec la case en haut à gauche noire)"""
    
    f = [[0]*nbrCol(matrice) for b in range(nbrLig(matrice))]

    for i in range(nbrCol(f)):
        for j in range(nbrLig(f)):
            if (i+j) % 2 != 0:
                f[i][j] = 1

    return f


def creationFiltre10(matrice):
    """ Génère le filtre 10 (des lignes horizontales alternées noires et blanches, la plus haute étant noire)"""
    
    f = [[0]*nbrCol(matrice) for b in range(nbrLig(matrice))]

    for i in range(nbrCol(f)):
        for j in range(nbrLig(f)):
            if (i % 2) != 0:
                f[i][j] = 1

    return f


def creationFiltre11(matrice):
    """ Génère le filtre 11 (des lignes verticales alternées noires et blanches, la plus à gauche étant noire)"""
    
    f = [[0]*nbrCol(matrice) for b in range(nbrLig(matrice))]

    for i in range(nbrCol(f)):
        for j in range(nbrLig(f)):
            if (j % 2) != 0:
                f[i][j] = 1

    return f


def filtre(matrice):
    """ Lit les pixels en position (22,8) et (23,8) puis applique le filtre
    correspondant et renvoie la matrice correspondante"""
    
    filtre = []
    mat_res = [[0]*nbrCol(matrice) for b in range(nbrLig(matrice))]

    if (matrice[22][8] == 0) and (matrice[23][8] == 0):
        filtre = creationFiltre00(matrice)
        print('filtre 00')
    elif (matrice[22][8] == 0) and (matrice[23][8] == 1):
        filtre = creationFiltre01(matrice)
        print('filtre 01')
    elif (matrice[22][8] == 1) and (matrice[23][8] == 0):
        filtre = creationFiltre10(matrice)
        print('filtre 10')
    else:
        filtre = creationFiltre11(matrice)
        print('filtre 11')

    
    for i in range(nbrLig(matrice)):
        for j in range(nbrCol(matrice)):
            mat_res[i][j] == matrice[i][j] ^ filtre[i][j]

    return mat_res


def nombreBlocs(matrice):
    """ Récupère le nombre de blocs où est stocké le message"""

    nb_blocs = str(matrice[13][0]) + str(matrice[14][0]) + str(matrice[15][0]) + str(matrice[16][0]) + str(matrice[17][0])

    if nb_blocs == '11111' :
        return 0
    else :
        return int(nb_blocs, 2)


def scanner(matrice):
    """Fonction qui permet la lecture du QR Code"""

    if mat_QRC == [] :
        return messageErreur("Erreur : Aucun QR_Code n'a été chargé")
        
    matrice = verifCarre(matrice, TAILLE_CARRE)
    # le QR Code est positionné dans le bon sens
    if (verifPointillesHaut(matrice) == False) or (verifPointillesGauche(matrice) == False):
        #QR Code non conforme
        return messageErreur("Erreur : Le QR_Code n'est pas conforme")            
            
    #Le QR Code est chargé et conforme
    #On applique le filtre au QR Code
    m_filtre = filtre(matrice)

    # on récupère les informations dans des listes de 7 bits
    info7bits = lectureBloc(divisionBlocs(m_filtre))
    info4bits = []

    message = ''

    for k in range(len(info7bits)):
            # chaque liste de 7 bits est corrigée est devient une liste de 4 bits
        info4bits.append(correction_erreurs(info7bits[k]))

    if matrice[24][8] == 0:
        print('données numériques')
            # si ce sont des données numériques
        for m in info4bits:
            bin = ''
            for c in m:
                bin += str(c)
            message += str(hex(int(bin,2)))
    else:
        print('données brutes')
        for m in range(0, len(info4bits), 2):
            l = info4bits[m] + info4bits[m+1]
            bin = ''
            for c in l:
                bin += str(c)
            message += chr(int(str(bin),2))
    affichage_texte.config(text=message)

    

    



##########################################
##### Boucle principale
##########################################

racine = tk.Tk()
racine.title("Projet : Lecture de QR Code")

### Création des widgets

#bouton_charger = tk.Button(racine, text='charger', command=lambda:charger(racine))
bouton_charger = tk.Button(racine, text='charger', command=init_matQRC)
bouton_scanner = tk.Button(racine, text='scanner', command=lambda: scanner(mat_QRC))
bouton_sauvegarder = tk.Button(racine, text='sauvegarder')
bouton_quitter = tk.Button(racine, text='quitter', command=fermer_fenetre)

affichage_texte = tk.Label(racine, text='')
affichage_blocs = tk.Label(racine, text='')


### Positionnement des widgets

bouton_charger.grid(column=0, row=0)
bouton_scanner.grid(column=0, row=1)
bouton_sauvegarder.grid(column=0, row=2)
bouton_quitter.grid(column=0, row=3)

affichage_texte.grid(column=1, row=3)
affichage_blocs.grid(column=1, row=4)

racine.mainloop()

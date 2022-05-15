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


def divisebloc(matrice):

    nb_bloc = nombreBlocs(mat_QRC)

    affichage_texte.config(text = "Le nombre de bloc(s) a decoder est " + str(nb_bloc) + '.')

    qr_decode = []

    #Liste contenant les coordonnees des differents blocs pour permettre l'appel de la fonction sousListe en fonction du nombre de bloc a lire
    c_blocs = [(23, 18, 24, 24), (23, 11, 24, 17), (21, 11, 22, 17), (21, 18, 22, 24), (19, 18, 20, 24), (19, 11, 20, 17), (17, 11, 18, 17),
    (17, 18, 18, 24), (15, 18, 16, 24), (15, 11, 16, 17), (13, 11, 14, 17), (13, 18, 14, 24), (11, 18, 12, 24), (11, 11, 12, 17), (9, 11, 10, 17), (9, 18, 10, 24)]

    ind_gauche_droite = [2, 3, 6, 7, 10, 11, 14, 15]    #Numeros des blocs a lire de gauche a droite
    ind_droite_gauche = [0, 1, 4, 5, 8, 9, 12, 13]      #Numeros des blocs a lire de droite a gauche

    for num_bloc in range(nb_bloc):
        if num_bloc in ind_droite_gauche:
            qr_decode.append(lecture_droite_a_gauche(sousListe(matrice, c_blocs[num_bloc][0], c_blocs[num_bloc][1], c_blocs[num_bloc][2], c_blocs[num_bloc][3])))

        if num_bloc in ind_gauche_droite:
            qr_decode.append(lecture_gauche_a_droite(sousListe(matrice, c_blocs[num_bloc][0], c_blocs[num_bloc][1], c_blocs[num_bloc][2], c_blocs[num_bloc][3])))

    return qr_decode


def lecture_droite_a_gauche(matrice):
    '''Fonction permettant la lecture d'un bloc de droite a gauche'''

    li_bloc = []
    for i in range(-1, -8, -1):
        li_bloc.append(matrice[-1][i])
        li_bloc.append(matrice[0][i])

    return li_bloc


def lecture_gauche_a_droite(matrice):
    '''Fonction permettant la lecture d'un bloc de gauche a droite'''

    li_bloc = []
    for i in range(7):
        li_bloc.append(matrice[1][i])
        li_bloc.append(matrice[0][i])

    return li_bloc
    

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


def correction_erreurs(matrice):
    """ Prend une liste de 7 bits et la corrige s'il y a une erreur"""

    matrice_corrigee = []

    for liste in matrice:
        
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

        matrice_corrigee.append([m1, m2, m3, m4])

    return matrice_corrigee


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
        affichage_filtre.config(text='filtre : noir (00)')

    elif (matrice[22][8] == 0) and (matrice[23][8] == 1):
        filtre = creationFiltre01(matrice)
        affichage_filtre.config(text='filtre : damier (01)')

    elif (matrice[22][8] == 1) and (matrice[23][8] == 0):
        filtre = creationFiltre10(matrice)
        affichage_filtre.config(text='filtre : lignes horizontales (10)')

    else:
        filtre = creationFiltre11(matrice)
        affichage_filtre.config(text='filtre : lignes verticales (11)')

    
    for i in range(nbrLig(matrice)):
        for j in range(nbrCol(matrice)):
            mat_res[i][j] = matrice[i][j] ^ filtre[i][j]

    return mat_res


def nombreBlocs(matrice):
    """ Récupère le nombre de blocs où est stocké le message"""

    nb_blocs = str(matrice[13][0]) + str(matrice[14][0]) + str(matrice[15][0]) + str(matrice[16][0]) + str(matrice[17][0])

    if nb_blocs == '11111' :
        return 0
    else :
        return int(nb_blocs, 2)


def separe_listes_bloc(matrice):
    '''Fonction permettant de creer des listes de 7 bits a partir d'une liste de 14 bits'''

    res = []

    for elt in matrice:
        res.append(elt[0:7])
        res.append(elt[7:15])

    return res


def scanner(matrice):
    """Fonction qui permet la lecture du QR Code"""

    #On verifie qu'un QR_Code a ete charge, sinon on renvoie un message d'erreur
    if mat_QRC == [] :
        return messageErreur("Erreur : Aucun QR_Code n'a été chargé")
        
    #On verifie que le QR_Code est dans le bon sens, sinon il subit une orientation jusqu'à obtenir le bon sens
    matrice = verifCarre(matrice, TAILLE_CARRE)

    #On verifie que le QR_Code est conforme, sinon on renvoie un message d'erreur
    if (verifPointillesHaut(matrice) == False) or (verifPointillesGauche(matrice) == False):
        return messageErreur("Erreur : Le QR_Code n'est pas conforme")            
            
    #On applique le filtre au QR Code
    m_filtre = filtre(matrice)


    #On lit la nouvelle matrice dans le bon ordre et on obtient une matrice avec des listes de 14 bits. 
    #On separe les listes de 14 bits en deux pour appliquer la correction d'erreurs qui lit des listes de 7 bits
    #On corrige ensuite les erreurs
    matrice_corrigee = correction_erreurs(separe_listes_bloc(divisebloc(m_filtre)))
    message = ''

    if matrice[24][8] == 0: # si ce sont des données numériques
        affichage_donnees.config(text='données : numériques') 

        for m in matrice_corrigee:
            bin = ''
            for c in m:
                bin += str(c)
            message += str(hex(int(bin,2)))
    else:
        affichage_donnees.config(text='données : brutes')
        for m in range(0, len(matrice_corrigee), 2):
            l = matrice_corrigee[m] + matrice_corrigee[m+1]
            bin = ''
            for c in l:
                bin += str(c)
            message += chr(int(str(bin),2))

    affichage_message.config(text=message)




##########################################
##### Boucle principale
##########################################

racine = tk.Tk()
racine.title("Projet : Lecture de QR Code")

### Création des widgets

#bouton_charger = tk.Button(racine, text='charger', command=lambda:charger(racine))
bouton_charger = tk.Button(racine, text='charger', font = ("helvetica", "15"), command=init_matQRC)
bouton_scanner = tk.Button(racine, text='scanner', font = ("helvetica", "15"), command=lambda: scanner(mat_QRC))
bouton_quitter = tk.Button(racine, text='quitter', font = ("helvetica", "15"), command=fermer_fenetre)

affichage_texte = tk.Label(racine, text='', font = ("helvetica", "15"))
affichage_message = tk.Label(racine, text='', font = ("helvetica", "15"))
affichage_filtre = tk.Label(racine, text='', font = ("helvetica", "15"))
affichage_donnees = tk.Label(racine, text='', font = ("helvetica", "15"))
affichage_blocs = tk.Label(racine, text='', font = ("helvetica", "15"))


### Positionnement des widgets

bouton_charger.grid(column=0, row=0, pady=5)
bouton_scanner.grid(column=0, row=1, pady=5)
bouton_quitter.grid(column=0, row=3, pady=5)

affichage_texte.grid(column=0, row=4, columnspan=2)
affichage_filtre.grid(column=0, row=5, columnspan=2)
affichage_donnees.grid(column=0, row=6, columnspan=2)
affichage_blocs.grid(column=0, row=7, columnspan=2)
affichage_message.grid(column=0, row=8, columnspan=2)


#Appel principal
racine.mainloop()

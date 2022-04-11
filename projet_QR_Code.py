######################################### 
# LDDBI
# LE CORRE Camille
# COUSTILLAS Laurédane
# LEFEVRE Laura
# https://github.com/uvsq22100620/Projet-QR-Code.git
# #########################################


##### Fonctions


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



def verifCarres(m):
    """ Fonction qui renvoie True si les carrés du QR Code (en haut à droite, en haut à gauche et en bas à gauche) 
    sont bien placés, sinon, elle renvoie False"""

### Modèles des carrés

carre = [[1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 1], [1, 0, 1, 1, 1, 0, 1],[1, 0, 1, 1, 1, 0, 1], [1, 0, 1, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1]]

carre_haut_gauche = carre.copy()

for i in range(len(carre)):
    carre_haut_gauche[i].append(0)
carre_haut_gauche.append([0]*8)


carre_haut_droite = [[1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 1], [1, 0, 1, 1, 1, 0, 1],[1, 0, 1, 1, 1, 0, 1], [1, 0, 1, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1]]

for i in range(len(carre)):
    carre_haut_droite[i].insert(0, 0)
carre_haut_droite.append([0]*8)


carre_bas_gauche = [[1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 1], [1, 0, 1, 1, 1, 0, 1],[1, 0, 1, 1, 1, 0, 1], [1, 0, 1, 1, 1, 0, 1], [1, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1]]

for i in range(len(carre)):
    carre_bas_gauche[i].append(0)
carre_bas_gauche.insert(0, 0)
carre_bas_gauche[0] = [0]*8

# Il faut maintenant récupérer la zone du QR Code où doivent s'organiser les pixels pour former les carrés,
# et les mettre dans 3 sous-listes puis les comparer avec les modèles.
# Ensuite, si les sous-listes sont égales aux modèles, c'est que le QR Code est dans le bon sens.
# Sinon, on effectue une rotation du QR Code puis on revérifier que ça correspond aux modèles, etc...
# test
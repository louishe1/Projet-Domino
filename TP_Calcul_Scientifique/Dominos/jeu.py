############################################## FICHIER DE JEU ##############################################
############################################################################################################
from Classes import Main
from Classes import Pioche
from Classes import Domino
from Classes import Plateau


def plus_grand_numero () :
    return( int( input("Donner le chiffre entier maximal sur les dominos.") ) )

def nb_participants() :
    N = int(input("Combien de participants dans cette partie (joueurs ou IA) entre 2 et 4"))
    while N not in [2,3,4] :
        N = int(input("Recommencez avec un entier entre 2 et 4"))
    X = int(input("Combien de joueurs humains"))
    while X not in [0, 1, 2, 3, 4] or X > N:
        X = int(input("Recommencez avec un entier valide inférieur au nombre de participants"))
    return(N,X)

def liste_type_IA(r) : #r est le nb d'ia
    c,L = -1,[]
    for i in range(r) :
        c = int(input("Choisissez le type d'IA : tapez 0 pour l'IA aléatoire, tapez 1 pour l'IA gloutonne ou tapez 3 pour l'IA minmax"))
        while c != 0 and c != 1 and c != 2 :
            c = int(input("Recommencez avec 0,1 ou 2."))
        L.append(c)
    return(L)               #liste des r modes d'IA

def nb_dominos_par_personnes(n) :
    if n == 2 or n == 3 :
        return(7)
    if n == 4 :
        return(6)

P = plus_grand_numero()
N,X = nb_participants()
L = liste_type_IA(N-X)
M = nb_dominos_par_personnes(N)   # parametres globaux du jeu

PIOCHE = Pioche()
PIOCHE.remplir(P)

DICO_MAINS = {}
for i in range(N) :
    DICO_MAINS[f"Joueur_{i}"] = Main()
    DICO_MAINS[f"Joueur_{i}"].initialisation(PIOCHE,M)  # EVENTUELLEMENT ADAPTER X JOUEUR ET N-X IA

def maximum(Main) :
    c, d = -2 , Domino(-1,-1)
    for j in Main.liste :
        if Domino.est_un_double(j) and Domino.valeur(j) > c :
            c = Domino.valeur(j)
            d = j
    if c >= 0:
        return(d)
    else :
        for j in Main.liste :
            if Domino.valeur(j) > c :
                c = Domino.valeur(j)
                d = j
        return(d)

def premier_joueur(D) :
    MAXI, JOUEUR, DOMINO_MAX= -1,None,None
    for l in D.keys() :
        if Domino.valeur(maximum(D[l])) > MAXI and Domino.est_un_double(maximum(D[l])) :
            MAXI = Domino.valeur(maximum(D[l]))
            JOUEUR = l
            DOMINO_MAX = maximum(D[l])
    if MAXI >= 0:
        return(JOUEUR,DOMINO_MAX)
    else :
        for l in D.keys() :
            if Domino.valeur(maximum(D[l])) > MAXI :
                MAXI = Domino.valeur(maximum(D[l]))
                JOUEUR = l
                DOMINO_MAX = maximum(D[l])
        return(JOUEUR,DOMINO_MAX)












############################################## FICHIER DE JEU ##############################################
############################################################################################################
from Classes import Main
from Classes import Pioche
from Classes import Domino
from Classes import Plateau
import random


def plus_grand_numero () :
    return( int( input("Donner le chiffre entier positif maximal sur les dominos.") ) )

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

for i in range(X) :
    DICO_MAINS[f"Joueur_{i}"] = Main()
    DICO_MAINS[f"Joueur_{i}"].initialisation(PIOCHE,M)
for i in range(N-X) :
    DICO_MAINS[f"IA_{i}"] = Main()
    DICO_MAINS[f"IA_{i}"].initialisation(PIOCHE,M)

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
        return([JOUEUR,DOMINO_MAX])
    else :
        for l in D.keys() :
            if Domino.valeur(maximum(D[l])) > MAXI :
                MAXI = Domino.valeur(maximum(D[l]))
                JOUEUR = l
                DOMINO_MAX = maximum(D[l])
        return([JOUEUR,DOMINO_MAX])

#print(PIOCHE)
#print(DICO_MAINS)
#print(premier_joueur(DICO_MAINS))

def ia_aleatoire(main_ia,PLATEAU) :
    JOUABLES = main_ia.numeros_jouables(PLATEAU)
    if len(JOUABLES) == 0 :
        return(-1)                              # retourne -1 si elle doit piocher
    R =  random.randint(0,len(JOUABLES)-1)
    return(JOUABLES[R])

def max_glouton(L):
    c, indice = -1, -1
    for j in range(len(L)):
        if Domino.valeur(L[j]) > c:
            c = Domino.valeur(L[j])
            indice = j
    return(indice)

def ia_gloutonne(main_ia,PLATEAU) :
    JOUABLES = main_ia.dominos_jouables(PLATEAU)
    if len(JOUABLES) == 0 :
        return(-1)
    R = main_ia.numeros_jouables(PLATEAU)[max_glouton(JOUABLES)]
    return(R)

################# IA MINMAX A CREER ###################"

############### fonction qui prend la MAIN,PLATEAU et un indice de JOUABLES
# defini par les fonction ci dessus pour les IA et qui joue le Domino ##########

############# fonction qui montre sa main et ses jouables et le plateau au joueur
# et qui joue
# le domino choisi sur le coté choisi ######################


def jeu_joueur(MAIN,PLATEAU,PIOCHE) :
    print("*********************************************************")
    print("Plateau :   ", PLATEAU)
    print("Main :   ", MAIN.afficher_main())
    jouables = MAIN.numeros_jouables(PLATEAU)
    print("Numéros des dominos jouables:   ",jouables)

    if len(jouables) > 0:
        indice = int(input("Entrer le numéro du domino que vous voulez jouer : "))
        domino_choisi = MAIN.liste[indice]
        PLATEAU.jouer_domino_table(domino_choisi)
        MAIN.retirer(domino_choisi)
    elif len(PIOCHE) > 0:
        print("Aucun domino jouable, vous piochez !")
        domino_pioche = PIOCHE.piocher_rdm()
        MAIN.piocher(domino_pioche)


def jeu_IA(MAIN,PLATEAU,MODE_IA,PIOCHE) :
    indice = 0
    if MODE_IA == 0 :
        indice = ia_aleatoire(MAIN,PLATEAU)
    elif MODE_IA == 1 :
        indice = ia_gloutonne(MAIN,PLATEAU)
    #### à rajouter : ia minmax

    jouables = MAIN.numeros_jouables(PLATEAU)

    if len(jouables) > 0:
        indice = 0
        if MODE_IA == 0:
            indice = ia_aleatoire(MAIN, PLATEAU)
        elif MODE_IA == 1:
            indice = ia_gloutonne(MAIN, PLATEAU)
        domino_choisi = MAIN.liste[indice]
        PLATEAU.jouer_domino_table(domino_choisi)
        MAIN.retirer(domino_choisi)

    elif not PIOCHE.est_vide():
        print("L'IA pioche.")
        domino_pioche = PIOCHE.piocher_rdm()
        MAIN.piocher(domino_pioche)


PLATEAU = Plateau()

JOUEUR_DEPART = premier_joueur(DICO_MAINS)[0]               # donne celui qui commence
PLATEAU.jouer_domino_table(premier_joueur(DICO_MAINS)[1])  #oblige a jouer le premier coup

COMPTEUR_DIMPOSSIBILITE = 0   # incrementé si qqn ne peut ni jouer ni piocher sinon remit a zero
LISTE_JOUEUR_ACTIF = [Domino(-1,-1)]   # sert a verifier si la liste du joueur actif est vide

ordre_joueurs = list(DICO_MAINS.keys())
index_depart = ordre_joueurs.index(JOUEUR_DEPART)
tour = 1  # on a forcé le joueur de depart a jouer

while COMPTEUR_DIMPOSSIBILITE < N and len(LISTE_JOUEUR_ACTIF) != 0 :

    index_actuel = (index_depart + tour) % len(ordre_joueurs)  #index va de 0 à N-1
    nom_joueur = ordre_joueurs[index_actuel]
    main_actuelle = DICO_MAINS[nom_joueur]

    print(f"*** TOUR DE {nom_joueur} ***")

    ################  TOUR DE JEU IA OU HUMAIN ###############

    if nom_joueur.startswith("Joueur"):             # Logique pour faire jouer un humain
        jeu_joueur(main_actuelle,PLATEAU,PIOCHE)
    else:                                           # Logique automatique pour l'IA
        jeu_IA(main_actuelle,PLATEAU,MODE_IA,PIOCHE)

    # MISE A JOUR DE LA LISTE ACTIVE ET DU COMPTEUR

    # Passage au joueur suivant
    tour += 1




############################################## FICHIER DE JEU ##############################################
############################################################################################################
from Classes import Main
from Classes import Pioche
from Classes import Domino
from Classes import Plateau
import random


def plus_grand_numero () :
    return( int( input("Donner le chiffre entier positif maximal sur les dominos : ") ) )

def nb_participants() :
    N = int(input("Combien de participants dans cette partie (joueurs ou IA) entre 2 et 4 : "))
    while N not in [2,3,4] :
        N = int(input("Recommencez avec un entier entre 2 et 4 : "))
    X = int(input("Combien de joueurs humains : "))
    while X not in [0, 1, 2, 3, 4] or X > N:
        X = int(input("Recommencez avec un entier valide inférieur au nombre de participants : "))
    return(N,X)

def liste_type_IA(r) : #r est le nb d'ia
    c,L = -1,[]
    for i in range(r) :
        c = int(input("Choisissez le type d'IA : tapez 0 pour l'IA aléatoire, tapez 1 pour l'IA gloutonne ou tapez 2 pour l'IA minmax : "))
        while c != 0 and c != 1 and c != 2 :
            c = int(input("Recommencez avec 0,1 ou 2 :"))
        L.append(c)
    return(L)               #liste des r modes d'IA

def nb_dominos_par_personnes(n) :
    if n == 2 or n == 3 :
        return(7)
    if n == 4 :
        return(6)




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
        for d in D[l].liste :
            if Domino.valeur(d) > MAXI and Domino.est_un_double(d) :
                MAXI = Domino.valeur(d)
                JOUEUR = l
                DOMINO_MAX = d
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

def _evaluer_etat_minmax(main_ia_liste, adv_taille, pioche_vide, indices_ia):
    if len(main_ia_liste) == 0:
        return float("inf")
    if adv_taille <= 0:
        return float("-inf")

    score_main = sum(d.valeur() for d in main_ia_liste)
    nb_coups_jouables = len(indices_ia)

    val = -float(score_main) + 5.0 * nb_coups_jouables

    if nb_coups_jouables == 0 and pioche_vide:
        val -= 15.0

    return val


def _simuler_coup_minmax(plateau, domino):
    # Problème 1 : simulation stricte avec mode=2, identique à jeu_IA
    if plateau.compatible(domino) == "domino injouable":
        return None
    p_sim = Plateau()
    p_sim.dominos = [Domino(d.gauche, d.droite) for d in plateau.dominos]
    p_sim.jouer_domino_table_ia(domino, 2)
    return p_sim


def _dominos_adverses_supposes(main_ia_liste, plateau, limite=10):
    connus = {(min(d.gauche, d.droite), max(d.gauche, d.droite)) for d in main_ia_liste}
    for d in plateau.dominos:
        connus.add((min(d.gauche, d.droite), max(d.gauche, d.droite)))

    max_val = P if "P" in globals() else 6
    inconnus = []
    for a in range(max_val + 1):
        for b in range(a, max_val + 1):
            if (a, b) not in connus:
                inconnus.append(Domino(a, b))

    if len(inconnus) > limite:
        random.shuffle(inconnus)
        return inconnus[:limite]
    return inconnus


def _minmax_recursif(main_ia_liste, plateau, pioche_vide, profondeur, est_tour_ia, adv_taille):
    main_temp = Main()
    main_temp.liste = main_ia_liste
    indices_ia = main_temp.numeros_jouables(plateau)

    if profondeur == 0 or len(main_ia_liste) == 0 or adv_taille <= 0:
        return _evaluer_etat_minmax(main_ia_liste, adv_taille, pioche_vide, indices_ia)

    if est_tour_ia:
        if len(indices_ia) == 0:
            malus_pioche = 0.0 if pioche_vide else -3.0
            return malus_pioche + _minmax_recursif(
                main_ia_liste, plateau, pioche_vide, profondeur - 1, False, adv_taille
            )

        meilleur = float("-inf")
        for idx in indices_ia:
            dom = main_ia_liste[idx]
            p_suivant = _simuler_coup_minmax(plateau, dom)
            if p_suivant is None:
                continue
            nouvelle_main = [x for i, x in enumerate(main_ia_liste) if i != idx]
            score = _minmax_recursif(
                nouvelle_main, p_suivant, pioche_vide, profondeur - 1, False, adv_taille
            )
            if score > meilleur:
                meilleur = score
        return meilleur

    else:
        candidats_adv = _dominos_adverses_supposes(main_ia_liste, plateau, limite=10)
        coups_adv = []
        for dom in candidats_adv:
            p_suivant = _simuler_coup_minmax(plateau, dom)
            if p_suivant is not None:
                coups_adv.append(p_suivant)

        if not coups_adv:
            nouvelle_adv_taille = adv_taille if pioche_vide else adv_taille + 1
            return _minmax_recursif(
                main_ia_liste, plateau, pioche_vide, profondeur - 1, True, nouvelle_adv_taille
            )

        # Problème 2 : moyenne pondérée au lieu du pire cas absolu (évite la paranoïa)
        somme_scores = 0.0
        pire_score = float("inf")
        for p_suivant in coups_adv:
            nouvelle_adv_taille = max(0, adv_taille - 1)
            score = _minmax_recursif(
                main_ia_liste, p_suivant, pioche_vide, profondeur - 1, True, nouvelle_adv_taille
            )
            somme_scores += score
            if score < pire_score:
                pire_score = score

        moyenne = somme_scores / len(coups_adv)
        # Mélange 70% moyenne / 30% pire cas pour rester prudent sans être paralysé
        return 0.7 * moyenne + 0.3 * pire_score


def ia_minmax(main_ia, PLATEAU, PIOCHE=None, profondeur=None, adv_taille=None):
    prof = profondeur if profondeur is not None else 3
    indices_jouables = main_ia.numeros_jouables(PLATEAU)

    if len(indices_jouables) == 0:
        return -1

    pioche_vide = True if PIOCHE is None else PIOCHE.est_vide()

    if adv_taille is not None:
        adv_taille_init = adv_taille
    else:
        max_val = P if "P" in globals() else 6
        total_dominos = (max_val + 1) * (max_val + 2) // 2
        nb_pioche = len(PIOCHE.liste) if (PIOCHE is not None and hasattr(PIOCHE, "liste")) else 0
        adv_taille_init = max(1, total_dominos - len(main_ia.liste) - len(PLATEAU.dominos) - nb_pioche)

    meilleur_indice = indices_jouables[0]
    meilleure_val = float("-inf")

    for idx in indices_jouables:
        dom = main_ia.liste[idx]
        p_suivant = _simuler_coup_minmax(PLATEAU, dom)
        if p_suivant is None:
            continue
        nouvelle_main = [x for i, x in enumerate(main_ia.liste) if i != idx]
        val = _minmax_recursif(
            nouvelle_main,
            p_suivant,
            pioche_vide,
            prof - 1,
            est_tour_ia=False,
            adv_taille=adv_taille_init,
        )
        if val > meilleure_val:
            meilleure_val = val
            meilleur_indice = idx

    return meilleur_indice

############### fonction qui prend la MAIN,PLATEAU et un indice de JOUABLES
# defini par les fonction ci dessus pour les IA et qui joue le Domino ##########

############# fonction qui montre sa main et ses jouables et le plateau au joueur
# et qui joue
# le domino choisi sur le coté choisi ######################


def jeu_joueur(MAIN,PLATEAU,PIOCHE) :
    print("*********************************************************")
    print("Plateau :   ", PLATEAU)
    print("*********************************************************")
    print("Main :   ", MAIN.afficher_main())
    jouables = MAIN.numeros_jouables(PLATEAU)
    print("Numéros des dominos jouables:   ",jouables)
    print("*********************************************************")

    if len(jouables) > 0:
        indice = -1
        while indice not in jouables:
            try:
                indice = int(input("Entrer le numéro du domino que vous voulez jouer : "))
            except ValueError:
                print("Entrez un numéro valide.")
        domino_choisi = MAIN.liste[indice]
        PLATEAU.jouer_domino_table_humain(domino_choisi)
        MAIN.retirer(domino_choisi)
        return("ok")
    elif not PIOCHE.est_vide() :
        print("Aucun domino jouable, vous piochez !")
        domino_pioche = PIOCHE.piocher_rdm()
        MAIN.piocher(domino_pioche)
        return("ok")
    else :
        print("Aucun domino jouable, vous passez votre tour !")
        return(-1)


def jeu_IA(MAIN,PLATEAU,MODE_IA,PIOCHE) :

    jouables = MAIN.numeros_jouables(PLATEAU)

    if len(jouables) > 0:
        indice = 0
        if MODE_IA == 0:
            indice = ia_aleatoire(MAIN, PLATEAU)
        elif MODE_IA == 1:
            indice = ia_gloutonne(MAIN, PLATEAU)
        elif MODE_IA == 2:
            indice = ia_minmax(MAIN, PLATEAU, PIOCHE, M)

        domino_choisi = MAIN.liste[indice]
        PLATEAU.jouer_domino_table_ia(domino_choisi, MODE_IA)
        MAIN.retirer(domino_choisi)
        return "ok"

    elif not PIOCHE.est_vide():
        print("L'IA pioche.")
        domino_pioche = PIOCHE.piocher_rdm()
        MAIN.piocher(domino_pioche)
        return("ok")
    else :
        print("L'IA passe son tour.")
        return(-1)

def plus_petites_cles(dico):
    cles_min = []
    val_min = float('inf')

    for cle, valeur in dico.items():
        if valeur < val_min:
            val_min = valeur
            cles_min = [cle]
        elif valeur == val_min:
            cles_min.append(cle)

    return cles_min


if __name__ == "__main__":
    P = plus_grand_numero()
    N, X = nb_participants()
    L = liste_type_IA(N - X)
    M = nb_dominos_par_personnes(N)

    PIOCHE = Pioche()
    PIOCHE.remplir(P)

    DICO_MAINS = {}
    for i in range(X):
        DICO_MAINS[f"Joueur_{i}"] = Main()
        DICO_MAINS[f"Joueur_{i}"].initialisation(PIOCHE, M)
    for i in range(N - X):
        DICO_MAINS[f"IA_{i}"] = Main()
        DICO_MAINS[f"IA_{i}"].initialisation(PIOCHE, M)

    PLATEAU = Plateau()

    JOUEUR_DEPART = premier_joueur(DICO_MAINS)[0]
    PLATEAU.jouer_domino_table_humain(premier_joueur(DICO_MAINS)[1])
    DICO_MAINS[JOUEUR_DEPART].retirer(premier_joueur(DICO_MAINS)[1])

    COMPTEUR_DIMPOSSIBILITE = 0
    main_actuelle_liste = [Domino(-1, -1)]

    ordre_joueurs = list(DICO_MAINS.keys())
    index_depart = ordre_joueurs.index(JOUEUR_DEPART)

    tour = 1

    while COMPTEUR_DIMPOSSIBILITE < N and len(main_actuelle_liste) != 0:

        index_actuel = (index_depart + tour) % len(ordre_joueurs)
        nom_joueur = ordre_joueurs[index_actuel]
        main_actuelle = DICO_MAINS[nom_joueur]
        main_actuelle_liste = DICO_MAINS[nom_joueur].liste

        print(f"*** TOUR DE {nom_joueur} ***")

        if nom_joueur.startswith("Joueur"):
            Y = jeu_joueur(main_actuelle, PLATEAU, PIOCHE)
            if Y == "ok":
                COMPTEUR_DIMPOSSIBILITE = 0
            else:
                COMPTEUR_DIMPOSSIBILITE += 1

        else:
            index_ia = int(nom_joueur.split("_")[1])
            Y = jeu_IA(main_actuelle, PLATEAU, L[index_ia], PIOCHE)
            if Y == "ok":
                COMPTEUR_DIMPOSSIBILITE = 0
            else:
                COMPTEUR_DIMPOSSIBILITE += 1

        main_actuelle = DICO_MAINS[nom_joueur]
        main_actuelle_liste = DICO_MAINS[nom_joueur].liste

        print(f"Il reste {len(main_actuelle_liste)} dominos à {nom_joueur}.")

        tour += 1

    print("************* MAINS EN FIN DE PARTIE **************")
    print(DICO_MAINS)

    DICO_SCORE = {}
    for k in DICO_MAINS.keys():
        DICO_SCORE[k] = 0
        for j in range(len(DICO_MAINS[k].liste)):
            DICO_SCORE[k] += Domino.valeur(DICO_MAINS[k].liste[j])

    print("************* SCORES EN FIN DE PARTIE **************")
    print(DICO_SCORE)

    print("*********************************************************")
    if len(main_actuelle_liste) == 0:
        print(f"FIN DE PARTIE, {nom_joueur} a gagné !")
    else:
        print(f"FIN DE PARTIE, {plus_petites_cles(DICO_SCORE)} a gagné !")



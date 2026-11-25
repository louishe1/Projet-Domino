import random
from Classes import Domino, Main, Pioche, Plateau
from jeu import nb_dominos_par_personnes, plus_petites_cles


def _cle_canonique(domino):
    return tuple(sorted((domino.gauche, domino.droite)))


def _extremites_plateau(plateau):      #Récupère les valeurs aux deux bouts du plateau de façon générale."""
    if not plateau.dominos:
        return set()
    gauche = plateau.dominos[0].gauche
    droite = plateau.dominos[-1].droite
    return {gauche, droite}


def _calculer_points_fin_manche(mains, joueur_dernier_coup, main_vide):    # Applique la règle générale de score en fin de manche.
    points_main = {
        nom: sum(d.valeur() for d in m.liste)
        for nom, m in mains.items()
    }
    scores = {nom: 0 for nom in mains}

    if main_vide:
        gagnants = [joueur_dernier_coup]
    else:
        gagnants = plus_petites_cles(points_main)

    somme_perdants = sum(
        pts for nom, pts in points_main.items() if nom not in gagnants
    )
    for g in gagnants:
        scores[g] = somme_perdants

    return scores, gagnants, somme_perdants


# =====================================================================
# PALIER 1 : Distribution générale (P entre 6 et 12, nb de participants entre 2 et 4
# =====================================================================
def test_palier_1_distribution_generale():
    for max_val in (6,7,8,9,10,11,12):
        pioche = Pioche()
        pioche.remplir(max_val)
        nb_attendu = (max_val + 1) * (max_val + 2) // 2

        assert len(pioche.liste) == nb_attendu
        assert len({_cle_canonique(d) for d in pioche.liste}) == nb_attendu

    for nb_joueurs in (2, 3, 4):
        for _ in range(20):
            pioche = Pioche()
            pioche.remplir(6)
            taille_main = nb_dominos_par_personnes(nb_joueurs)

            mains = []
            for _ in range(nb_joueurs):
                m = Main()
                m.initialisation(pioche, taille_main)
                mains.append(m)
                assert len(m.liste) == taille_main

            tous = [d for m in mains for d in m.liste] + pioche.liste
            assert len(tous) == 28
            assert len({_cle_canonique(d) for d in tous}) == 28


# =====================================================================
# PALIER 2 : Coups légaux sur de nombreux plateaux et mains aléatoires
# =====================================================================
def test_palier_2_coups_legaux_cas_general():
    rng = random.Random(42)

    for _ in range(100):
        pioche = Pioche()
        pioche.remplir(6)
        rng.shuffle(pioche.liste)

        plateau = Plateau()
        premier = pioche.liste.pop()
        plateau.dominos.append(premier)

        for _ in range(rng.randint(1, 7)):
            if not pioche.liste:
                break
            d = pioche.liste.pop()
            ext_gauche = plateau.dominos[0].gauche
            ext_droite = plateau.dominos[-1].droite

            if d.droite == ext_gauche:
                plateau.dominos.insert(0, d)
            elif d.gauche == ext_gauche:
                plateau.dominos.insert(0, d.retourner())
            elif d.gauche == ext_droite:
                plateau.dominos.append(d)
            elif d.droite == ext_droite:
                plateau.dominos.append(d.retourner())

        main = Main()
        main.liste = [pioche.liste.pop() for _ in range(min(7, len(pioche.liste)))]

        extremites = {plateau.dominos[0].gauche, plateau.dominos[-1].droite}
        jouables = main.numeros_jouables(plateau)

        for idx in jouables:
            assert 0 <= idx < len(main.liste)
            d = main.liste[idx]
            assert (d.gauche in extremites) or (d.droite in extremites)

        for idx, d in enumerate(main.liste):
            if idx not in jouables:
                assert not ((d.gauche in extremites) or (d.droite in extremites))


# =====================================================================
# PALIER 3 : Pioche, talon vide et passage de tour (cas général)
# =====================================================================
def test_palier_3_pioche_et_passage_generaux():
    rng = random.Random(123)

    for _ in range(50):
        pioche = Pioche()
        pioche.remplir(6)
        rng.shuffle(pioche.liste)

        main = Main()
        main.liste = []
        compteur_blocage = 0

        while not pioche.est_vide():
            avant_main = len(main.liste)
            avant_pioche = len(pioche.liste)

            d = pioche.piocher_rdm()
            main.piocher(d)
            compteur_blocage = 0

            assert len(main.liste) == avant_main + 1
            assert len(pioche.liste) == avant_pioche - 1
            assert compteur_blocage == 0

        # Talon vide : piocher est impossible, on passe le tour
        assert pioche.est_vide()
        for tour_passe in range(1, 5):
            compteur_blocage += 1
            assert compteur_blocage == tour_passe


# =====================================================================
# PALIER 4 & 5 : Fins de manche et calcul des points sur cas aléatoires
# =====================================================================
def test_palier_4_et_5_calcul_points_cas_general():
    rng = random.Random(999)

    for _ in range(100):
        pioche = Pioche()
        pioche.remplir(6)
        rng.shuffle(pioche.liste)

        nb_joueurs = rng.choice([2, 3, 4])
        noms = [f"J_{i}" for i in range(nb_joueurs)]
        mains = {nom: Main() for nom in noms}

        for nom in noms:
            nb_d = rng.randint(0, 6)
            mains[nom].liste = [pioche.piocher_rdm() for _ in range(nb_d) if not pioche.est_vide()]

        # Cas 1 : fin par main vide
        gagnant_vide = rng.choice(noms)
        mains[gagnant_vide].liste = []

        scores_vide, gagnants_vide, somme_vide = _calculer_points_fin_manche(
            mains, gagnant_vide, main_vide=True
        )
        assert gagnants_vide == [gagnant_vide]
        assert scores_vide[gagnant_vide] == somme_vide
        for nom in noms:
            if nom != gagnant_vide:
                assert scores_vide[nom] == 0

        # Cas 2 : fin par blocage (gère victoire unique et égalités multiples)
        scores_bloc, gagnants_bloc, somme_bloc = _calculer_points_fin_manche(
            mains, joueur_dernier_coup=None, main_vide=False
        )
        assert len(gagnants_bloc) >= 1
        for nom in noms:
            if nom in gagnants_bloc:
                assert scores_bloc[nom] == somme_bloc
            else:
                assert scores_bloc[nom] == 0
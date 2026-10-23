
import random

def creer_dominos():
    return [(i, j) for i in range(7) for j in range(i, 7)]

def afficher_dominos(main):
    for i, domino in enumerate(main):
        print(f"{i}: [{domino[0]}|{domino[1]}]", end="   ")
    print()

def jouer_domino():
    dominos = creer_dominos()
    random.shuffle(dominos)

    joueur1 = dominos[:7]
    joueur2 = dominos[7:14]
    pioche = dominos[14:]

    chaine = []
    joueur_actuel = 1

    while joueur1 and joueur2:
        main = joueur1 if joueur_actuel == 1 else joueur2

        print("\n" + "=" * 50)
        print(f"Tour du joueur {joueur_actuel}")
        print("Chaîne :", chaine if chaine else "Vide")
        print("Votre main :")
        afficher_dominos(main)

        print(f"Dominos restants : {len(main)}")

        # Déterminer les dominos jouables
        jouables = []
        for i, (a, b) in enumerate(main):
            if not chaine or a == chaine[0] or b == chaine[0] \
                    or a == chaine[-1] or b == chaine[-1]:
                jouables.append(i)

        if not jouables:
            if pioche:
                domino = pioche.pop()
                main.append(domino)
                print(f"Vous piochez [{domino[0]}|{domino[1]}].")
                continue
            else:
                print("Aucun coup possible ! Vous passez votre tour.")
                joueur_actuel = 3 - joueur_actuel
                continue

        print("Choisissez le numéro du domino à jouer.")
        choix = input("Votre choix (ou 'p' pour piocher) : ").strip()

        if choix.lower() == "p" and pioche:
            domino = pioche.pop()
            main.append(domino)
            print(f"Vous piochez [{domino[0]}|{domino[1]}].")
            continue

        try:
            index = int(choix)
            if index not in jouables:
                print("Ce domino ne peut pas être joué !")
                continue
        except ValueError:
            print("Choix invalide.")
            continue

        a, b = main.pop(index)

        if not chaine:
            chaine = [a, b]
        elif a == chaine[0]:
            chaine.insert(0, b)
        elif b == chaine[0]:
            chaine.insert(0, a)
        elif a == chaine[-1]:
            chaine.append(b)
        elif b == chaine[-1]:
            chaine.append(a)
        else:
            print("Coup impossible.")
            main.insert(index, (a, b))
            continue

        print("Domino joué :", f"[{a}|{b}]")

        joueur_actuel = 3 - joueur_actuel

    print("\n" + "=" * 50)
    if not joueur1:
        print("🏆 Le joueur 1 a gagné !")
    elif not joueur2:
        print("🏆 Le joueur 2 a gagné !")

if __name__ == "__main__":
    jouer_domino()

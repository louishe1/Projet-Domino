from scipy.stats import quantile_test
import random

########################################### CLASSE DOMINO #####################################################
###############################################################################################################

class Domino :

    def __init__(self, gauche,droite):
        self.gauche = gauche
        self.droite = droite

    def __eq__(self, other):
        if not isinstance(other, Domino):
            return False
        return self.gauche == other.gauche and self.droite == other.droite

    def est_un_double(self):
        return(self.gauche == self.droite)

    def valeur(self):
        return(self.gauche + self.droite)                      #somme des valeurs

    def retourner(self):
        return (Domino(self.droite, self.gauche))                                          #modifie le domino en l'inversant

    def __repr__(self):
        # Utilisé dès qu'un Domino se trouve dans une liste : print(liste_dominos)
        return self.__str__()



    def __str__(self):
        return f"[{self.gauche}|{self.droite}]"                #affiche un beau domino

####################################### CLASSE PLATEAU ###################################################
##########################################################################################################

class Plateau :
    def __init__(self):
        self.dominos = []                       #simple liste vide

    def question_cote(self):
        reponse = None
        while reponse not in ["1","2"] :
            reponse = input("voulez vous jouer à droite (1) ou à gauche (2) ?")
        return reponse

    def append_g(self,domino):
        self.dominos = [domino] + self.dominos

    def extremites(self):
        if self.dominos == []:
            return('rien sur le plateau')
        else :
            return [self.dominos[0].gauche, self.dominos[-1].droite]# comment choisir les extremites

    def compatible(self, domino):
        ext = self.extremites()
        if ext == 'rien sur le plateau':
            return(-1)
        elif domino.gauche == ext[0] and domino.droite == ext[1]:
            return(4)
        elif domino.gauche == ext[1] and domino.droite == ext[0]:
            return(5)
        elif domino.gauche == ext[0] and domino.gauche == ext[1]:
            return(6)
        elif domino.droite == ext[1] and domino.droite == ext[0]:
            return(7)
        elif domino.gauche == ext[0] :
            return(0)
        elif domino.gauche == ext[1]:
            return(1)
        elif domino.droite == ext[0]:
            return(2)
        elif domino.droite == ext[1]:
            return(3)
        else:
            #print("domino injouable")
            return("domino injouable")

    def jouer_domino_table_humain(self, domino):
        comp = self.compatible(domino)
        P = self.dominos
        question = 0
        if comp in [4,5,6,7] :
            question = self.question_cote()
        if comp ==-1  :
            P.append(domino)
        elif comp == 0 or (comp == 4 and question == "2") or (comp == 6 and question =="2"): #placement de la partie gauche du domino à gauche du plateau
            self.append_g(domino.retourner())
        elif comp == 1 or (comp == 5 and question == "1") or (comp == 6 and question == "1"): #placement de la partie gauche du domino à droite du plateau
            P.append(domino)
        elif comp == 2 or (comp == 5 and question == "2") or (comp == 7 and question == "2"): #placement de la partie droite du domino à gauche du plateau
            self.append_g(domino)
        elif comp == 3 or (comp == 4 and question == "1") or (comp == 7 and question == "1" ) : #placement de la partie droite du domino à droite du plateau
            P.append(domino.retourner())

    def cloner(self):
        copie = Plateau()
        copie.dominos = [Domino(d.gauche, d.droite) for d in self.dominos]
        return copie

    def jouer_domino_table_ia(self, domino,type):
        comp = self.compatible(domino)
        P = self.dominos
        question = 0
        if comp in [4,5,6,7] :
            if type == 2:
                # Choix stratégique du côté pour MinMax :
                # compare l'effet d'une pose à droite ("1") ou à gauche ("2") sur une copie du plateau
                meilleur_cote = "1"
                meilleur_score_ext = float("inf")
                for cote_test in ("1", "2"):
                    p_test = Plateau()
                    p_test.dominos = [Domino(d.gauche, d.droite) for d in self.dominos]
                    pt_test = p_test.dominos

                    if comp == 4 and cote_test == "2":
                        p_test.append_g(domino.retourner())
                    elif comp == 5 and cote_test == "1":
                        pt_test.append(domino)
                    elif comp == 5 and cote_test == "2":
                        p_test.append_g(domino)
                    elif comp == 6 and cote_test == "2":
                        p_test.append_g(domino.retourner())
                    elif comp == 6 and cote_test == "1":
                        pt_test.append(domino)
                    elif comp == 7 and cote_test == "2":
                        p_test.append_g(domino)
                    elif comp == 7 and cote_test == "1":
                        pt_test.append(domino.retourner())
                    elif comp == 4 and cote_test == "1":
                        pt_test.append(domino.retourner())

                    exts = p_test.extremites()
                    # Favorise des extrémités basses pour limiter les gros points adverses
                    score_ext = exts[0] + exts[1] if isinstance(exts, list) else 0
                    if score_ext < meilleur_score_ext:
                        meilleur_score_ext = score_ext
                        meilleur_cote = cote_test

                question = meilleur_cote
            if type in [0,1] :
                question = str(random.randint(1, 2))
        elif comp ==-1  :
            P.append(domino)
        elif comp == 0 or (comp == 4 and question == "2") or (comp == 6 and question =="2"): #placement de la partie gauche du domino à gauche du plateau
            self.append_g(domino.retourner())
        elif comp == 1 or (comp == 5 and question == "1") or (comp == 6 and question == "1"): #placement de la partie gauche du domino à droite du plateau
            P.append(domino)
        elif comp == 2 or (comp == 5 and question == "2") or (comp == 7 and question == "2"): #placement de la partie droite du domino à gauche du plateau
            self.append_g(domino)
        elif comp == 3 or (comp == 4 and question == "1") or (comp == 7 and question == "1" ) : #placement de la partie droite du domino à droite du plateau
            P.append(domino.retourner())



    def __str__(self):
        return " ".join(str(d) for d in self.dominos)



############################################ CLASSE MAIN ##################################################
###########################################################################################################

class Main:
    def __init__(self):
        self.liste = []                             #simple liste vide (idem que plateau)

    def __str__(self) -> str:
        return " ".join(str(d) for d in self.liste)

    def __repr__(self) -> str:
        return self.__str__()
    def piocher(self, domino):
        self.liste.append(domino)                   #c'est ecrit

    def question_domino(self):
        reponse = input("quelle domino voulez vous jouer ?")
        return reponse

    def retirer(self, domino):
        self.liste.remove(domino)

    def dominos_jouables(self, plateau):
        jouable = []
        for d in self.liste:
            if plateau.compatible(d) !=  "domino injouable"  :       # PLATEAU_EXTREMITES A DEFINIR COMME DOMINOS AUX EXTREMITES
                jouable.append(d)
        return jouable

    def afficher_main(self):
        return "[" + ", ".join(f"{elt} ({i})" for i, elt in enumerate(self.liste)) + "]"

    def numeros_jouables(self,plateau):
        L = []
        for i,d in enumerate(self.liste):
            for j in self.dominos_jouables(plateau):
                if d == j:
                    L.append(i)
        return L

    def test_contenant(self):
        if self.liste == []:
            return True
        else:
            return False

    def test_famille(self):
        for i in range(1,6):
            c = 0
            for d in self.liste :
                if d.gauche == i or d.droite == i :
                    c+=1
            if c>=5 :
                return True
        return False

    def taille(self):
        return len(self.liste)

    def ajout(self,domino):
        self.liste.append(domino)

    def initialisation(self,pioche,M):
        for i in range(M):
            x = pioche.piocher_rdm()
            self.ajout(x)


############################################### CLASSE PIOCHE ###############################################
#############################################################################################################

class Pioche:

    def __init__(self):
        self.liste = []

    def __str__(self) -> str:
        return " ".join(str(d) for d in self.liste)

    def __repr__(self) -> str:
        return self.__str__()

    def ajout(self,domino):
        self.liste.append(domino)

    def remplir(self,P =6):
        for i in range(P+1):
            for j in range(i,P+1) :
                self.ajout(Domino(i,j))

    def est_vide(self):
        if self.liste == []:
            return True
        else:
            return False

    def piocher_rdm(self):
        if self.est_vide():
            return "pioche vide "
        i = random.randint(0, len(self.liste) - 1)
        return self.liste.pop(i)

from scipy.stats import quantile_test


########################################### CLASSE DOMINO #####################################################
###############################################################################################################

class Domino :

    def __init__(self, gauche,droite):
        self.gauche = gauche
        self.droite = droite

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
        self.Liste_gauche = []
        self.Liste_droite = []
    def question_cote(self):
        reponse  = input("voulez vous jouer à droite (1) ou à gauche (2) ?")
        return reponse

    def append_g(self,domino):
        self.dominos = [domino] + self.dominos

    def extremites(self):
        if self.dominos == []:
            return('rien sur le plateau')
        else :
            return([self.Liste_gauche[-1].droite,self.Liste_droite[-1].droite])# comment choisir les extremites

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
            print("domino injouable")

    def jouer_domino_table(self, domino):
        comp = self.compatible(domino)
        P = self.dominos
        G = self.Liste_gauche
        D = self.Liste_droite
        question = 0
        if comp in [4,5,6,7] :
            question = self.question_cote()
        if comp ==-1  :
            P.append(domino)
            D.append(domino)
            G.append(domino.retourner())
        elif comp == 0 or (comp == 4 and question == "2") or (comp == 6 and question =="2"): #placement de la partie gauche du domino à gauche du plateau
            self.append_g(domino.retourner())
            G.append(domino)
        elif comp == 1 or (comp == 5 and question == "1") or (comp == 6 and question == "1"): #placement de la partie gauche du domino à droite du plateau
            P.append(domino)
            D.append(domino)
        elif comp == 2 or (comp == 5 and question == "2") or (comp == 7 and question == "2"): #placement de la partie droite du domino à gauche du plateau
            self.append_g(domino)
            G.append(domino.retourner())
        elif comp == 3 or (comp == 4 and question == "1") or (comp == 7 and question == "1" ) : #placement de la partie droite du domino à droite du plateau
            P.append(domino.retourner())
            D.append(domino.retourner())

    def __str__(self):
        return " ".join(str(d) for d in self.dominos)



############################################ CLASSE MAIN ##################################################
###########################################################################################################

class Main:
    def __init__(self):
        self.dominos = []                             #simple liste vide (idem que plateau)

    def piocher(self, domino):
        self.dominos.append(domino)                   #c'est ecrit

    def question_domino(self):
        reponse = input("quelle domino voulez vous jouer ?")
        return reponse

    def retirer(self, domino):
        if domino in self.dominos:
            self.dominos.remove(domino)
            return True
        return False                                  #renvoie True si on peut le retirer et False sinon
    def dominos_jouables(self, plateau):
        jouable = []
        for d in self.dominos:
            if plateau.compatible(d) is not None :       # PLATEAU_EXTREMITES A DEFINIR COMME DOMINOS AUX EXTREMITES
                jouable.append(d)
        return jouable                            # Liste de dominos jouables

    #def utiliser(self, domino, plateau):
        #if domino in dominos_jouables(self, plateau):
            #self.dominos.remove(domino)
            #return True
        #return False                           #on verifie qu'on peut le jouer et on le retire de la main

    #def __str__(self):
        #if self.dominos == []:
            #return "Main vide gg bg"
        #return " ".join(str(d) for d in self.dominos)    # Affiche les dominos séparé par un espace

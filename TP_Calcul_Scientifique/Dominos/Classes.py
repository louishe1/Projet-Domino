
########################################### CLASSE DOMINO #####################################################
###############################################################################################################

class Domino :

    def __init__(self, gauche,droite):
        self.gauche = gauche
        self.droite = droite

    def est_un_double(self):
        return(self.gauche == self.droite)

    def valeur_domino(self):
        return(self.gauche + self.droite)                      #somme des valeurs

    def retourner(self):
        self.gauche, self.droite = self.droite, self.gauche
        return(self)                                           #modifie le domino en l'inversant

    def compatibles(self,other):
        return(self.gauche == other.gauche
               or self.droite == other.droite
               or self.droite == other.gauche
               or self.gauche == other.droite)                #verifie qu'une valeur est commune

    def __str__(self):
        return f"[{self.gauche}|{self.droite}]"                #affiche un beau domino

####################################### CLASSE PLATEAU ###################################################
##########################################################################################################

class Plateau :
    def __init__(self):
        self.dominos = []                             #simple liste vide

    def extremites(self):                            # definir en revoyant une liste de 2 dominos
        if self.dominos == []:
            print('rien sur le plateau')
        elif len(self.dominos) == 1 :
            return(self.dominos[0], self.dominos[0])
        else                                                  # comment choisir les extremites




    def jouer_domino_table(self, domino):
        self.dominos.append(domino)






############################################ CLASSE MAIN ##################################################
###########################################################################################################

class Main:
    def __init__(self):
        self.dominos = []                             #simple liste vide (idem que plateau)

    def piocher(self, domino):
        self.dominos.append(domino)                   #c'est ecrit

    def retirer(self, domino):
        if domino in self.dominos:
            self.dominos.remove(domino)
            return True
        return False                                  #renvoie True si on peut le retirer et False sinon

#    def dominos_jouables(self, plateau):

#        jouable = []
#        for d in self.dominos:
#            if d.compatibles(plateau.extremites()[0] or d.compatibles(plateau.extremites()[1]) :       # PLATEAU_EXTREMITES A DEFINIR COMME DOMINOS AUX EXTREMITES
#                jouable.append(d)
#        return jouable                            # Liste de dominos jouables

    def utiliser(self, domino, plateau):
        if domino in dominos_jouables(self, plateau):
            self.dominos.remove(domino)
            return True
        return False                           #on verifie qu'on peut le jouer et on le retire de la main

    def __str__(self):
        if self.dominos == []:
            return "Main vide gg bg"
        return " ".join(str(d) for d in self.dominos)    # Affiche les dominos séparé par un espace

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
        self.gauche, self.droite = self.droite, self.gauche
        return(self)                                           #modifie le domino en l'inversant

    def compatible(self,plateau):
        if self.gauche == extremites(plateau)[0] :
            return(0)
        if self.gauche == extremites(plateau)[1] :
            return(1)
        if self.droite == extremites(plateau)[0]:
            return(2)
        if self.droite == extremites(plateau)[1]:
            return(3)
        else:
            print('non compatibles')


    def __str__(self):
        return f"[{self.gauche}|{self.droite}]"                #affiche un beau domino

####################################### CLASSE PLATEAU ###################################################
##########################################################################################################

class Plateau :
    def __init__(self):
        self.dominos = []                       #simple liste vide
        self.Liste_gauche = []
        self.Liste_droite = []

    def extremites(self):
        if self.dominos == []:
            print('rien sur le plateau')
        else :
            return(self.dominos[0],self.dominos[-1])# comment choisir les extremites


    def jouer_domino_table(self, domino,cote):
        if compatible(domino,self) == 0 :
            self.dominos.append(Domino.retourner(domino))
            self.Liste_gauche.append(Domino.retourner(domino))
        if compatible(domino,self) == 1 :
            self.dominos.append(domino)
            self.Liste_droite.append(domino)
        if compatible(domino, self) == 0:
            self.dominos.append(domino)
            self.Liste_gauche.append(domino)
        if compatible(domino, self) == 1:
            self.dominos.append(Domino.retourner(domino))
            self.Liste_droite.append(Domino.retourner(domino))

    def __str__(self):
        return " ".join(str(d) for d in self.dominos)







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
def dominos_jouables(self, plateau):
    jouable = []
    for d in self.dominos:
        if Domino.compatible(d,plateau) :       # PLATEAU_EXTREMITES A DEFINIR COMME DOMINOS AUX EXTREMITES
            jouable.append(d)
    return jouable                            # Liste de dominos jouables

    def utiliser(self, domino, plateau):
        if domino in dominos_jouables(self, plateau):
            self.dominos.remove(domino)
            return True
        return False                           #on verifie qu'on peut le jouer et on le retire de la main

    def __str__(self):
        if self.dominos == []:
            return "Main vide gg bg"
        return " ".join(str(d) for d in self.dominos)    # Affiche les dominos séparé par un espace
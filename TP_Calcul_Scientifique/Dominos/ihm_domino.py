from PyQt6 import QtGui, QtCore, QtWidgets

from Classes import Domino, Plateau, Main, Pioche
from jeu import (
    nb_dominos_par_personnes,
    premier_joueur,
    ia_aleatoire,
    ia_gloutonne,
    ia_minmax,
    plus_petites_cles,
)


class CanvasPlateau(QtWidgets.QWidget):
    """Zone de dessin dédiée à l'affichage des dominos sur le plateau."""

    def __init__(self, manager, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.domino_painter = QtGui.QPainter()
        self.setMinimumHeight(200)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )

    def paintEvent(self, event):
        super().paintEvent(event)
        self.domino_painter.begin(self)
        self.domino_painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        fond = QtGui.QBrush(QtGui.QColor(245, 245, 240))
        self.domino_painter.fillRect(self.rect(), fond)

        stylo = QtGui.QPen(QtCore.Qt.GlobalColor.black)
        stylo.setWidth(2)
        self.domino_painter.setPen(stylo)
        self.domino_painter.setBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.white))

        font_chiffres = self.domino_painter.font()
        font_chiffres.setBold(True)
        font_chiffres.setPointSize(10)
        self.domino_painter.setFont(font_chiffres)

        x, y = 16, 16
        petit, grand = 28, 54
        espacement = 8
        marge_droite = self.width() - 16
        hauteur_ligne_courante = 0

        for d in self.manager.plateau.dominos:
            if d.est_un_double():
                w, h = petit, grand
            else:
                w, h = grand, petit

            if x != 16 and x + w > marge_droite:
                x = 16
                y += hauteur_ligne_courante + 12
                hauteur_ligne_courante = 0

            rect = QtCore.QRect(x, y, w, h)
            self.domino_painter.drawRoundedRect(rect, 5, 5)

            if d.est_un_double():
                milieu_y = y + h // 2
                self.domino_painter.drawLine(x, milieu_y, x + w, milieu_y)
                self.domino_painter.drawText(
                    QtCore.QRect(x, y, w, h // 2),
                    QtCore.Qt.AlignmentFlag.AlignCenter,
                    str(d.gauche),
                )
                self.domino_painter.drawText(
                    QtCore.QRect(x, milieu_y, w, h // 2),
                    QtCore.Qt.AlignmentFlag.AlignCenter,
                    str(d.droite),
                )
            else:
                milieu_x = x + w // 2
                self.domino_painter.drawLine(milieu_x, y, milieu_x, y + h)
                self.domino_painter.drawText(
                    QtCore.QRect(x, y, w // 2, h),
                    QtCore.Qt.AlignmentFlag.AlignCenter,
                    str(d.gauche),
                )
                self.domino_painter.drawText(
                    QtCore.QRect(milieu_x, y, w // 2, h),
                    QtCore.Qt.AlignmentFlag.AlignCenter,
                    str(d.droite),
                )

            x += w + espacement
            if h > hauteur_ligne_courante:
                hauteur_ligne_courante = h

        self.domino_painter.end()


class DominoIHMManager(QtWidgets.QMainWindow):
    """
    Gère l'interface graphique PyQt6 du jeu de dominos entièrement en code :
    - Vue menu / configuration (paramètres, modes IA, score cible multi-manches)
    - Vue partie / plateau (manches, scores, mains des humains, masquage des IA)
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jeu de Dominos - PyQt6")
        self.resize(940, 660)

        self.plateau = Plateau()
        self.pioche = Pioche()
        self.dico_mains = {}
        self.ordre_joueurs = []
        self.types_ia = []
        self.combos_ia = []

        self.max_chiffre = 6
        self.nb_participants = 2
        self.nb_humains = 1
        self.nb_dominos_init = 7
        self.cible_score = 50

        self.num_manche = 1
        self.scores_cumules = {}
        self.tour_index = 0
        self.joueur_courant = None
        self.compteur_blocage = 0
        self.manche_terminee = False
        self.match_termine = False

        self.indice_domino_selectionne = None
        self.cote_choisi = "1"

        self.stack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)

        self.vue_menu = self._construire_vue_menu()
        self.vue_partie = self._construire_vue_partie()

        self.stack.addWidget(self.vue_menu)
        self.stack.addWidget(self.vue_partie)
        self.stack.setCurrentWidget(self.vue_menu)

        self._synchroniser_combos_ia()
        self.maj_parametres()

    def _construire_vue_menu(self):
        widget = QtWidgets.QWidget()
        layout_principal = QtWidgets.QVBoxLayout(widget)

        titre = QtWidgets.QLabel("Configuration de la partie de Dominos")
        font_titre = titre.font()
        font_titre.setPointSize(16)
        font_titre.setBold(True)
        titre.setFont(font_titre)
        titre.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(titre)

        form_layout = QtWidgets.QFormLayout()

        self.spin_max_chiffre = QtWidgets.QSpinBox()
        self.spin_max_chiffre.setRange(1, 12)
        self.spin_max_chiffre.setValue(6)
        form_layout.addRow("Chiffre maximal sur les dominos :", self.spin_max_chiffre)

        self.spin_nb_participants = QtWidgets.QSpinBox()
        self.spin_nb_participants.setRange(2, 4)
        self.spin_nb_participants.setValue(2)
        form_layout.addRow("Nombre total de participants (2 à 4) :", self.spin_nb_participants)

        self.spin_nb_humains = QtWidgets.QSpinBox()
        self.spin_nb_humains.setRange(0, 4)
        self.spin_nb_humains.setValue(1)
        form_layout.addRow("Nombre de joueurs humains :", self.spin_nb_humains)

        self.spin_cible_score = QtWidgets.QSpinBox()
        self.spin_cible_score.setRange(1, 99)
        self.spin_cible_score.setValue(50)
        form_layout.addRow("Score cible du match (1 à 99) :", self.spin_cible_score)

        layout_principal.addLayout(form_layout)

        groupe_ia = QtWidgets.QGroupBox("Modes des IA")
        self.layout_combos_ia = QtWidgets.QFormLayout(groupe_ia)
        layout_principal.addWidget(groupe_ia)

        boutons_layout = QtWidgets.QHBoxLayout()
        self.btn_lancer = QtWidgets.QPushButton("Lancer le match")
        self.btn_charger = QtWidgets.QPushButton("Charger sauvegarde (TODO)")
        boutons_layout.addWidget(self.btn_lancer)
        boutons_layout.addWidget(self.btn_charger)
        layout_principal.addLayout(boutons_layout)

        self.spin_max_chiffre.valueChanged.connect(self.maj_parametres)
        self.spin_nb_participants.valueChanged.connect(self._on_nb_joueurs_change)
        self.spin_nb_humains.valueChanged.connect(self._on_nb_joueurs_change)
        self.spin_cible_score.valueChanged.connect(self.maj_parametres)
        self.btn_lancer.clicked.connect(self.lancer_partie)
        self.btn_charger.clicked.connect(self.charger_sauvegarde)

        return widget

    def _construire_vue_partie(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)

        barre_haut = QtWidgets.QHBoxLayout()
        self.label_manche = QtWidgets.QLabel("Manche : 1")
        self.label_cible = QtWidgets.QLabel("Cible : 50")
        self.label_tour = QtWidgets.QLabel("Tour : -")
        self.label_pioche = QtWidgets.QLabel("Pioche : -")
        self.label_cote = QtWidgets.QLabel("Côté : Droite")
        self.btn_retour_menu = QtWidgets.QPushButton("Retour menu")

        barre_haut.addWidget(self.label_manche)
        barre_haut.addWidget(self.label_cible)
        barre_haut.addWidget(self.label_tour)
        barre_haut.addWidget(self.label_pioche)
        barre_haut.addWidget(self.label_cote)
        barre_haut.addStretch()
        barre_haut.addWidget(self.btn_retour_menu)
        layout.addLayout(barre_haut)

        self.conteneur = CanvasPlateau(self)
        layout.addWidget(self.conteneur)

        zone_bas = QtWidgets.QHBoxLayout()

        main_box = QtWidgets.QVBoxLayout()
        self.label_main = QtWidgets.QLabel("Main du joueur humain :")
        main_box.addWidget(self.label_main)
        self.liste_main = QtWidgets.QListWidget()
        main_box.addWidget(self.liste_main)
        zone_bas.addLayout(main_box, stretch=2)

        actions_box = QtWidgets.QVBoxLayout()
        self.btn_gauche = QtWidgets.QPushButton("Côté Gauche")
        self.btn_droite = QtWidgets.QPushButton("Côté Droite")
        self.btn_jouer = QtWidgets.QPushButton("Jouer le domino")
        self.btn_piocher = QtWidgets.QPushButton("Piocher / Passer")
        self.btn_tour_ia = QtWidgets.QPushButton("Tour IA suivant")
        self.btn_manche_suivante = QtWidgets.QPushButton("Manche suivante")

        actions_box.addWidget(self.btn_gauche)
        actions_box.addWidget(self.btn_droite)
        actions_box.addWidget(self.btn_jouer)
        actions_box.addWidget(self.btn_piocher)
        actions_box.addWidget(self.btn_tour_ia)
        actions_box.addWidget(self.btn_manche_suivante)
        zone_bas.addLayout(actions_box, stretch=1)

        log_box = QtWidgets.QVBoxLayout()
        log_box.addWidget(QtWidgets.QLabel("Journal de partie :"))
        self.text_log = QtWidgets.QTextEdit()
        self.text_log.setReadOnly(True)
        log_box.addWidget(self.text_log)
        zone_bas.addLayout(log_box, stretch=2)

        layout.addLayout(zone_bas)

        self.btn_gauche.clicked.connect(lambda: self.definir_cote("2"))
        self.btn_droite.clicked.connect(lambda: self.definir_cote("1"))
        self.btn_jouer.clicked.connect(self.action_joueur_jouer)
        self.btn_piocher.clicked.connect(self.action_joueur_piocher)
        self.btn_tour_ia.clicked.connect(self.executer_prochain_tour)
        self.btn_manche_suivante.clicked.connect(self.demarrer_manche_suivante)
        self.btn_retour_menu.clicked.connect(self.retour_menu)
        self.liste_main.currentRowChanged.connect(self.selectionner_domino)

        return widget

    def _on_nb_joueurs_change(self):
        self._synchroniser_combos_ia()
        self.maj_parametres()

    def _synchroniser_combos_ia(self):
        nb_total = int(self.spin_nb_participants.value())
        self.spin_nb_humains.setMaximum(nb_total)
        if self.spin_nb_humains.value() > nb_total:
            self.spin_nb_humains.setValue(nb_total)

        nb_humains = int(self.spin_nb_humains.value())
        nb_ia = max(0, nb_total - nb_humains)

        while self.layout_combos_ia.rowCount() > 0:
            self.layout_combos_ia.removeRow(0)
        self.combos_ia.clear()

        for i in range(nb_ia):
            combo = QtWidgets.QComboBox()
            combo.addItems([
                "0 - IA Aléatoire",
                "1 - IA Gloutonne",
                "2 - IA Minmax",
            ])
            combo.setCurrentIndex(min(1, i))
            combo.currentIndexChanged.connect(self.maj_parametres)
            self.layout_combos_ia.addRow(f"IA_{i} :", combo)
            self.combos_ia.append(combo)

    def maj_parametres(self):
        self.max_chiffre = int(self.spin_max_chiffre.value())
        self.nb_participants = int(self.spin_nb_participants.value())

        self.spin_nb_humains.setMaximum(self.nb_participants)
        if self.spin_nb_humains.value() > self.nb_participants:
            self.spin_nb_humains.setValue(self.nb_participants)

        self.nb_humains = int(self.spin_nb_humains.value())
        self.cible_score = max(1, min(99, int(self.spin_cible_score.value())))
        self.types_ia = [int(combo.currentIndex()) for combo in self.combos_ia]
        self.nb_dominos_init = nb_dominos_par_personnes(self.nb_participants)

    def charger_sauvegarde(self):
        self.log_message("charger_sauvegarde : TODO")

    def retour_menu(self):
        self.stack.setCurrentWidget(self.vue_menu)

    def lancer_partie(self):
        self.maj_parametres()
        self.text_log.clear()
        self.num_manche = 1
        self.match_termine = False

        self.scores_cumules = {}
        for i in range(self.nb_humains):
            self.scores_cumules[f"Joueur_{i}"] = 0
        for i in range(self.nb_participants - self.nb_humains):
            self.scores_cumules[f"IA_{i}"] = 0

        self.log_message(
            f"Nouveau match démarré | Cible : {self.cible_score} pts | Participants : {self.nb_participants} ({self.nb_humains} humain(s))."
        )
        self._preparer_manche()
        self.stack.setCurrentWidget(self.vue_partie)
        self.rafraichir_ihm()

    def demarrer_manche_suivante(self):
        if not self.manche_terminee or self.match_termine:
            return
        self.num_manche += 1
        self.log_message(f"--- Début de la manche {self.num_manche} ---")
        self._preparer_manche()
        self.rafraichir_ihm()

    def _preparer_manche(self):
        self.plateau = Plateau()
        self.pioche = Pioche()
        self.pioche.remplir(self.max_chiffre)

        self.dico_mains = {}
        for i in range(self.nb_humains):
            m = Main()
            m.initialisation(self.pioche, self.nb_dominos_init)
            self.dico_mains[f"Joueur_{i}"] = m

        nb_ia = self.nb_participants - self.nb_humains
        for i in range(nb_ia):
            m = Main()
            m.initialisation(self.pioche, self.nb_dominos_init)
            self.dico_mains[f"IA_{i}"] = m

        self.ordre_joueurs = list(self.dico_mains.keys())
        for nom in self.ordre_joueurs:
            self.scores_cumules.setdefault(nom, 0)

        joueur_depart, domino_depart = premier_joueur(self.dico_mains)

        self.plateau.dominos.append(domino_depart)
        self.dico_mains[joueur_depart].retirer(domino_depart)

        index_depart = self.ordre_joueurs.index(joueur_depart)
        self.tour_index = 1
        self.joueur_courant = self.ordre_joueurs[
            (index_depart + self.tour_index) % len(self.ordre_joueurs)
        ]
        self.compteur_blocage = 0
        self.manche_terminee = False
        self.indice_domino_selectionne = None
        self.cote_choisi = "1"
        self.label_cote.setText("Côté : Droite")

        self.log_message(
            f"[Manche {self.num_manche}] {joueur_depart} pose {domino_depart}. Tour de {self.joueur_courant}."
        )

    def definir_cote(self, cote):
        self.cote_choisi = cote
        self.label_cote.setText(f"Côté : {'Gauche' if cote == '2' else 'Droite'}")

    def selectionner_domino(self, row):
        self.indice_domino_selectionne = row if row >= 0 else None

    def _poser_domino_avec_cote(self, domino, comp, cote):
        if comp == 4 and cote == "2":
            self.plateau.append_g(domino.retourner())
        elif comp == 4 and cote == "1":
            self.plateau.dominos.append(domino.retourner())
        elif comp == 5 and cote == "1":
            self.plateau.dominos.append(domino)
        elif comp == 5 and cote == "2":
            self.plateau.append_g(domino)
        elif comp == 6 and cote == "2":
            self.plateau.append_g(domino.retourner())
        elif comp == 6 and cote == "1":
            self.plateau.dominos.append(domino)
        elif comp == 7 and cote == "2":
            self.plateau.append_g(domino)
        elif comp == 7 and cote == "1":
            self.plateau.dominos.append(domino.retourner())

    def action_joueur_jouer(self):
        if self.manche_terminee or self.match_termine or not self.joueur_courant.startswith("Joueur"):
            return

        main_joueur = self.dico_mains[self.joueur_courant]
        jouables = main_joueur.numeros_jouables(self.plateau)

        if (
            self.indice_domino_selectionne is None
            or self.indice_domino_selectionne not in jouables
        ):
            self.log_message("Sélectionne un domino jouable dans la liste.")
            return

        domino = main_joueur.liste[self.indice_domino_selectionne]
        comp = self.plateau.compatible(domino)

        if comp in [4, 5, 6, 7]:
            self._poser_domino_avec_cote(domino, comp, self.cote_choisi)
        else:
            self.plateau.jouer_domino_table_humain(domino)

        main_joueur.retirer(domino)
        self.compteur_blocage = 0
        self.log_message(f"{self.joueur_courant} joue {domino}.")
        self._avancer_apres_action(main_joueur)

    def action_joueur_piocher(self):
        if self.manche_terminee or self.match_termine or not self.joueur_courant.startswith("Joueur"):
            return

        main_joueur = self.dico_mains[self.joueur_courant]
        if main_joueur.numeros_jouables(self.plateau):
            self.log_message("Tu as déjà un domino jouable.")
            return

        if not self.pioche.est_vide():
            pio = self.pioche.piocher_rdm()
            if isinstance(pio, Domino):
                main_joueur.piocher(pio)
                self.compteur_blocage = 0
                self.log_message(f"{self.joueur_courant} pioche {pio}.")
        else:
            self.compteur_blocage += 1
            self.log_message(f"{self.joueur_courant} passe son tour (pioche vide).")

        self._avancer_apres_action(main_joueur)

    def executer_prochain_tour(self):
        if self.manche_terminee or self.match_termine or self.joueur_courant.startswith("Joueur"):
            return

        main_ia = self.dico_mains[self.joueur_courant]
        idx_ia = int(self.joueur_courant.split("_")[1])
        mode_ia = self.types_ia[idx_ia] if idx_ia < len(self.types_ia) else 0

        jouables = main_ia.numeros_jouables(self.plateau)
        if jouables:
            if mode_ia == 0:
                idx = ia_aleatoire(main_ia, self.plateau)
            elif mode_ia == 1:
                idx = ia_gloutonne(main_ia, self.plateau)
            else:
                idx = ia_minmax(main_ia, self.plateau, self.pioche, profondeur=3)

            domino = main_ia.liste[idx]
            self.plateau.jouer_domino_table_ia(domino, mode_ia)
            main_ia.retirer(domino)
            self.compteur_blocage = 0
            self.log_message(f"{self.joueur_courant} joue {domino}.")
        elif not self.pioche.est_vide():
            pio = self.pioche.piocher_rdm()
            if isinstance(pio, Domino):
                main_ia.piocher(pio)
                self.compteur_blocage = 0
                self.log_message(f"{self.joueur_courant} pioche un domino.")
        else:
            self.compteur_blocage += 1
            self.log_message(f"{self.joueur_courant} passe son tour.")

        self._avancer_apres_action(main_ia)

    def _cloturer_manche(self, main_courante):
        self.manche_terminee = True

        scores_manche = {
            nom: sum(d.valeur() for d in main.liste)
            for nom, main in self.dico_mains.items()
        }
        for nom, pts in scores_manche.items():
            self.scores_cumules[nom] = self.scores_cumules.get(nom, 0) + pts

        if len(main_courante.liste) == 0:
            self.log_message(f"FIN DE MANCHE {self.num_manche} : {self.joueur_courant} a posé tous ses dominos.")
        else:
            gagnants_manche = plus_petites_cles(scores_manche)
            self.log_message(
                f"FIN DE MANCHE {self.num_manche} (blocage) : plus petit score de manche {gagnants_manche}."
            )

        self.log_message(f"Scores de la manche {self.num_manche} : {scores_manche}")
        self.log_message(f"Scores cumulés : {self.scores_cumules}")

        # Mains des joueurs humains uniquement (les mains des IA restent secrètes)
        for nom, main in self.dico_mains.items():
            if nom.startswith("Joueur"):
                dominos_str = " ".join(str(d) for d in main.liste) if main.liste else "(aucun domino)"
                self.log_message(f"Main de {nom} : {dominos_str}")

        # Vérification de la cible du match (somme des scores >= cible)
        joueurs_cible = [
            nom for nom, total in self.scores_cumules.items() if total >= self.cible_score
        ]
        if joueurs_cible:
            self.match_termine = True
            gagnants_match = plus_petites_cles(self.scores_cumules)
            self.log_message(
                f"=== FIN DU MATCH (cible {self.cible_score} dépassée par {joueurs_cible}) ==="
            )
            self.log_message(f"Scores finaux du match : {self.scores_cumules}")
            self.log_message(f"Gagnant(s) du match (plus petit total) : {gagnants_match}")
            for nom, main in self.dico_mains.items():
                if nom.startswith("Joueur"):
                    dominos_str = " ".join(str(d) for d in main.liste) if main.liste else "(aucun domino)"
                    self.log_message(f"Main finale de {nom} : {dominos_str}")
        else:
            self.log_message(
                f"Cible {self.cible_score} non atteinte : clique sur 'Manche suivante' pour continuer."
            )

    def _avancer_apres_action(self, main_courante):
        if len(main_courante.liste) == 0 or self.compteur_blocage >= self.nb_participants:
            self._cloturer_manche(main_courante)
        else:
            self.tour_index += 1
            self.joueur_courant = self.ordre_joueurs[
                self.tour_index % len(self.ordre_joueurs)
            ]

        self.indice_domino_selectionne = None
        self.rafraichir_ihm()

    def log_message(self, texte):
        self.text_log.append(texte)

    def rafraichir_ihm(self):
        self.label_manche.setText(f"Manche : {self.num_manche}")
        self.label_cible.setText(f"Cible : {self.cible_score}")
        self.label_tour.setText(f"Tour : {self.joueur_courant}")
        self.label_pioche.setText(f"Pioche : {len(self.pioche.liste)} domino(s)")

        partie_active = not self.manche_terminee and not self.match_termine
        est_humain = (
            partie_active
            and isinstance(self.joueur_courant, str)
            and self.joueur_courant.startswith("Joueur")
        )

        self.liste_main.clear()
        if est_humain and self.joueur_courant in self.dico_mains:
            self.label_main.setText(f"Main de {self.joueur_courant} :")
            main_affichee = self.dico_mains[self.joueur_courant]
            jouables = set(main_affichee.numeros_jouables(self.plateau))
            for i, d in enumerate(main_affichee.liste):
                tag = " [JOUABLE]" if i in jouables else ""
                self.liste_main.addItem(f"{i} : {d}{tag}")
        else:
            self.label_main.setText("Main cachée (tour d'une IA ou manche terminée)")

        self.liste_main.setEnabled(est_humain)
        self.btn_jouer.setEnabled(est_humain)
        self.btn_piocher.setEnabled(est_humain)
        self.btn_gauche.setEnabled(est_humain)
        self.btn_droite.setEnabled(est_humain)
        self.btn_tour_ia.setEnabled(partie_active and not est_humain)
        self.btn_manche_suivante.setEnabled(self.manche_terminee and not self.match_termine)

        self.conteneur.update()
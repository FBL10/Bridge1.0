class Joueur:

    def __init__(self, nom, cartes, humain, rang_e):

        self.pts = 0
        self.nom = nom
        self.cartes = cartes
        self.humain = humain  # Humain ou machine
        self.coups = []  # Cartes jouées
        self.rang_e = rang_e  # Ordre des enchères(N=1, E=2, S=3, O=4)
        self.rang_l = 0  # rang dans la levée en cours(dynamique, changé par contrôleur)
        self.levees = 0  # Nombre de levées remportées
        self.equil = False  # indicateur de main équilibrée
        self.equiTxt = "Non-Eq"  # équilibre en texte
        self.pique = 0  # nb piques
        self.coeur = 0
        self.carreau = 0
        self.trefle = 0
        self.piquePts = 0  # nb pts pique
        self.coeurPts = 0
        self.carreauPts = 0
        self.treflePts = 0
        self.piqueHon = 0  # nb honneurs pique incluant 10
        self.coeurHon = 0
        self.carreauHon = 0
        self.trefleHon = 0
        self.pique_bon = False
        self.coeur_bon = False
        self.carreau_bon = False
        self.trefle_bon = False
        self.maxDistro = 0  # plus longue
        self.minDistro = 0  # plus courte
        self.distro = ()  # distribution en couleurs croissantes
        self.distroOrd = ()  # distribution en index de couleurs croissantes
        self.longue1 = ""  # plus longue
        self.longue2 = ""  # 2eme plus longue
        self.longue3 = ""  # plus courte
        self.longue4 = ""  # 2eme plus courte
        self.bonLongue1 = False
        self.bonLongue2 = False
        self.ptsDistro = 0  # pts de longueur
        self.ptsTot = 0  # points + points de longueur
        self.reg20 = 0  # points + 2 nb 2 plus longues
        self.ouvre = False  # main d'ouverture
        self.ouverture = ""  # 1ere enchère
        self.majeur5 = False  # majeure 5e
        self.fit = False  # fit trouve?
        self.barrage = False  # main de barrage?
        self.role = ""  # role dans enchères
        self.capitaine = False  # capitaine des enchères ?
        self.forceOuv = ""  # force d'ouvreur
        self.forceRep = ""  # force de répondant
        self.intervient = False  # main d'intervention?
        self.couleurs = ("P", "C", "K", "T", "S")  # liste des couleurs
        self.couleurs_nom = ("Pique", "Coeur", "Carreau", "Trèfle", "Sans-Atout")

    def encherir(self, tab_e, ouvert):
        if self.humain:
            return input("\nenchère de " + self.nom + " : ")
        else:
            return self.enchere()

    def jouer(self, tab_c, tab_t):
        if self.humain:
            coup = input("\n" + self.nom + " : ")
            return coup
        else:
            pass  # TODO

    # @property
    # retirer annule fonction print
    def evaluer(self):
        # compte points
        for i in self.cartes:
            self.pts += i.p
            if i.val < 15:
                self.trefle += 1
                self.treflePts += i.p
                if 10 <= i.val <= 14:
                    self.trefleHon += 1
            elif 14 < i.val < 28:
                self.carreau += 1
                self.carreauPts += i.p
                if 23 <= i.val <= 27:
                    self.carreauHon += 1
            elif 27 < i.val < 41:
                self.coeur += 1
                self.coeurPts += i.p
                if 36 <= i.val <= 40:
                    self.coeurHon += 1
            else:
                self.pique += 1
                self.piquePts += i.p
                if i.val >= 48:
                    self.piqueHon += 1

        # évalue distribution
        self.distro = [self.pique, self.coeur, self.carreau, self.trefle]
        # self.distro = [self.trefle, self.carreau, self.coeur, self.pique]

        self.ptsDistro = max(0, sorted(self.distro)[3] - 4) + max(0, sorted(self.distro)[2] - 4)
        self.ptsTot = self.pts + self.ptsDistro
        # Tri par index - attention égalités favorisent le faible
        # https://stackoverflow.com/questions/7851077/how-to-return-index-of-a-sorted-list
        # self.distroOrd = sorted(range(len(self.distro)), key=lambda k: sorted(self.distro[k], reverse= True)
        # self.distroOrd = sorted(self.distro, reverse=True)
        self.distroOrd = sorted(range(len(self.distro)), key=lambda k: self.distro[k])
        # https://stackoverflow.com/questions/3382352/equivalent-of-numpy-argsort-in-basic-python
        # self.distroOrd = [i for (v, i) in sorted((v, i) for (i, v) in enumerate(self.distro))]
        # TODO réordonner les égalités : plus fort en premier (?)
        self.longue1 = self.couleurs[self.distroOrd[3]]  # plus longue
        self.longue2 = self.couleurs[self.distroOrd[2]]  # 2eme plus longue
        self.longue3 = self.couleurs[self.distroOrd[1]]  # 2eme plus courte
        self.longue4 = self.couleurs[self.distroOrd[0]]  # plus courte
        # identifie si longue1 ou longue2 sont "bonnes" 2 des top 3 ou 3 des tops 5
        # self.bonLongue1

        # évalue majeur 5
        if self.pique >= 5 or self.coeur >= 5:
            self.majeur5 = True

        # évalue équilibre
        self.maxDistro = max(self.distro)
        self.minDistro = min(self.distro)
        if self.minDistro >= 2 and sorted(self.distro)[1] >= 3:
            self.equil = True
            self.equiTxt = "Equil"

        # évalue barrage
        if 5 <= self.pts <= 10 and self.maxDistro >= 6 and self.longue1 != "T":
            self.barrage = True
            self.ouverture = str(self.maxDistro - 4) + self.longue1

        # évalue force d'ouvreur
        if self.ptsTot <= 16:
            self.forceOuv = "faible"
        elif 17 >= self.ptsTot <= 18:
            self.forceOuv = "medium"
        elif 19 >= self.ptsTot <= 21:
            self.forceOuv = "fort"

    #  @property
    #  génère ouverture
    def enchere(self):

        self.reg20 = self.pts + sorted(self.distro)[3] + sorted(self.distro)[2]
        if self.ptsTot >= 13 or self.reg20 >= 20:
            self.ouvre = True

            if self.ptsTot >= 22:
                self.forceOuv = "fort+"
                self.ouverture = "2T"

            elif self.majeur5:
                if self.pique >= self.coeur:
                    self.ouverture = "1P"
                else:
                    if self.coeur >= 5:
                        self.ouverture = "1C"
            else:
                if self.equil:
                    if 15 <= self.ptsTot <= 17:
                        self.ouverture = "1S"
                    elif 20 <= self.ptsTot <= 21:
                        self.ouverture = "2S"
                    elif self.carreau >= self.trefle and self.carreau >= 3:
                        self.ouverture = "1K"
                    else:
                        self.ouverture = "1T"
                else:
                    if self.carreau >= self.trefle and self.carreau >= 3:
                        self.ouverture = "1K"
                    else:
                        self.ouverture = "1T"

        elif self.barrage:
            self.ouverture = str(self.maxDistro - 4) + self.longue1
        else:
            self.ouverture = "0X"

        #print("\n" + self.nom + " :", self.cartes, " ", self.distro, self.pts, self.ptsDistro, self.ptsTot, "pts",
              #self.equiTxt, "Ouvre=", self.ouvre, "Maj5=", self.majeur5, "Barr=", self.barrage, "Ouvr=", self.ouverture,
              #self.forceOuv, self.longue1, self.longue2, self.longue3, self.longue4)
        return self.ouverture

    def __str__(self):
        return self.nom

    def __repr__(self):
        return self.nom

    def add_carte(self, carte):
        self.coups.append(carte)
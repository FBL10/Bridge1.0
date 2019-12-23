import random
import itertools
import sys

from joueur import Joueur
from carte import Carte

e_running = True
tab_e = []
contrat = ["", Joueur]  # [contrat, joueur]
p_running = True
tab_c = []
ouvert = False
roles = {"ouvreur": None, "repondant": None, "defenseur1": None, "defenseur2": None}
tour = 0
dem = ''
att = ''
joueurs = []

def f_deb(e, joueurs):  # retourne le joueur qui va faire le contrat
    # e = tableau des enchères
    global contrat

    enseigne = e[-4][1][1]
    joueur = e[-4][0]  # contrat
    jrs = [e[-4][0], e[-2][0]]
    for i in reversed(e):
        if i[1][1:] == enseigne and (i[0] in jrs):
            joueur = i[0]
    contrat[1] = joueur
    if joueur.nom == "Ouest":
        joueurs.append(joueurs[0])
        joueurs.pop(0)
    return joueur

def definir_roles(joueur):
    global roles
    global joueurs

    for i, j in enumerate(joueurs):
        if joueur.nom == j.nom:
            roles["ouvreur"] = joueurs[i].nom
            roles["defenseur1"] = joueurs[(i + 1) % len(joueurs)].nom
            roles["repondant"] = joueurs[(i + 2) % len(joueurs)].nom
            roles["defenseur2"] = joueurs[(i + 3) % len(joueurs)].nom

    print("DEFINITION DES ROLES" , roles)


def enchere(joueur):

    global contrat
    global e_running
    global tab_e
    global ouvert
    global roles

    e_valides = ["P", "C", "K", "T", "S", "X"]

    e = joueur.encherir(tab_e, ouvert, roles)

    while e[1] not in e_valides and int(e[0]) in range(7):
        print("enchère invalide")
        e = joueur.encherir(tab_e, ouvert, roles)
    if e != "0X" :
        if ouvert == False:
            definir_roles(joueur)
        ouvert = True

    tab_e.append([joueur, e])
    if len(tab_e) > 3 and tab_e[-1][1] == tab_e[-2][1] == tab_e[-3][1] == "0X":
        e_running = False
        contrat[0] = tab_e[-4][1]
        if contrat[0] == "0X":
            contrat[0] = "aucun contrat"
            print(contrat[0])
            sys.exit()
        print("\ncontrat de " + tab_e[-4][0].nom + " et " + tab_e[-2][0].nom + " : " + contrat[0])



def coup(joueur, ncoups, tab_tour):

    global tab_c
    global p_running
    global dem
    cv = False  # Coup valide
    # cj = joueur.cartes[0]

    while not cv:
        c = joueur.jouer(tab_c, tab_tour)
        for i in joueur.cartes:
            if i.n == c and not i.j:
                if c[-1] == dem or absc(joueur, dem) or ncoups == 0:
                    if ncoups == 0:
                        dem = c[-1]
                    cv = True
                    i.j = True
                    joueur.add_carte(i)
        if not cv:
            print("coup invalide")


def absc(joueur, sorte):
    for c in joueur.cartes:
        if c.n[1] == sorte and not c.j:
            return False  # Si le joueur n'a pas d'abscence dans la sorte
    return True  # Si le joueur a une abscence dans la sorte


def c_deck():  # Crée les instances de cartes et de joueurs

    cartes = list(range(1, 53))
    for i in range(len(cartes)):
        if (i % 13) == 0:
            cartes[i] += 13
    random.shuffle(cartes)

    cartes[:13] = sorted(cartes[:13], reverse=True)
    cartes[13:26] = sorted(cartes[13:26], reverse=True)
    cartes[26:39] = sorted(cartes[26:39], reverse=True)
    cartes[39:] = sorted(cartes[39:], reverse=True)

    for i in range(52):
        v = cartes[i]
        cartes[i] = Carte(v)

    nord = Joueur("Nord", cartes[:13], False, 1)
    est = Joueur("Est", cartes[13:26], False, 2)
    sud = Joueur("Sud", cartes[26:39],False, 3)
    ouest = Joueur("Ouest", cartes[39:],True, 4)
    joueurs = [nord, est, sud, ouest]
    return joueurs


def check_win(tab_tour):  # retourne le joueur qui a gagné la levée

    global tour
    global dem
    global att

    m = tab_tour[0][0].val  # maximum
    j = tab_tour[0][1]

    for t in tab_tour:
        if t[0].n[-1] == dem:
            if t[0].val > m:
                m = t[0].val
                j = t[1]
        if t[0].n[-1] == att:
            if att != dem:
                m = t[0].val
                j = t[1]
                dem = att
            else:
                if t[0].val > m:
                    m = t[0].val
                    j = t[1]
    return j


def p_tab(t):
    tab = []
    for c in t:
        tab.append([c[0].n, c[1]])
    #print(tab)


def start(gen):

    print("starting")

    global tab_e
    global tab_c
    global e_running
    global p_running
    global tour
    global dem
    global att
    global contrat
    global joueurs

    joueurs = c_deck()

    cj = itertools.cycle(joueurs)

    for j in joueurs:
        j.evaluer()

    while e_running:
        for j in joueurs: pass
            #print("\n" + j.nom + " :", j.cartes)
        enchere(next(cj))
        if gen:
            return
    att = contrat[0][1]
    joueur = f_deb(tab_e, joueurs)
    j_comm = joueurs[joueurs.index(joueur)+1]
    while joueurs[0] is not j_comm:
        joueurs.append(joueurs[0])
        joueurs.pop(0)

    ncoups = 0
    while tour < 13:
        tab_tour = [0, 0, 0, 0]  # [[carte, joueur],...]
        win = joueurs[0]
        for j in joueurs:
            print(j.nom + " :", j.cartes)
            coup(j, ncoups, tab_tour)
            j.rang_l = ncoups
            tab_tour[ncoups] = [j.coups[-1], j]
            ncoups += 1
            if ncoups % 4 == 0:
                win = check_win(tab_tour)
                ncoups = 0
                tab_c.append(tab_tour)
                tour += 1
                p_tab(tab_tour)
                print("levée : " + win.nom)
        while joueurs[0] is not win:
            joueurs.append(joueurs[0])
            joueurs.pop(0)
        joueurs[0].levees += 1
        joueurs[2].levees += 1
    print("contrat : " + str(contrat[0]) + ", résultat : " + contrat[1].nom + " fait " + str(contrat[1].levees) + " levées")
    if int(contrat[0][0]) + 5 < contrat[1].levees:
        print("-> contrat réussi")
        sys.exit()
    else:
        print("-> contrat raté")
        sys.exit()


start(False)

# TODO : séparer le jeu et le menu en méthode séparée,
#  chacune appeleée par le controlleur quamd il le faut,
#  créer les cartes ???

import pygame

from bouton import Bouton
pygame.init()

display_info = pygame.display.Info()

WIDTH, HEIGHT = display_info.current_w, display_info.current_h

WIDTH, HEIGHT = 1000, 600 # Temporaire, seulement pour le dévelopement

win = pygame.display.set_mode((WIDTH, HEIGHT)) # pygame.FULLSCREEN
pygame.display.set_caption("Bridge1.0")

pygame.display.set_icon(pygame.transform.scale(pygame.image.load('images/back_cards-07.png').convert_alpha(), (32, 32)))

# start_ : bouton de début de partie dans le menu
start_largeur, start_hauteur = int(WIDTH/5), int(HEIGHT/10)
start_x, start_y = int(WIDTH/2 - (WIDTH/5)/2), int(HEIGHT/5)
start_image = pygame.transform.scale(pygame.image.load('images/jouer.png').convert_alpha(), (start_largeur, start_hauteur))
start_rect = pygame.Rect(start_x, start_y, start_largeur, start_hauteur)

# quit_ : bouton de sortie dans le menu
quit_largeur, quit_hauteur = int(WIDTH/5), int(HEIGHT/7)
quit_x, quit_y = int(WIDTH/2 - (WIDTH/5)/2), int(4/5 * HEIGHT)
quit_image = pygame.transform.scale(pygame.image.load('images/quitter.png').convert_alpha(), (quit_largeur, quit_hauteur))
quit_rect = pygame.Rect(quit_x, quit_y, quit_largeur, quit_hauteur)

# back_ : bouton de retour au menu dans le jeu
back_largeur, back_hauteur = int(WIDTH/12), int(HEIGHT/10)
back_x, back_y = int(WIDTH/100), int(HEIGHT/100)
back_image = pygame.transform.scale(pygame.image.load('images/retour.png').convert_alpha(), (back_largeur, back_hauteur))
back_rect = pygame.Rect(back_x, back_y, back_largeur, back_hauteur)

# bids_ : carte d'enchères
bids_largeur, bids_hauteur = (WIDTH//5), (HEIGHT//3)
bids_x, bids_y = (WIDTH//2), (HEIGHT//3)
bids_image = pygame.transform.scale(pygame.image.load('images/enchere.png').convert_alpha(), (bids_largeur, bids_hauteur))
bids_rects = []
bids_dim = {"marge_cotés": 82/712, "marge_dessus": 56/712, "largeur_petit": 98/712,
              "hauteur_petit": 65/712,  "hauteur_long": 98/712, "dist_long_pass": 16/712,
              "hauteur_pass": 96/712, "largeur_pass": 293/712}

encheres_possibles = ["1T", "1K", "1K", "1P", "1S", "2T", "2K", "2K", "2P", "2S", "3T", "3K", "3K", "3P", "3S",
                      "4T", "4K", "4K", "4P", "4S", "5T", "5K", "5K", "5P", "5S", "6T", "6K", "6K", "6P", "6S",
                      "7T", "7K", "7K", "7P", "7S", "0X"]

def make_encheres(encheres_valides):
    global bids_rects

    bids_rects = []
    for index, enchere in enumerate(encheres_valides):
        if index == 0:
            x = bids_x + bids_dim["marge_cotés"]*bids_largeur
            y = bids_y + bids_dim["marge_dessus"]*bids_hauteur
            largeur = bids_dim["largeur_petit"]*bids_largeur
            hauteur = bids_dim["hauteur_petit"]*bids_hauteur
            rect = pygame.Rect(x, y, largeur, hauteur)
            bids_rects.append(rect)

# bg_ : background
menu_bg_image = pygame.transform.scale(pygame.image.load('images/menu_bg.png').convert_alpha(), (WIDTH, HEIGHT))
playing_bg_image = pygame.transform.scale(pygame.image.load('images/playing_bg.png').convert_alpha(), (WIDTH, HEIGHT))

clock = pygame.time.Clock()

playing = False
menu = True
run = True
while run:

    clock.tick(45)

    win.fill(0)

    if menu :
        win.blit(menu_bg_image, (0, 0))
        win.blit(start_image, (start_x, start_y))
        win.blit(quit_image, (quit_x, quit_y))

    if playing :

        win.blit(playing_bg_image, (0, 0))
        win.blit(back_image, (back_x, back_y))
        win.blit(bids_image, (bids_x, bids_y))

        make_encheres(encheres_possibles)

        for rect in bids_rects:
            pygame.draw.rect(win, (0, 0, 0), rect)

    # Event handler
    for event in pygame.event.get():
        # Clique bouton gauche
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()

            if menu:
                # clique bouton jouer
                if start_rect.collidepoint(pos):
                    playing = True
                    menu = False

                # clique bouton quitter
                if quit_rect.collidepoint(pos):
                    run = False

            if playing:
                # clique bouton retour
                if back_rect.collidepoint(pos):
                    playing = False
                    menu = True

        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
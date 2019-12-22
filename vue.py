# TODO : séparer le jeu et le menu en méthode séparée,
#  chacune appeleée par le controlleur quamd il le faut,
#  créer les cartes ???

import pygame

from bouton import Bouton
pygame.init()

display_info = pygame.display.Info()

WIDTH, HEIGHT = display_info.current_w, display_info.current_h

#WIDTH, HEIGHT = 600, 400 # Temporaire, seulement pour le dévelopement

win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Bridge1.0")

pygame.display.set_icon(pygame.transform.scale(pygame.image.load('images/back_cards-07.png').convert_alpha(), (32, 32)))

# start_ : bouton de début de partie dans le menu
start_largeur, start_hauteur = int(WIDTH/5), int(HEIGHT/10)
start_x, start_y = int(WIDTH/2 - (WIDTH/5)/2), int(HEIGHT/5)
start_image = pygame.transform.scale(pygame.image.load('images/jouer.png').convert_alpha(), (start_largeur, start_hauteur))
start_bouton = Bouton(start_x, start_y, start_largeur, start_hauteur, "start")
start_rect = pygame.Rect(start_x, start_y, start_largeur, start_hauteur)

# quit_ : bouton de sortie dans le menu
quit_largeur, quit_hauteur = int(WIDTH/5), int(HEIGHT/7)
quit_x, quit_y = int(WIDTH/2 - (WIDTH/5)/2), int(4/5 * HEIGHT)
quit_image = pygame.transform.scale(pygame.image.load('images/quitter.png').convert_alpha(), (quit_largeur, quit_hauteur))
quit_bouton = Bouton(quit_x, quit_y, quit_largeur, quit_hauteur, "quit")
quit_rect = pygame.Rect(quit_x, quit_y, quit_largeur, quit_hauteur)

# back_ : bouton de retour au menu dans le jeu
back_largeur, back_hauteur = int(WIDTH/12), int(HEIGHT/10)
back_x, back_y = int(WIDTH/100), int(HEIGHT/100)
back_image = pygame.transform.scale(pygame.image.load('images/retour.png').convert_alpha(), (back_largeur, back_hauteur))
back_bouton = Bouton(back_x, back_y, back_largeur, back_hauteur, "back")
back_rect = pygame.Rect(back_x, back_y, back_largeur, back_hauteur)

# bg_ : background
menu_bg_image = pygame.transform.scale(pygame.image.load('images/menu_bg.png').convert_alpha(), (WIDTH, HEIGHT))
playing_bg_image = pygame.transform.scale(pygame.image.load('images/playing_bg.png').convert_alpha(), (WIDTH, HEIGHT))
clock = pygame.time.Clock()

# cartes_ : cartes de jeu




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

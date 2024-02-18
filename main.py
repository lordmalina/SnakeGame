# Snake vs. GhostSnake
# Jakub Malický, I. ročník, kruh 36
# Zimní semestr 2023/2024
# Programování 1 (NPRG030)

# import knihoven a ostatních souborů
import pygame

import button
import logo
import game_surface
import text
import snake
import hostile_snake

import random

def main(): # Hlavní funkce programu
    ### Inicializace knihovny Pygame
    pygame.init()


    ### Vytvoření okna
    screen = pygame.display.set_mode((800, 600)) # Rozlišení okna
    pygame.display.set_caption("Snake vs. GhostSnake 🐍") # Název okna
    pygame.display.set_icon(pygame.image.load("images/ikona.png")) # Ikona okna
    game_state = "main_menu" # Stav hry (main_menu, game, paused_game, game_over)
    pygame.display.toggle_fullscreen() # Zobrazení okna na celou obrazovku


    ### Logo hry
    game_logo_img = pygame.image.load("images/logo.png") # Obrázek loga hry
    game_logo = logo.Logo(400, 220, game_logo_img, 0.3) # Vytvoření loga hry, kde poslední parametr je velikost loga


    ### Tlačítka hry
    # Tlačítka v hlavním okně
    start_btn_img = pygame.image.load("images/startbutton.png") # Obrázek tlačítka start
    quit_btn_img = pygame.image.load("images/quitbutton.png") # Obrázek tlačítka quit
    start_hvr_img = pygame.image.load("images/startbutton_hover.png") # Obrázek tlačítka start při najetí myši
    quit_hvr_img = pygame.image.load("images/quitbutton_hover.png") # Obrázek tlačítka quit při najetí myši

    start_button = button.Button(250, 500, start_btn_img, 0.8, start_hvr_img) # Vytvoření tlačítka start
    quit_button = button.Button(550, 500, quit_btn_img, 0.8, quit_hvr_img) # Vytvoření tlačítka quit

    # Tlačítka v herním okně
    home_button_img = pygame.image.load("images/home_button.png") # Obrázek tlačítka home
    home_btn_hvr_img = pygame.image.load("images/home_button_hover.png") # Obrázek tlačítka home při najetí myši
    pause_button_img = pygame.image.load("images/pause_button.png") # Obrázek tlačítka pause
    pause_btn_hvr_img = pygame.image.load("images/pause_button_hover.png") # Obrázek tlačítka pause při najetí myši

    home_button = button.Button(60, 75, home_button_img, 0.13, home_btn_hvr_img) # Vytvoření tlačítka home
    pause_button = button.Button(140, 75, pause_button_img, 0.15, pause_btn_hvr_img) # Vytvoření tlačítka pause

    # Tlačítka v pozastavené hře
    home_button_paused_img = pygame.image.load("images/home_button.png") # Obrázek tlačítka home
    home_btn_pasued_hvr_img = pygame.image.load("images/home_button_hover.png") # Obrázek tlačítka home při najetí myši

    home_button_paused = button.Button(400, 500, home_button_paused_img, 0.13, home_btn_pasued_hvr_img) # Vytvoření tlačítka home


    ### Herní plocha
    # Počet sloupců a řádků musí být stejný, musí být sudé a zároveň musí dělit rozlišení okna beze zbytku
    gamesurface = game_surface.Grid(screen, 30, 30) # Vytvoření herní plochy


    ### Vytvoření fontu pro psaní textu
    font_paused_game1 = pygame.font.SysFont("Arial", 72) # font pro nápis GAME PAUSED
    font_paused_game2 = pygame.font.SysFont("Arial", 48) # font pro nápis Press SPACE to continue!
    font_pausing = pygame.font.SysFont("Arial", 16) # font pro nápis (ESC)
    font_score = pygame.font.SysFont("Arial", 32) # font pro nápis SCORE
    font_game_over = pygame.font.SysFont("Arial", 96) # font pro nápis GAME OVER

    paused_game_text1 = text.Text(screen, font_paused_game1, (0, 0, 0), 400, 100) # Vytvoření textu GAME PAUSED
    paused_game_text2 = text.Text(screen, font_paused_game2, (0, 0, 0), 400, 260) # Vytvoření textu Press SPACE to continue!
    pausing_text = text.Text(screen, font_pausing, (0, 0, 0), 140, 130) # Vytvoření textu (ESC)
    score_text = text.Text(screen, font_score, (0, 0, 0), 100, 300) # Vytvoření textu SCORE v herním okně
    score_text_num = text.Text(screen, font_score, (0, 0, 0), 100, 340) # Vytvoření textu skóre
    game_over_text = text.Text(screen, font_game_over, (0, 0, 0), 400, 160) # Vytvoření textu GAME OVER!
    game_over_score_text = text.Text(screen, font_score, (0, 0, 0), 400, 300) # Vytvoření textu SCORE v GAME OVER!


    ### Jídlo
    food = [0, 0] # Souřadnice jídla, které se od spuštění hry náhodně mění
    new_food = True  # Vytvoření proměnné, která kontroluje jestli předchozí jablko bylo sežráno


    ### Nepřátelští hadi
    # Vytvoření nepřátelského hada č. 1
    hostile_snake1 = hostile_snake.HostileSnake(gamesurface.center[0] + (gamesurface.cell_size[0] * (gamesurface.columns // 4)), 
                                   gamesurface.center[1] - (gamesurface.cell_size[1] * (gamesurface.rows // 4)), 
                                   gamesurface.cell_size[0], gamesurface, "down", 1)
    hostile_snake1.native_length() # Zvětšení hada na jeho původní délku


    ### Proměnné pro herní smyčku
    clock = pygame.time.Clock()

    fps = 15 # FPS

    CHANGE_DIRECTION = pygame.USEREVENT + 1 # Událost pro změnu směru nepřátelských hadů
    pygame.time.set_timer(CHANGE_DIRECTION, 750) # Časový interval pro změnu směru nepřátelských hadů


    ### Hlavní smyčka hry
    running = True
    while running:
        screen.fill((243, 239, 210)) # Změna barvy pozadí

        if game_state == "main_menu": # Podmínka pro hlavní menu
            # Podmínky pro přepnutí stavu hry
            if start_button.draw(screen) == True: # Podmínka pro spuštění hry
                game_state = "game"

                ### Restartování hry, při přechodu do herního okna
                # Restartování skóre
                score = 0

                # Restartování jablka
                new_food = True

                # Vytvoření hada a zárověň restartování hry
                play_snake = snake.Snake(gamesurface.center[0] - (gamesurface.cell_size[0] * (gamesurface.columns // 4)), 
                                         gamesurface.center[1] + (gamesurface.cell_size[1] * (gamesurface.rows // 4)), 
                                         gamesurface.cell_size[0], gamesurface, "up", fps) # Vytvoření hada. X a Y předstvují startovní pozici hada
                play_snake.native_length() # Zvětšení hada na jeho původní délku

                # restartování nepřátelských hadů
                hostile_snake1 = hostile_snake.HostileSnake(gamesurface.center[0] + (gamesurface.cell_size[0] * (gamesurface.columns // 4)), 
                                                            gamesurface.center[1] + (gamesurface.cell_size[1] * (gamesurface.rows // 4)), 
                                                            gamesurface.cell_size[0], gamesurface, "down", fps) # Vytvoření nepřátelského hada. X a Y předstvují startovní pozici hada
                hostile_snake1.native_length() # Zvětšení hada na jeho původní délku

            if quit_button.draw(screen) == True: # Podmínka pro opuštění hry
                running = False

            # Vykreslení loga
            game_logo.draw(screen)

        elif game_state == "game": # Podmínka pro herní okno
            # podmínky pro přepnutí stavu hry
            if home_button.draw(screen) == True: # Podmínka pro návrat do hlavního menu
                game_state = "main_menu"
            if pause_button.draw(screen) == True or pygame.key.get_pressed()[pygame.K_ESCAPE]: # Podmínka pro pozastavení hry
                game_state = "paused_game"

            # Změna FPS
            clock.tick(fps) # Změna rychlosti hry na 15 FPS

            # Vykreslení herní plochy
            gamesurface.draw()

            ### Jablko
            # Nové jablko
            if new_food == True: # Podmínka kontrolující jestli předchozí jablko bylo sežráno
                new_food = False

                valid_food = False # Proměnná, která kontroluje jestli je jablko na validní pozici, tj. taková pozice, na které není had.
                while not valid_food: # Cyklus, který se opakuje dokud není jablko na validní pozici
                    food[0] = (gamesurface.cell_size[0] * random.randint(0, gamesurface.columns - 1)) + gamesurface.start_pos # Náhodná souřadnice X
                    food[1] = (gamesurface.cell_size[1] * random.randint(0, gamesurface.rows - 1)) # Náhodná souřadnice Y
                    if [food[0], food[1]] not in play_snake.body and [food[0], food[1]] not in hostile_snake1.body: # Podmínka kontrolující jestli je jablko na validní pozici
                        valid_food = True

            # Vykreslení jablka
            pygame.draw.rect(screen, (0, 0, 0), (food[0], food[1], gamesurface.cell_size[0], gamesurface.cell_size[1]))
            pygame.draw.rect(screen, (255, 0, 0), (food[0] + 1, food[1] + 1, gamesurface.cell_size[0] - 2, gamesurface.cell_size[1] - 2))

            # Podmínka pro kontrolu kolize hada s jídlem
            if play_snake.body[0] == food: # Podmínka kontrolující jestli jsou souřadnice hlavy hada a jídla stejné
                new_food = True
                play_snake.increase_length() # Zvětšení hada o 1 segment
                score += 10 # Zvýšení skóre o 10 bodů
            elif hostile_snake1.body[0] == food: # Podmínka kontrolující jestli jsou souřadnice hlavy nepřátelského hada a jídla stejné
                new_food = True
                for i in range(5): # Zvětšení hada o 5 segmentů
                    hostile_snake1.increase_length()
                score -= 50 # Snížení skóre o 50 bodů

            ### Hráčův had
            play_snake.draw(screen) # Vykreslení hada
            play_snake.move() # Pohyb hada

            ### Nepřátelští hadi (je možné jich přidat více)
            hostile_snake1.draw(screen) # Vykreslení nepřátelského hada
            hostile_snake1.move() # Pohyb nepřátelských hadů

            # Pohyb nepřátelských hadů
            hostile_snake1.turn_when_hit_wall()

            ### Vykreslení textu
            # Vykreslení textu (ESC) pro pozastavení hry
            text.Text.draw(pausing_text, "(ESC)")

            # Vykreslení textu SCORE
            text.Text.draw(score_text, "SCORE:")

            # Vykreslení skóre
            text.Text.draw(score_text_num, str(score))

            ### Podmínky pro konec hry
            # Podmínka pro kontrolu kolize hada s okrajem herní plochy
            if play_snake.check_collision() == True:
                game_state = "game_over"

            # Podmínka pro kontrolu kolize hada s nepřátelským hadem
            for segment in hostile_snake1.body:
                if play_snake.body[0] == segment:
                    game_state = "game_over"

        elif game_state == "paused_game": # Podmínka pro pozastavenou hru
            # Podmínky pro přepnutí stavu hry
            if home_button_paused.draw(screen) == True:
                game_state = "main_menu"
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                game_state = "game"

            text.Text.draw(paused_game_text1, "GAME PAUSED")
            text.Text.draw(paused_game_text2, "Press SPACE to continue!")

        elif game_state == "game_over": # Podmínka pro konec hry
            # Podmínky pro přepnutí stavu hry
            if home_button_paused.draw(screen) == True:
                game_state = "main_menu"

            text.Text.draw(game_over_text, "GAME OVER!")
            text.Text.draw(game_over_score_text, "SCORE: {}" .format(score))

        # Cyklus pro zpracování událostí
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN: # Podmínka pro stisknutí klávesy 
                    # Pohyb hada
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and game_state == "game": # Podmínka pro pohyb hada doprava
                        play_snake.change_direction("right")
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and game_state == "game": # Podmínka pro pohyb hada doleva
                        play_snake.change_direction("left")
                    elif (event.key == pygame.K_UP or event.key == pygame.K_w) and game_state == "game": # Podmínka pro pohyb hada nahoru
                        play_snake.change_direction("up")
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and game_state == "game": # Podmínka pro pohyb hada dolů
                        play_snake.change_direction("down")

            if event.type == CHANGE_DIRECTION: # Podmínka pro změnu směru nepřátelských hadů
                hostile_snake1.random_turn()

        pygame.display.update() # Obnovení obrazovky

    # Ukončení knihovny Pygame
    pygame.quit()

# Spuštění hry
if __name__ == "__main__":
    main()